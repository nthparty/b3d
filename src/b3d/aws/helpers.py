"""
Helper functions for this module
"""
import time
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
    """
    Instantiate and run a waiter object
    """

    waiter = cl.get_waiter(condition)
    waiter.wait(**kwargs)


def attempt_api_call_multiple_times(func):
    """
    Sometimes the AWS API needs time to catch up when doing multiple
    delete / detach calls in sequence. This function can be added as
    a decorator for any API call that returns a ["ResponseMetadata"]["HTTPStatusCode"]
    key path in its response dictionary.
    """

    def wrap(*args, **kwargs):

        resp = {}
        attempts = 0

        while attempts < 3:

            resp = func(*args, **kwargs)
            if resp["ResponseMetadata"]["HTTPStatusCode"] in [200, 202, 204]:
                return resp

            attempts += 1
            time.sleep(10)

        return resp
    return wrap


def dry_run_success_resp():
    """
    Produce a generic success response. Used in dry runs
    """
    return {
        "ResponseMetadata": {
            "HTTPStatusCode": 200
        }
    }
