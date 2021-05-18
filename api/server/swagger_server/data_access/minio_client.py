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
import json
import os
import tarfile
import tempfile

from io import BytesIO
from minio import Minio
from minio.error import NoSuchKey, NoSuchBucketPolicy, ResponseError
from pprint import pprint
from swagger_server.util import ApiError
from tarfile import TarFile
from urllib3 import Timeout
from werkzeug.datastructures import FileStorage


_namespace = os.environ.get("POD_NAMESPACE", "kubeflow")
_host = os.environ.get("MINIO_SERVICE_SERVICE_HOST", "minio-service.%s.svc.cluster.local" % _namespace)
_port = os.environ.get("MINIO_SERVICE_SERVICE_PORT", "9000")
_access_key = 'minio'
_secret_key = 'minio123'


_bucket_policy_sid = "AllowPublicReadAccess"
_bucket_policy_stmt = {
    "Sid": _bucket_policy_sid,
    "Action": ["s3:GetObject"],
    "Effect": "Allow",
    "Principal": {"AWS": ["*"]},
    "Resource": []
}
_bucket_policy_template = {
    "Version": "2012-10-17",
    "Statement": [_bucket_policy_stmt]
}


def _get_minio_client(timeout=None):
    client = Minio(f"{_host}:{_port}", access_key=_access_key, secret_key=_secret_key, secure=False)

    if timeout != Timeout.DEFAULT_TIMEOUT:
        client._http.connection_pool_kw["timeout"] = timeout

    return client


def health_check():
    client = _get_minio_client(timeout=Timeout(connect=0.1, read=0.1))
    client.list_buckets()
    return True


def store_file(bucket_name, prefix, file_name, file_content) -> str:
    client = _get_minio_client()
    f = tempfile.TemporaryFile()
    f.write(file_content)
    size = f.tell()
    f.seek(0)  # return to beginning of file
    object_name = f"{prefix.rstrip('/')}/{file_name}"
    client.put_object(bucket_name, object_name, f, size)  # f.read()
    f.close()  # close and delete temporary file
    object_url = f"http://{_host}:{_port}/{bucket_name}/{object_name}"
    return object_url


def store_tgz(bucket_name, prefix, tgz_file: FileStorage):
    client = _get_minio_client()
    tar = tarfile.open(fileobj=tgz_file.stream, mode="r:gz")

    for member in tar.getmembers():
        file_ext = os.path.splitext(member.name)[-1].lower()

        if file_ext in [".yaml", ".yml", ".md", ".py"]:
            object_name = f"{prefix.rstrip('/')}/{member.name}"
            f = tar.extractfile(member)
            client.put_object(bucket_name, object_name, f, f.raw.size)  # f.read()
            f.close()

    tar.close()
    tgz_file.close()

    return True


def extract_yaml_from_tarfile(uploadfile: FileStorage, filename_filter: str = "", reset_after_read=False) -> str:
    tar = tarfile.open(fileobj=uploadfile.stream, mode="r:gz")

    for member in tar.getmembers():

        file_name = member.name

        # ignore ._ files in tar balls created by Mac OS
        # https://superuser.com/questions/61185/why-do-i-get-files-like-foo-in-my-tarball-on-os-x
        if file_name.startswith("._"):
            continue

        file_ext = file_name.split(".")[-1]

        if file_ext in ["yaml", "yml"] and filename_filter in file_name:
            f = tar.extractfile(member)
            yaml_file_content = f.read()

            if reset_after_read:
                uploadfile.stream.seek(0)  # reset the upload file stream, we might need to re-read later

            f.close()
            tar.close()
            return yaml_file_content

    return None


def create_tarfile(bucket_name: str, prefix: str, file_extensions: [str], keep_open=False) -> (TarFile, BytesIO):
    client = _get_minio_client()
    objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)

    tar_file = BytesIO()
    tar = tarfile.open(mode="w:gz", fileobj=tar_file)

    for o in objects:
        file_name = o.object_name.split("/")[-1]
        file_ext = os.path.splitext(file_name)[-1].lower()

        if file_extensions and file_ext not in file_extensions:
            continue

        if not file_ext and prefix.startswith("pipelines/"):
            file_name = "pipeline.yaml"

        file_content = client.get_object(bucket_name, o.object_name)
        file_obj = BytesIO(file_content.data)
        file_size = file_content.tell()
        tarinfo = tarfile.TarInfo(name=file_name)
        tarinfo.size = file_size
        tar.addfile(tarinfo, file_obj)

    if not keep_open:
        tar.close()

    return tar, tar_file


def retrieve_file_content_and_url(bucket_name, prefix, file_extensions: [str], file_name_filter="") -> [(str, str)]:
    client = _get_minio_client()
    objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)

    files_w_url = []

    for o in objects:
        file_ext = os.path.splitext(o.object_name)[-1].lower()

        if file_ext in file_extensions and file_name_filter in o.object_name:
            file_content = client.get_object(bucket_name, o.object_name)
            object_url = f"http://{_host}:{_port}/{bucket_name}/{o.object_name}"
            files_w_url.append((file_content.data.decode('utf-8'), object_url))

    return files_w_url


def retrieve_file_content(bucket_name, prefix, file_extensions: [str], file_name_filter: str = ""):

    files_w_url = retrieve_file_content_and_url(bucket_name, prefix, file_extensions, file_name_filter)

    if files_w_url:
        (file_content, url) = files_w_url[0]  # TODO: return first result only?
        return file_content

    return None


def get_object_url(bucket_name, prefix, file_extensions: [str], file_name_filter: str = ""):

    files_w_url = retrieve_file_content_and_url(bucket_name, prefix, file_extensions, file_name_filter)

    if files_w_url:
        (file_content, url) = files_w_url[0]  # TODO: return first result only?
        return url

    return None


def delete_object(bucket_name, prefix, file_name):
    client = _get_minio_client()
    try:
        object_name = f"{prefix.rstrip('/')}/{file_name}"
        client.remove_object(bucket_name, object_name)
        return True
    except NoSuchKey as e:
        print(e.message)
        return False


def delete_objects(bucket_name, prefix):
    client = _get_minio_client()
    try:
        if prefix.endswith("/*/"):
            prefix = prefix[:-2]

        objects = client.list_objects(bucket_name, prefix=prefix, recursive=True)
        object_names = [obj.object_name for obj in objects if not obj.is_dir]
        maybe_errors = client.remove_objects(bucket_name, object_names)
        actual_errors = [(e.object_name, e.error_code, e.error_message) for e in maybe_errors]

        if actual_errors:
            pprint(actual_errors)
            return False

        return True

    except NoSuchKey as e:
        print(e.message)
        return False


def enable_anonymous_read_access(bucket_name, prefix):
    _update_bucket_policy(bucket_name, f"{prefix.split('/')[0]}/*")


def _update_bucket_policy(bucket_name: str, prefix: str):
    client = _get_minio_client()

    try:
        bucket_policy = json.loads(client.get_bucket_policy(bucket_name))
    except NoSuchBucketPolicy:
        bucket_policy = dict(_bucket_policy_template)

    getobject_stmts = [s for s in bucket_policy["Statement"] if s.get("Sid") == _bucket_policy_sid] or \
                      [s for s in bucket_policy["Statement"] if "s3:GetObject" in s["Action"]]

    if not getobject_stmts:
        bucket_policy["Statement"].append(_bucket_policy_stmt)
        getobject_stmts = bucket_policy["Statement"][-1]

    resources = getobject_stmts[-1]["Resource"]

    new_resource = f"arn:aws:s3:::{bucket_name}/{prefix}"

    if new_resource not in resources and not any([r.strip("*") in new_resource for r in resources]):
        resources.append(new_resource)

    new_policy_str = json.dumps(bucket_policy)

    try:
        client.set_bucket_policy(bucket_name, new_policy_str)

    except ResponseError as e:

        if e.code == 'XMinioPolicyNesting':
            raise ApiError(
                f"{e.message.split('.')[0]}."
                f" New policy: '{new_policy_str}'."
                f" Existing policy: '{client.get_bucket_policy(bucket_name)}'")

