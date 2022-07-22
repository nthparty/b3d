from b3d.delete import Service
from b3d import aws
from b3d.utils import log_msg
from typing import List, Dict
import boto3


class EC2(Service):
    """
    Container class for EC2 resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "ec2"

    class Instance(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "instance"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:

            instance_data = aws.ec2.get_instance(
                cl, EC2.Instance.extract_resource_id_from_arn(resource_arn)
            )

            if instance_data is None:
                return False

            try:
                return instance_data["Reservations"][0]["Instances"][0]["State"]["Name"] != "terminated"
            except IndexError:
                return False

        @staticmethod
        def _detach_all_security_groups(cl: boto3.client, instance_id: str, dry: bool):

            resps = []

            instance_resp = aws.ec2.get_instance(cl, instance_id)
            try:
                all_groups = [
                    sg["GroupId"] for sg in
                    instance_resp["Reservations"][0]["Instances"][0].get("SecurityGroups", [])
                ]
            # Instance terminated but not cleaned up yet
            except IndexError:
                return []

            for sg in all_groups:
                resps.append(
                    log_msg.log_msg_detach(
                        resource_type_detached_from="instance",
                        resource_type_detached="security-group",
                        resource_id_detached_from=instance_id,
                        resource_id_detached=sg,
                        resp=aws.ec2.detach_security_group_from_instance(
                            cl, instance_id, all_groups, sg, dry=dry
                        )
                    )
                )

            return resps

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("ec2", region_name=region)
            instance_id = EC2.Instance.extract_resource_id_from_arn(arn)

            if not EC2.Instance.query(cl, arn):
                return resps

            # Detach all security groups from this instance
            resps.extend(EC2.Instance._detach_all_security_groups(cl, instance_id, dry))

            # Terminate this instance
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="instance",
                    resource_id=instance_id,
                    resp=aws.ec2.delete_instance(cl, instance_id, dry=dry)
                )
            )

            return resps

    class SecurityGroup(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "security-group"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.ec2.get_security_group(
                cl, EC2.SecurityGroup.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def _detach_from_instances(cl: boto3.client, security_group_id: str, dry: bool) -> List[Dict]:
            """
            Get IDs of all instances this security group is attached to and detach it from each
            """

            resps = []

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
                            cl, instance_id, group_ids, security_group_id, dry=dry
                        )
                    )
                )

            return resps

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("ec2", region_name=region)
            security_group_id = EC2.SecurityGroup.extract_resource_id_from_arn(arn)

            if not EC2.SecurityGroup.query(cl, arn):
                return resps

            # Detach this security group from instances
            resps.extend(EC2.SecurityGroup._detach_from_instances(cl, security_group_id, dry))

            # Delete this security group
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="security-group",
                    resource_id=security_group_id,
                    resp=aws.ec2.delete_security_group(cl, security_group_id, dry=dry)
                )
            )

            return resps

    class Volume(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "volume"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.ec2.get_volume(
                cl, EC2.Volume.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def _detach_from_instances(cl: boto3.client, volume_id: str, dry: bool) -> List[Dict]:
            """
            Get IDs of all instances this volume is attached to and detach it from each
            """

            resps = []

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
                            cl, instance_id, volume_id, dry=dry
                        )
                    )
                )

            return resps

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("ec2", region_name=region)
            volume_id = EC2.Volume.extract_resource_id_from_arn(arn)

            # Abort if this resource doesn't exist
            if not EC2.Volume.query(cl, arn):
                return resps

            # Detach this volume from instances
            resps.extend(EC2.Volume._detach_from_instances(cl, volume_id, dry))

            # Delete this volume
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="volume",
                    resource_id=volume_id,
                    resp=aws.ec2.delete_volume(cl, volume_id, dry=dry)
                )
            )

            return resps
