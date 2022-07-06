import boto3


class Lambda:

    @staticmethod
    def delete_lambda_function_by_arn(cl: boto3.client, arn: str):
        pass
