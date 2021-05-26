# Copyright 2021 IBM Corporation
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inflection
import inspect
import json
import typing

from datetime import datetime
from kfp_tekton.compiler._k8s_helper import sanitize_k8s_name
from mysql.connector import connect, errorcode, Error
from mysql.connector.errors import IntegrityError
from os import environ as env
from random import choice
from string import ascii_letters, digits, hexdigits
from swagger_server.models.base_model_ import Model
from swagger_server.models import *  # required for dynamic Api ...Extension class loading during View-table creation
from swagger_server.util import _deserialize, ApiError
from typing import List


_namespace = env.get("POD_NAMESPACE", "kubeflow")
_host = env.get("MYSQL_SERVICE_HOST", "mysql.%s.svc.cluster.local" % _namespace)
_port = env.get("MYSQL_SERVICE_PORT", "3306")
_database = 'mlpipeline'
_user = 'root'

existing_tables = dict()

# map Python data types of the Swagger model object's attributes to MySQL column types
type_map = {
    str: 'varchar(255)',
    int: 'int(11)',
    bool: 'tinyint(1)',
    list: 'longtext',
    dict: 'longtext',
    Model: 'longtext',
    datetime: 'bigint(20)'
}
# some attributes do not comply to the defaults in the type_map
swagger_attr_to_mysql_type = {
    'namespace': 'varchar(63)'
}

# some Swagger attributes names have special MySQL column names (KFP idiosyncrasy)
field_name_swagger_to_mysql = {
    'id': 'UUID',
    'created_at': 'CreatedAtInSec'
}
field_name_mysql_to_swagger = {v: k for (k, v) in field_name_swagger_to_mysql.items()}  # Note: overrides duplicates


##############################################################################
#         methods to convert between Swagger and MySQL
##############################################################################

def _convert_value_to_mysql(value, target_type: type, quote_str=False):

    def to_dict(v):
        return v.to_dict() if hasattr(v, "to_dict") else v

    if type(target_type) == typing._GenericAlias:  # or str(target_type).startswith("typing."):
        target_type = eval(target_type._name.lower())

    if value and not issubclass(type(value), target_type) \
            and not (isinstance(value, dict) and issubclass(target_type, Model)):
        err_msg = f"The type '{type(value)}' does not match expected target type '{target_type}' for value '{value}'"
        raise ApiError(err_msg, 422)

    if not value:
        if target_type == bool:
            return False
        elif target_type in [int, float]:
            return 0
        elif target_type in [str, dict, list] or issubclass(target_type, Model):
            return ""
        else:
            return None

    if hasattr(value, "to_dict"):
        mysql_value = json.dumps(value.to_dict())

    elif target_type == list:  # or isinstance(value, list):
        mysql_value = json.dumps(list(map(to_dict, value)))

    elif target_type == dict or issubclass(target_type, Model) and isinstance(value, dict):
        mysql_value = json.dumps(dict(map(lambda item: (item[0], to_dict(item[1])), value.items())))

    elif target_type == datetime:  # or isinstance(value, datetime):
        mysql_value = int(value.timestamp())

    else:
        mysql_value = value

    # DON'T quote strings when using MySQL queries with parameters
    if mysql_value and quote_str and type(mysql_value) == str:
        mysql_value_escaped = mysql_value.replace("'", r"\'")
        mysql_value = f"'{mysql_value_escaped}'"

    return mysql_value


def _convert_value_to_python(value, target_type: type):

    if isinstance(value, int) and target_type == datetime:
        return datetime.fromtimestamp(value)

    elif isinstance(value, str) and (
            type(target_type) == typing._GenericAlias or issubclass(target_type, Model)):

        json_dict = json.loads(value or '{}')
        swaggered_value = _deserialize(json_dict, target_type)
        return swaggered_value

    else:
        return value


def _convert_attr_name_to_col_name(swagger_attr_name: str):

    return field_name_swagger_to_mysql.get(swagger_attr_name) \
           or inflection.camelize(swagger_attr_name)


def _convert_col_name_to_attr_name(mysql_column_name: str):

    return field_name_mysql_to_swagger.get(mysql_column_name) \
           or inflection.underscore(mysql_column_name)


def _get_table_name(swagger_object_or_class) -> str:

    if isinstance(swagger_object_or_class, Model):
        swagger_class = swagger_object_or_class.__class__
    else:
        swagger_class = swagger_object_or_class

    table_name = inflection.underscore(swagger_class.__name__.replace("Api", ""))

    if not table_name.endswith("_extended"):
        return table_name + "s"
    else:
        return table_name.replace("_extended", "s_extended")


