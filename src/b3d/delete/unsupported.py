from b3d.delete import Service
from b3d.utils import log_msg
import boto3


class UnsupportedService(Service):
    """
    Container class for IAM resource deletion procedures
    """

    @staticmethod
    def service_type():
        return "unsupported-service"

    class UnsupportedResource(Service.Resource):

        @staticmethod
        def resource_type():
            return "unsupported-resource"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return True

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return log_msg.log_msg_unsupported_resource(arn)
