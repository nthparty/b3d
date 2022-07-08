from src.b3d.delete import Service
import boto3


class Lambda(Service):
    """
    Container class for IAM resource deletion procedures
    """

    @staticmethod
    def service_type():
        return "lambda"

    class Function(Service.Resource):

        @staticmethod
        def resource_type():
            return "lambda-function"

        @staticmethod
        def query(cl: boto3.client, resource_id: str) -> bool:
            """ TODO """
            return True

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return ["function arn here"]
