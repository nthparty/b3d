import boto3


class EC2:
    """
    Container class for atomic EC2 API functions.

    TODO: Need to wrap responses in some kind of structured message format for logging.
    """

    @staticmethod
    def delete_instance(cl: boto3.client, instance_id: str):
        return cl.terminate_instances(InstanceIds=instance_id)

    @staticmethod
    def delete_volume(cl: boto3.client, volume_id: str):
        return cl.delete_volume(VolumeId=volume_id)

    @staticmethod
    def delete_security_group(cl: boto3.client, security_group_id: str):
        pass

    @staticmethod
    def get_volume_attachments(cl: boto3.client, volume_id: str):
        """
        Return the IDs for all instances that a given volume is attached to.
        """

        vol = cl.describe_volumes(VolumeIds=[volume_id])
        return [
            attachment["InstanceId"]
            for attachment in vol["Volumes"][0]["Attachments"]
        ]

    @staticmethod
    def detach_volume_from_instance(cl: boto3.client, instance_id: str, volume_id: str):
        return cl.detach_volume(
            InstanceId=instance_id,
            VolumeId=volume_id
        )

    @staticmethod
    def detach_security_group_from_instance(cl: boto3.client, instance_arn: str, security_group_arn: str):
        pass