##############################################################################
#              general helper methods
##############################################################################

def generate_id(name: str = None, length: int = 36) -> str:
    if name:
        # return name.lower().replace(" ", "-").replace("---", "-").replace("-–-", "–")
        return sanitize_k8s_name(name)
    else:
        # return ''.join([choice(ascii_letters + digits + '-') for n in range(length)])
        return ''.join([choice(hexdigits) for n in range(length)]).lower()


##############################################################################
#         helper methods to create MySQL tables
##############################################################################

def _get_mysql_type_declaration(python_class_or_type) -> str:

    if python_class_or_type in type_map:
        return type_map[python_class_or_type]

    # elif type(python_class_or_type) == typing._GenericAlias:
    elif str(python_class_or_type).startswith("typing."):  # TODO
        type_name = getattr(python_class_or_type, "_name", "").lower()
        clazz = eval(type_name)
        if clazz in type_map:
            return type_map[clazz]

    elif isinstance(python_class_or_type, Model) or issubclass(python_class_or_type, Model):
        clazz = Model
        if clazz in type_map:
            return type_map[clazz]

    raise ValueError(f"Cannot find MySQL data type for Python type {python_class_or_type}")


def _get_mysql_default_value_declaration(default_value):

    if default_value:
        raise ValueError("DEFAULT value not implemented for MySQL CREATE TABLE statement,"
                         f" default: '{default_value}'")

    # TODO: generate MySQL default value declaration
    return default_value or "NOT NULL"


def _get_create_table_statement(swagger_class) -> str:

    table_name = _get_table_name(swagger_class)

    create_table_stmt = [f"CREATE TABLE IF NOT EXISTS `{table_name}` ("]

    # swagger_object.swagger_types dictionary maintains insertion order since Python 3.6
    # but does not show defaults, use inspection to get argument list from constructor
    sig = inspect.signature(swagger_class.__init__)

    for _, p in sig.parameters.items():
        if p.name == "self":
            continue
        field_name = _convert_attr_name_to_col_name(p.name)
        field_type = _get_mysql_type_declaration(p.annotation)
        field_default = _get_mysql_default_value_declaration(p.default)

        create_table_stmt.append(f"  `{field_name}` {field_type} {field_default},")

    if "id" in sig.parameters.keys():
        id_field_name = _convert_attr_name_to_col_name("id")

        create_table_stmt.append(f"  PRIMARY KEY (`{id_field_name}`)")

    else:
        raise ValueError("CREATE TABLE statement requires PRIMARY KEY field. Expected 'id'")

    if "name" in sig.parameters.keys():
        name_field = _convert_attr_name_to_col_name("name")

        create_table_stmt.append(f",  UNIQUE KEY `{name_field}` (`{name_field}`)")

    create_table_stmt.append(") ENGINE=InnoDB DEFAULT CHARSET=latin1")

    create_table_stmt = "\n".join(create_table_stmt)

    print(create_table_stmt)

    return create_table_stmt


def _get_create_view_statement(swagger_class) -> str:

    view_name = _get_table_name(swagger_class)
    base_table_name = view_name.replace("_extended", "")
    extension_table_name = view_name.replace("s_extended", "_extensions")

    extension_swagger_class = eval(swagger_class.__name__.replace("Extended", "Extension"))

    ext_sig = inspect.signature(extension_swagger_class.__init__)

    b_id_col_name = _convert_attr_name_to_col_name("id")
    e_id_col_name = _convert_attr_name_to_col_name("id")

    e_non_id_col_names = [_convert_attr_name_to_col_name(p.name)
                          for _, p in ext_sig.parameters.items()
                          if p.name not in ["id", "self"]]

    e_non_id_col_list = ", ".join([f"e.`{cn}`" for cn in e_non_id_col_names])

    create_view_stmt = f"""
        CREATE VIEW `{view_name}` AS 
        SELECT b.*, {e_non_id_col_list}
        FROM `{base_table_name}` AS b
        LEFT OUTER JOIN `{extension_table_name}` AS e 
        ON b.`{b_id_col_name}`=e.`{e_id_col_name}`
    """

    print(create_view_stmt)

    return create_view_stmt


##############################################################################
#         helper methods to create SQL (query) statement
##############################################################################

