from src.b3d.resources import Service


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
            return "policies"

        @staticmethod
        def query(arn: str):
            return True

        @staticmethod
        def destroy(arn: str, name: str, tag: str, region: str):
            if IAM.Policy.query(arn):
                return ["policy arn here, along with the ARNs of any other resources deleted in the process"]
            else:
                return []