from botocore.exceptions import ClientError
import boto3


def make_call_catch_err(fn: callable, **kwargs):
    """
    Catch ClientError exceptions in AWS API calls
    """

    try:
        return fn(**kwargs)
    except ClientError as ce:
        return ce.response


def wait_on_condition(cl: boto3.client, condition: str, **kwargs):

    waiter = cl.get_waiter(condition)
    waiter.wait(**kwargs)


def dry_run_success_resp():
    return {
        "ResponseMetadata": {
            "HTTPStatusCode": 200
        }
    }
