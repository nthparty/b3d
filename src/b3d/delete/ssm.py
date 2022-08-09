"""
Delete procedures for S3 resources
"""
from typing import List, Dict
import boto3
from b3d.delete import Service
from b3d import aws
from b3d.utils import log_msg


class SSM(Service):
    """
    Container class for SSM resource delete procedures
    """

    @staticmethod
    def service_type() -> str:
        return "ssm"

    class Parameter(Service.Resource):
        """
        Delete procedure for Parameter objects
        """

        @staticmethod
        def resource_type() -> str:
            return "parameter"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.ssm.get_parameter(
                cl, SSM.Parameter.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            cl = boto3.client("ssm", region_name=region)
            parameter_name = SSM.Parameter.extract_resource_id_from_arn(arn)

            if not SSM.Parameter.query(cl, arn):
                return []

            return [
                log_msg.log_msg_destroy(
                    resource_type="parameter",
                    resource_id=parameter_name,
                    resp=aws.ssm.delete_parameter(cl, parameter_name, dry)
                )
            ]