def _get_where_clause(swagger_class, filter_dict=dict()) -> str:

    if not filter_dict:
        return None

    sig = inspect.signature(swagger_class.__init__)

    predicates = []

    for attribute_name, attribute_value in filter_dict.items():

        if attribute_name not in sig.parameters.keys():
            raise ValueError(f"{swagger_class} does not have an '{attribute_name}' attribute.")

        attribute_type = sig.parameters[attribute_name].annotation

        column_name = _convert_attr_name_to_col_name(attribute_name)
        column_value = _convert_value_to_mysql(attribute_value, attribute_type, quote_str=True)

        # if type(column_value) == str:
        #     column_value = f"'{column_value}'"

        # TODO: defend against SQL injection attack
        predicates.append(f"`{column_name}` LIKE {column_value}")

    if predicates:
        return "WHERE " + " AND ".join(predicates)

    return None


def _get_orderby_clause(swagger_class, column_name_and_sort_order) -> str:

    if not column_name_and_sort_order:
        return None

    sig = inspect.signature(swagger_class.__init__)

    attr_name, sort_order = (column_name_and_sort_order.split(" ") + ["asc"])[:2]

    if attr_name not in sig.parameters.keys():
        raise ValueError(f"{swagger_class} does not have an '{attr_name}' attribute.")

    column_name = _convert_attr_name_to_col_name(attr_name)

    return f"ORDER BY `{column_name}` {sort_order}"


def _get_limit_clause(count, offset):

    if offset and count:
        return f"LIMIT {offset}, {count}"

    if count:
        return f"LIMIT {count}"

    return None


##############################################################################
#         methods to connect to MySQL and execute db operations
##############################################################################

def _get_connection(timeout: int = 10):

    return connect(host=_host, port=_port, user=_user, database=_database, connection_timeout=timeout)


def _verify_or_create_table(table_name: str, swagger_class_or_object, validate_schema=True) -> bool:

    if table_name not in existing_tables:

        if isinstance(swagger_class_or_object, Model):
            swagger_class = type(swagger_class_or_object)
        else:
            swagger_class = swagger_class_or_object

        if validate_schema:
            _validate_schema(table_name, swagger_class)

        if swagger_class.__name__.endswith("Extended"):
            # first, create the table with the additional columns
            extension_swagger_class = eval(swagger_class.__name__.replace("Extended", "Extension"))
            extension_table_name = _get_table_name(extension_swagger_class)
            create_table_stmt = _get_create_table_statement(extension_swagger_class)
            table_created = _run_create_table_statement(extension_table_name, create_table_stmt)
            existing_tables[extension_table_name] = table_created

            # second, create the table-view that extends the base table with the additional columns from the ext table
            create_view_stmt = _get_create_view_statement(swagger_class)
            view_created = _run_create_table_statement(table_name, create_view_stmt)
            existing_tables[table_name] = view_created
        else:
            create_table_stmt = _get_create_table_statement(swagger_class)
            table_created = _run_create_table_statement(table_name, create_table_stmt)
            existing_tables[table_name] = table_created

    return True


def _validate_schema(table_name: str, swagger_class):

    # swagger_object.swagger_types dictionary maintains insertion order since Python 3.6
    # but does not show defaults, use inspection to get argument list from constructor
    sig = inspect.signature(swagger_class.__init__)

    swagger_columns_w_type = []

    for _, p in sig.parameters.items():
        if p.name == "self":
            continue
        col_name = _convert_attr_name_to_col_name(p.name)
        col_type = swagger_attr_to_mysql_type.get(p.name) or \
                   _get_mysql_type_declaration(p.annotation)

        # hack, TODO: find a more generic solution to custom map columns to types by table
        if issubclass(swagger_class, ApiPipeline) and col_name == "Description":
            col_type = "longtext"

        swagger_columns_w_type.append((col_name, col_type))

    query = f"SELECT COLUMN_NAME, SUBSTR(COLUMN_TYPE,1,64) as COLUMN_TYPE " \
            f"  FROM INFORMATION_SCHEMA.COLUMNS " \
            f"  WHERE TABLE_SCHEMA = '{_database}' AND TABLE_NAME = '{table_name}'"

    cnx = _get_connection()
    cursor = cnx.cursor(buffered=True)

    table_columns_w_type = []

    try:
        cursor.execute(query)
        for column_name, column_type in cursor:
            table_columns_w_type.append((column_name, column_type))

    except Error as err:
        print(err.msg)
        raise err

    finally:
        cursor.close()
        cnx.close()

    if table_columns_w_type and set(table_columns_w_type) != set(swagger_columns_w_type):

        if isinstance(swagger_class, Model):
            swagger_class = type(swagger_class)

        cols_found = "\n  - ".join([f"'{n}' {t}" for n, t in table_columns_w_type])
        cols_expect = "\n  - ".join([f"'{n}' {t}" for n, t in swagger_columns_w_type])

        err_msg = f"The MySQL table '{_database}.{table_name}' does not match Swagger" \
            f" class '{swagger_class.__name__}'.\n" \
            f" Found table with columns:\n" \
            f"  - {cols_found}.\n" \
            f" Expected table with columns:\n" \
            f"  - {cols_expect}.\n" \
            f" Delete and recreate the table by calling the API endpoint 'DELETE /{table_name}/*'"

        raise ApiError(err_msg)

    return True


