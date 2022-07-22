from b3d.aws import helpers
import boto3


def get_parameter(cl: boto3.client, parameter_name: str):

    resp = helpers.make_call_catch_err(
        cl.get_parameter, Name=parameter_name
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


@helpers.attempt_api_call_multiple_times
def delete_parameter(cl: boto3.client, parameter_name: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_parameter, Name=parameter_name
    )
