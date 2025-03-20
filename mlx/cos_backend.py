import json
import boto3
import jsonschema
from jsonschema import validate


class COSKVStore:
    def __init__(self, bucket_name, schema, cos_client=None):
        """
        Initialize the COS Key-Value store.
        :param bucket_name: Name of the COS bucket.
        :param schema: JSON Schema to validate values.
        :param cos_client: Optional COS client instance (for dependency injection).
        """
        self.bucket_name = bucket_name
        self.schema = schema
        self.cos_client = cos_client or boto3.client('s3')

    def put(self, key, value):
        """
        Store a value in COS after validating against the JSON schema.
        :param key: The key under which the value is stored.
        :param value: The value to store (must be JSON-serializable).
        """
        try:
            validate(instance=value, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            raise ValueError(f"Validation error: {e.message}")

        self.cos_client.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=json.dumps(value)
        )

    def get(self, key):
        """
        Retrieve a value from COS.
        :param key: The key to retrieve.
        :return: The stored value as a dictionary.
        """
        try:
            response = self.cos_client.get_object(Bucket=self.bucket_name, Key=key)
            return json.loads(response['Body'].read().decode('utf-8'))
        except self.cos_client.exceptions.NoSuchKey:
            raise KeyError(f"Key '{key}' not found in bucket '{self.bucket_name}'")

    def delete(self, key):
        """
        Delete a key-value pair from COS.
        :param key: The key to delete.
        """
        self.cos_client.delete_object(Bucket=self.bucket_name, Key=key)

    def list_keys(self):
        """
        List all keys in the COS bucket.
        :return: A list of keys.
        """
        response = self.cos_client.list_objects_v2(Bucket=self.bucket_name)
        return [obj['Key'] for obj in response.get('Contents', [])]


# Example Usage
if __name__ == "__main__":
    example_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"}
        },
        "required": ["name", "age"]
    }

    cos_store = COSKVStore("my-cos-bucket", example_schema)
    test_data = {"name": "John Doe", "age": 30}
    cos_store.put("user_123", test_data)
    print(cos_store.get("user_123"))
