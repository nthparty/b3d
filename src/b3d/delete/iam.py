from src.b3d.delete import Service
import boto3


class IAM(Service):
    """
    Container class for IAM resource deletion procedures
    """

    @staticmethod
    def service_type():
        return "iam"

    class Policy(Service.Resource):

        @staticmethod
        def resource_type():
            return "policy"

        @staticmethod
        def query(cl: boto3.client, resource_id: str) -> bool:
            """ TODO """
            return True

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return ["policy arn here, along with the ARNs of any other resources affected in the process"]
