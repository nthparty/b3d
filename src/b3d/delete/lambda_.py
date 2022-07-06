from src.b3d.delete import Service


class Lambda(Service):
    """
    Container class for IAM resource deletion procedures
    """

    @staticmethod
    def service_type():
        return "lambda"

    class Function(Service.Resource):

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            return arn.split("/")[-1]

        @staticmethod
        def resource_type():
            return "lambda-function"

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return ["function arn here"]
