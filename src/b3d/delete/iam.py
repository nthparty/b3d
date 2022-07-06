from src.b3d.delete import Service


class IAM(Service):
    """
    Container class for IAM resource deletion procedures
    """

    @staticmethod
    def service_type():
        return "iam"

    class Policy(Service.Resource):

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            return arn.split("/")[-1]

        @staticmethod
        def resource_type():
            return "policy"

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return ["policy arn here, along with the ARNs of any other resources affected in the process"]
