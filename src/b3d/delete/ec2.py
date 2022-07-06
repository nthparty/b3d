from src.b3d.delete import Service
from src.b3d.utils import aws
import boto3


class EC2(Service):
    """
    Container class for EC2 resource deletion procedures
    """

    @staticmethod
    def service_type():
        return "ec2"

    class Instance(Service.Resource):

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            return arn.split("/")[-1]

        @staticmethod
        def resource_type():
            return "instance"

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return ["instance arn here, along with the ARNs of any other resources affected in the process"]

    class SecurityGroup(Service.Resource):

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            return arn.split("/")[-1]

        @staticmethod
        def resource_type():
            return "security-group"

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):
            return ["security group arn here, along with ARNs of any other resources affected in the process"]

    class Volume(Service.Resource):

        @staticmethod
        def extract_resource_id_from_arn(arn: str) -> str:
            return arn.split("/")[-1]

        @staticmethod
        def resource_type():
            return "volume"

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):

            resps = []
            cl = boto3.client("ec2", region_name=region)
            volume_id = EC2.Volume.extract_resource_id_from_arn(arn)

            # Get IDs of all instances that this volume is attached to
            attachments = aws.EC2.get_volume_attachments(
                cl, volume_id
            )

            # Detach this volume from each instance
            for instance_id in attachments:
                resps.append(
                    aws.EC2.detach_volume_from_instance(cl, instance_id, volume_id)
                )

            # Delete this volume
            resps.append(aws.EC2.delete_volume(cl, volume_id))
            return resps
