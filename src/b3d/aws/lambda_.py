from b3d.aws import helpers
import boto3


@helpers.attempt_api_call_multiple_times
def delete_function(cl: boto3.client, function_name: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    delete_resp = helpers.make_call_catch_err(
        cl.delete_function, FunctionName=function_name
    )

    return delete_resp


def get_function(cl: boto3.client, function_name: str):

    resp = helpers.make_call_catch_err(
        cl.get_function, FunctionName=function_name
    )

    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp
