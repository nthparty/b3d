from b3d.delete import Service
from b3d import aws
from b3d.utils import log_msg
from typing import List, Dict
import boto3


class Lambda(Service):
    """
    Container class for Lambda resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "lambda"

    class Function(Service.Resource):

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            return arn.split(":")[-1]

        @staticmethod
        def resource_type() -> str:
            return "function"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.lambda_.get_function(
                cl, Lambda.Function.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("lambda", region_name=region)
            function_name = Lambda.Function.extract_resource_id_from_arn(arn)

            if not Lambda.Function.query(cl, arn):
                return resps

            # Destroy this function
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="function",
                    resource_id=function_name,
                    resp=aws.lambda_.delete_function(cl, function_name, dry=dry)
                )
            )

            return resps