def _run_create_table_statement(table_name, table_description: tuple) -> bool:

    cnx = _get_connection()
    cnx.autocommit = True
    cursor = cnx.cursor(buffered=True)

    try:
        print(f"Creating table '{table_name}': ", end='')
        cursor.execute(table_description)
        cnx.commit()
        print("OK")

    except Error as err:

        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("already exists.")
        else:
            print(err.msg)
            raise err

    finally:
        cursor.close()
        cnx.close()

    return True


##############################################################################
#      public methods to store, load, delete data in a MySQL database
##############################################################################

# _host = "123.34.13.12"

def health_check():
    cnx = _get_connection(timeout=1)
    cnx.connect()
    cnx.disconnect()
    cnx.close()
    return True


def num_rows(swagger_class: type) -> int:

    table_name = _get_table_name(swagger_class)

    _verify_or_create_table(table_name, swagger_class)

    query = f"SELECT TABLE_ROWS FROM INFORMATION_SCHEMA.TABLES " \
            f"WHERE TABLE_SCHEMA = '{_database}' AND TABLE_NAME = '{table_name}'"

    cnx = _get_connection()
    cursor = cnx.cursor()

    try:
        cursor.execute(query)
        num_records, = cursor.fetchone()

    except Error as err:
        print(err.msg)
        raise err

    finally:
        cursor.close()
        cnx.close()

    return num_records


def store_data(swagger_object: Model) -> str:

    table_name = _get_table_name(swagger_object)

    _verify_or_create_table(table_name, swagger_object)

    swagger_fields = swagger_object.to_dict().keys()

    # TODO: remove generate_id() calls in controller_impl methods, do it here
    if "id" in swagger_fields and not swagger_object.id:
        swagger_object.id = generate_id(swagger_object.name if "name" in swagger_fields else None)

    # TODO: remove creating a new data in controller_impl methods, do it here
    if "created_at" in swagger_fields and not swagger_object.created_at:
        swagger_object.created_at = datetime.now()

    column_names = [_convert_attr_name_to_col_name(f) for f in swagger_fields]
    column_values = [_convert_value_to_mysql(getattr(swagger_object, f),
                                             swagger_object.swagger_types[f])
                     for f in swagger_fields]

    column_names_str = ", ".join(column_names)
    values_list_str = ('%s,' * len(column_values)).rstrip(',')

    insert_stmt = (f"INSERT INTO {table_name} "
                   f"({column_names_str}) "
                   f"VALUES ({values_list_str})")

    cnx = _get_connection()
    cnx.autocommit = True
    cursor = cnx.cursor()

    try:
        cursor.execute(insert_stmt, tuple(column_values))
        cnx.commit()

    except IntegrityError as e:
        cnx.rollback()
        raise ApiError(e.msg, 409)

    except Error as err:
        cnx.rollback()
        print(err.msg)
        print(insert_stmt)
        print(column_values)
        raise err

    finally:
        cursor.close()
        cnx.close()

    return swagger_object.id


