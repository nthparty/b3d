from src.b3d.delete import Service
from typing import List, Dict
import boto3


class Lambda(Service):
    """
    Container class for IAM resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "lambda"

    class Function(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "lambda-function"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            """ TODO """
            return True

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:
            return []
