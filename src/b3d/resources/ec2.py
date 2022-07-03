from src.b3d.resources import Service


class EC2(Service):
    """
    Container class for EC2 resource deletion procedures
    """

    @staticmethod
    def service_type():
        return "ec2"

    class Instance(Service.Resource):

        @staticmethod
        def resource_type():
            return "instances"

        @staticmethod
        def query(arn: str):
            """
            query boto3 EC2 client API to see if an instance with this ARN exists
            """
            return True

        @staticmethod
        def destroy(arn: str, name: str, tag: str, region: str):
            if EC2.Instance.query(arn):
                return ["instance arn here, along with the ARNs of any other resources deleted in the process"]
            else:
                return []

    class SecurityGroup(Service.Resource):

        @staticmethod
        def resource_type():
            return "security_groups"

        @staticmethod
        def query(arn: str):
            return True

        @staticmethod
        def destroy(arn: str, name: str, tag: str, region: str):
            if EC2.SecurityGroup.query(arn):
                return ["security group arn here, along with ARNs of any other resources deleted in the process"]
            else:
                return []

