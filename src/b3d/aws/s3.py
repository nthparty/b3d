from b3d.aws import helpers
import boto3


def get_bucket(cl: boto3.client, bucket_name: str) -> bool:

    resp = helpers.make_call_catch_err(
        cl.head_bucket, Bucket=bucket_name
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


@helpers.attempt_api_call_multiple_times
def delete_bucket(cl: boto3.client, bucket_name: str, dry: bool) -> dict:

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_bucket, Bucket=bucket_name
    )


def get_objects_in_bucket(cl: boto3.client, bucket_name: str) -> list:

    resp = helpers.make_call_catch_err(
        cl.list_objects, Bucket=bucket_name
    )
    return [obj.get("Key") for obj in resp.get("Contents", [])]


@helpers.attempt_api_call_multiple_times
def delete_objects(cl: boto3.client, bucket_name: str, objects: list, dry: bool) -> dict:

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_objects,
        Bucket=bucket_name,
        Delete={"Objects": [{"Key": k} for k in objects]}
    )
