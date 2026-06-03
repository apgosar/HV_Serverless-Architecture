"""Simple Lambda: remove S3 objects older than a small threshold.

Design goals:
- Keep code minimal and easy to read.
- Use environment variable `S3_BUCKET` or default to
  the assignment bucket `hv-assignment-test-bucket`.
- Event may supply `bucket` and `age_minutes` to override defaults.

Required IAM permissions for the Lambda role:
- s3:ListBucket (to list objects)
- s3:DeleteObject (to delete objects)
"""

import os
import datetime
from typing import List

import boto3

# Simple configuration
DEFAULT_BUCKET = os.environ.get("S3_BUCKET", "hv-assignment-test-bucket")
S3 = boto3.client("s3")


def _list_old_keys(bucket: str, age_minutes: int) -> List[str]:
    """Return keys whose LastModified is older than age_minutes."""
    now = datetime.datetime.now(datetime.timezone.utc)
    cutoff = now - datetime.timedelta(minutes=age_minutes)
    resp = S3.list_objects_v2(Bucket=bucket)
    contents = resp.get("Contents", [])
    # Collect keys older than cutoff
    return [obj["Key"] for obj in contents if obj.get("LastModified") and obj["LastModified"] < cutoff]


def _delete_keys(bucket: str, keys: List[str]) -> List[str]:
    """Delete given keys and return list of deleted keys.

    This uses S3 batch delete (up to 1000 keys per request).
    """
    deleted: List[str] = []
    for i in range(0, len(keys), 1000):
        chunk = keys[i : i + 1000]
        delete_req = {"Objects": [{"Key": k} for k in chunk]}
        resp = S3.delete_objects(Bucket=bucket, Delete=delete_req)
        for d in resp.get("Deleted", []):
            deleted.append(d.get("Key"))
    return deleted


def lambda_handler(event, context):
    """Lambda handler.

    Event (optional keys):
    - bucket: str -> override default bucket
    - age_minutes: int -> override default age (5)

    Returns a dict with the deleted filenames.
    """
    # Resolve inputs
    bucket = event.get("bucket") if isinstance(event, dict) and event.get("bucket") else DEFAULT_BUCKET
    age = int(event.get("age_minutes", 5)) if isinstance(event, dict) else 5

    # Find and delete
    keys = _list_old_keys(bucket, age)
    if not keys:
        return {"deleted_count": 0, "deleted_files": []}

    deleted = _delete_keys(bucket, keys)
    return {"deleted_count": len(deleted), "deleted_files": deleted}
