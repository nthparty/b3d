"""
Delete procedures for unsupported resources
"""
import boto3
from b3d.delete import Service
from b3d.utils import log_msg


class UnsupportedService(Service):
    """
    Container class for unsupported resource delete procedures
    """

    @staticmethod
    def service_type():
        return "unsupported-service"

    class UnsupportedResource(Service.Resource):
        """
        Delete procedure for unsupported objects
        """

        @staticmethod
        def resource_type():
            return "unsupported-resource"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return True

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return log_msg.log_msg_unsupported_resource(arn)
