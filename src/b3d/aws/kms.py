"""
KMS helper functions
"""
import boto3
from b3d.aws import helpers


def get_key(cl: boto3.client, key_id: str):
    """
    Describe a key, if it exists
    """

    resp = helpers.make_call_catch_err(
        cl.describe_key, KeyId=key_id
    )

    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


@helpers.attempt_api_call_multiple_times
def disable_key(cl: boto3.client, key_id: str, dry: bool) -> dict:
    """
    Disable a key
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.disable_key, KeyId=key_id
    )


@helpers.attempt_api_call_multiple_times
def schedule_key_deletion(cl: boto3.client, key_id: str, dry: bool) -> dict:
    """
    Schedule a key for deletion
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.schedule_key_deletion, KeyId=key_id
    )
