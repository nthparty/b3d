from b3d.aws import helpers
import boto3
import b3q


@helpers.attempt_api_call_multiple_times
def delete_instance(cl: boto3.client, instance_id: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    resp = helpers.make_call_catch_err(
        cl.terminate_instances, InstanceIds=[instance_id]
    )

    if resp["ResponseMetadata"]["HTTPStatusCode"] == 200:
        helpers.wait_on_condition(cl, "instance_terminated", InstanceIds=[instance_id])

    return resp


def get_instance(cl: boto3.client, instance_id: str):

    resp = helpers.make_call_catch_err(
        cl.describe_instances, InstanceIds=[instance_id]
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def describe_all_instances(cl: boto3.client):
    return list(b3q.get(
        cl.describe_instances,
        attribute="Reservations"
    ))


@helpers.attempt_api_call_multiple_times
def delete_security_group(cl: boto3.client, security_group_id: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_security_group, GroupId=security_group_id
    )


def get_security_group(cl: boto3.client, security_group_id: str):

    resp = helpers.make_call_catch_err(
        cl.describe_security_groups, GroupIds=[security_group_id]
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def get_default_security_group_id(cl: boto3.client):
    """
    In general, each VPC has a default security group named 'default'. We need
    to retrieve its ID in order to remove security groups from instances, because
    the modify_instance_attribute API call requires at least 1 security group ID
    as part of the request.
    """

    resp = helpers.make_call_catch_err(
        cl.describe_security_groups, GroupNames=["default"]
    )

    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 \
        else resp["SecurityGroups"][0]["GroupId"]


@helpers.attempt_api_call_multiple_times
def delete_volume(cl: boto3.client, volume_id: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_volume, VolumeId=volume_id
    )


def get_volume(cl: boto3.client, volume_id: str):

    resp = helpers.make_call_catch_err(cl.describe_volumes, VolumeIds=[volume_id])
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def get_volume_attachments(cl: boto3.client, volume_id: str):
    """
    Return the IDs for all instances that a given volume is attached to.
    """

    volume_data = get_volume(cl, volume_id)
    if volume_data is None:
        # Volume not found, already deleted.
        return []
    else:
        return [
            attachment["InstanceId"]for attachment in volume_data["Volumes"][0]["Attachments"]
        ]


def detach_volume_from_instance(cl: boto3.client, instance_id: str, volume_id: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.detach_volume, InstanceId=instance_id, VolumeId=volume_id
    )


def detach_security_group_from_instance(
        cl: boto3.client,
        instance_id: str,
        attached_security_groups: list,
        target_security_group_id: str,
        dry: bool
):
    """
    Detach a target security group from an instance.
    """

    if dry:
        return helpers.dry_run_success_resp()

    result_groups = [sg for sg in attached_security_groups if sg != target_security_group_id]
    default_security_group_id = get_default_security_group_id(cl)

    # If this VPC does not have a default security group (which shouldn't happen),
    # we won't be able to detach this security group from an instance because EC2
    # requires that at least 1 security group be attached.
    if default_security_group_id is None and len(result_groups) == 0:
        raise ValueError("No default security group detected for this VPC")

    return helpers.make_call_catch_err(
        cl.modify_instance_attribute,
        InstanceId=instance_id,
        Groups=result_groups if result_groups != [] else [default_security_group_id]
    )


def get_all_instances_with_security_group_id(cl: boto3.client, security_group_id: str):
    """
    Given some security group ID, return the IDs of all instances that its attached to. IDs for
    all security groups currently attached to the instance are also returned, as they are needed
    to detach the target security group later.
    """

    ret = []
    all_instances = describe_all_instances(cl)

    for instance in all_instances:

        # Each instance record has an 'Instances'  list, but there should only be one entry per instance
        instance_data = instance["Instances"][0]
        security_groups = [sg["GroupId"] for sg in instance_data.get("SecurityGroups", [])]
        if security_group_id in security_groups:
            ret.append(
                (
                    instance_data.get("InstanceId"),
                    [gid for gid in security_groups if gid != security_group_id]
                )
            )

    return ret
