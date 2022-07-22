from tests import config


def create_security_group(group_name: str):

    resp = config.MASTER_EC2_CLIENT.create_security_group(
        Description="B3D test security group",
        GroupName=group_name
    )

    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f"Error trying to create security group {group_name}: {resp}")

    waiter = config.MASTER_EC2_CLIENT.get_waiter("security_group_exists")
    waiter.wait(GroupIds=[resp["GroupId"]])

    return resp["GroupId"]


def create_instance(**kwargs):

    resp = config.MASTER_EC2_CLIENT.run_instances(
        ImageId=config.TEST_AMI_ID,
        InstanceType="t2.micro",
        MaxCount=1,
        MinCount=1,
        Placement={
            "AvailabilityZone": config.AVAILABILITY_ZONE
        },
        **kwargs
    )

    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f"Error trying to start instance: {resp}")

    waiter = config.MASTER_EC2_CLIENT.get_waiter("instance_running")
    waiter.wait(InstanceIds=[resp["Instances"][0]["InstanceId"]])

    return resp["Instances"][0]["InstanceId"]


def create_volume():

    resp = config.MASTER_EC2_CLIENT.create_volume(
        AvailabilityZone=config.AVAILABILITY_ZONE,
        Size=10
    )

    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f"Error trying to create volume: {resp}")

    waiter = config.MASTER_EC2_CLIENT.get_waiter("volume_available")
    waiter.wait(VolumeIds=[resp["VolumeId"]])

    return resp["VolumeId"]


def attach_volume(instance_id: str, volume_id: str):

    resp = config.MASTER_EC2_CLIENT.attach_volume(
        Device="/dev/sdh",
        InstanceId=instance_id,
        VolumeId=volume_id
    )

    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f"Error trying to attach volume {volume_id} to instance {instance_id}: {resp}")

    waiter = config.MASTER_EC2_CLIENT.get_waiter("volume_in_use")
    waiter.wait(
        VolumeIds=[volume_id],
        Filters=[
            {
                "Name": "attachment.instance-id",
                "Values": [instance_id]
            }
        ]
    )


def tag_ec2_resources(resource_ids: list, tags: list):

    resp = config.MASTER_EC2_CLIENT.create_tags(
        Resources=resource_ids,
        Tags=tags
    )

    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        raise Exception(f"Error tagging resources with IDs {resource_ids}: {resp}")
