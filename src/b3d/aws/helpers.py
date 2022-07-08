from botocore.exceptions import ClientError


def make_call_catch_err(fn: callable, **kwargs):
    """
    Catch ClientError exceptions in AWS API calls
    """

    try:
        return fn(**kwargs)
    except ClientError as ce:
        return ce.response
