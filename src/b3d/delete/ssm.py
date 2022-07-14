from src.b3d.delete import Service
from src.b3d import aws
from src.b3d.utils import log_msg
from typing import List, Dict
import boto3


class SSM(Service):
    """
    Container class for SSM resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "ssm"

    class Parameter(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "parameter"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return True

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:
            return []