def update_multiple(swagger_class: type, ids: List[str], attribute_name: str, value):

    table_name = _get_table_name(swagger_class)

    _verify_or_create_table(table_name, swagger_class, False)

    sig = inspect.signature(swagger_class.__init__)

    if attribute_name not in sig.parameters.keys():
        raise ValueError(f"{swagger_class} does not have an attribute with name '{attribute_name}'.")

    if ids and "id" not in sig.parameters.keys():
        raise ValueError(f"{swagger_class} does not have an 'id' attribute.")

    update_column_name = _convert_attr_name_to_col_name(attribute_name)
    update_column_value = _convert_value_to_mysql(value, sig.parameters.get(attribute_name).annotation, quote_str=False)

    # if type(update_column_value) == str:
    #     update_column_value = f"'{update_column_value}'"

    if not ids or ids[0] == "*":
        # if we get an empty list, we assume the update is for all
        update_stmt = f"UPDATE `{table_name}` \
                        SET `{update_column_name}` = %s"
    else:
        id_column_name = _convert_attr_name_to_col_name("id")
        str_of_quoted_ids = ",".join([f"'{id}'" for id in ids])

        update_stmt = f"UPDATE `{table_name}` \
                        SET `{update_column_name}` = %s \
                        WHERE `{id_column_name}` in ({str_of_quoted_ids})"

    cnx = _get_connection()
    cnx.autocommit = True
    cursor = cnx.cursor()

    try:
        cursor.execute(update_stmt, params=[update_column_value])
        cnx.commit()

    except Error as err:
        cnx.rollback()
        print(err.msg)
        print(update_stmt)
        raise err

    finally:
        cursor.close()
        cnx.close()


def delete_data(swagger_class: type, id: str) -> bool:

    table_name = _get_table_name(swagger_class)

    if id != "*":
        # don't create tables if we will delete it a few lines later
        _verify_or_create_table(table_name, swagger_class, False)

    sig = inspect.signature(swagger_class.__init__)

    if not id:
        raise ValueError(f"Must specify 'id' column value to delete row from table '{table_name}'")

    elif "id" not in sig.parameters.keys():
        raise ValueError(f"{swagger_class} does not have an 'id' attribute.")

    elif id == "*":
        # until we have a proper schema migration, use this opportunity to force recreating of the table later
        if table_name.endswith("extended"):
            sql = f"DROP VIEW IF EXISTS `{table_name}`"
        elif table_name in ["pipelines", "pipeline_versions"]:
            sql = f"DELETE FROM `{table_name}`"
        else:
            sql = f"DROP TABLE IF EXISTS `{table_name}`"

        if sql.startswith("DROP ") and table_name in existing_tables:
            existing_tables.pop(table_name)

    else:
        column_name = _convert_attr_name_to_col_name("id")
        column_value = _convert_value_to_mysql(id, str, True)
        sql = f"DELETE FROM `{table_name}` WHERE `{column_name}` = {column_value}"

    cnx = _get_connection()
    cursor = cnx.cursor()

    try:
        cursor.execute(sql)
        cnx.commit()

    except IntegrityError as e:
        cnx.rollback()
        return e.msg

    except Error as err:
        cnx.rollback()
        print(err.msg)
        raise err

    finally:
        cursor.close()
        cnx.close()

    return True  # TODO: determine return value


def load_data(swagger_class: type, filter_dict: dict = None, sort_by: str = None, count: int = 100, offset: int = 0) -> [Model]:

    table_name = _get_table_name(swagger_class)

    _verify_or_create_table(table_name, swagger_class)

    sig = inspect.signature(swagger_class.__init__)

    where_clause = _get_where_clause(swagger_class, filter_dict) or ""
    orderby_clause = _get_orderby_clause(swagger_class, sort_by) or ""
    limit_clause = _get_limit_clause(count, offset) or ""

    query = f"SELECT * FROM {table_name} {where_clause} {orderby_clause} {limit_clause}"

    cnx = _get_connection()
    cursor = cnx.cursor(buffered=True, dictionary=False)

    swagger_objects = []

    try:
        cursor.execute(query)

        swagger_attr_names = [_convert_col_name_to_attr_name(c) for c in cursor.column_names]

        assert set(swagger_attr_names) <= set(sig.parameters.keys()), \
            f"Mismatch between database schema and API spec for {table_name}. " \
            f"Expected columns: {[_convert_attr_name_to_col_name(k) for k in sig.parameters.keys() if k != 'self']}. " \
            f"Database columns: {cursor.column_names}"

        swagger_attr_types = [sig.parameters.get(a).annotation for a in swagger_attr_names]

        for row_values in cursor:
            value_type_tuples = zip(list(row_values), swagger_attr_types)
            swagger_attr_values = [_convert_value_to_python(v, t) for v, t in value_type_tuples]
            swagger_attr_dict = dict(zip(swagger_attr_names, swagger_attr_values))
            swagger_object = swagger_class(**swagger_attr_dict)

            swagger_objects.append(swagger_object)

    except Error as err:
        print(err.msg)
        raise err

    finally:
        cursor.close()
        cnx.close()

    return swagger_objects
