from src.b3d.delete import Service
from src.b3d import aws
from src.b3d.utils import log_msg
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
        def resource_type():
            return "instance"

        @staticmethod
        def query(cl: boto3.client, resource_id: str) -> bool:
            return aws.ec2.get_instance(cl, resource_id) is not None

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):

            resps = []
            cl = boto3.client("ec2", region_name=region)
            instance_id = EC2.Instance.extract_resource_id_from_arn(arn)

            if not EC2.Instance.query(cl, instance_id):
                return resps

            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="instance",
                    resource_id=instance_id,
                    resp=aws.ec2.delete_instance(cl, instance_id)
                )
            )

            return resps

    class SecurityGroup(Service.Resource):

        @staticmethod
        def resource_type():
            return "security-group"

        @staticmethod
        def query(cl: boto3.client, resource_id: str) -> bool:
            return aws.ec2.get_security_group(cl, resource_id) is not None

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):

            resps = []
            cl = boto3.client("ec2", region_name=region)
            security_group_id = EC2.SecurityGroup.extract_resource_id_from_arn(arn)

            if not EC2.SecurityGroup.query(cl, security_group_id):
                return resps

            # Get IDs of all instances that this security group is attached to
            all_instances_attached = aws.ec2.get_all_instances_with_security_group_id(
                cl, security_group_id
            )

            # Detach this security group from each instance
            for instance_id, group_ids in all_instances_attached:
                resps.append(
                    log_msg.log_msg_detach(
                        resource_type_detached_from="instance",
                        resource_type_detached="security-group",
                        resource_id_detached_from=instance_id,
                        resource_id_detached=security_group_id,
                        resp=aws.ec2.detach_security_group_from_instance(
                            cl, instance_id, group_ids, security_group_id
                        )
                    )
                )

            # Delete this security group
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="security-group",
                    resource_id=security_group_id,
                    resp=aws.ec2.delete_security_group(cl, security_group_id)
                )
            )

            return resps

    class Volume(Service.Resource):

        @staticmethod
        def resource_type():
            return "volume"

        @staticmethod
        def query(cl: boto3.client, resource_id: str) -> bool:
            return aws.ec2.get_volume(cl, resource_id) is not None

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True):

            resps = []
            cl = boto3.client("ec2", region_name=region)
            volume_id = EC2.Volume.extract_resource_id_from_arn(arn)

            # Abort if this resource doesn't exist
            if not EC2.Volume.query(cl, volume_id):
                return resps

            # Get IDs of all instances that this volume is attached to
            attachments = aws.ec2.get_volume_attachments(
                cl, volume_id
            )

            # Detach this volume from each instance
            for instance_id in attachments:
                resps.append(
                    log_msg.log_msg_detach(
                        resource_type_detached_from="instance",
                        resource_type_detached="volume",
                        resource_id_detached=volume_id,
                        resource_id_detached_from=instance_id,
                        resp=aws.ec2.detach_volume_from_instance(
                            cl, instance_id, volume_id
                        )
                    )
                )

            # Delete this volume
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="volume",
                    resource_id=volume_id,
                    resp=aws.ec2.delete_volume(cl, volume_id)
                )
            )

            return resps
