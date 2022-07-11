from src.b3d.aws import helpers
from typing import List, Dict
import boto3
import b3q


def delete_policy(cl: boto3.client, policy_arn: str) -> dict:
    return helpers.make_call_catch_err(
        cl.delete_policy, PolicyArn=policy_arn
    )


def get_policy(cl: boto3.client, policy_arn: str) -> dict:

    resp = helpers.make_call_catch_err(cl.get_policy, PolicyArn=policy_arn)
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def delete_role(cl: boto3.client, role_name: str) -> dict:
    return helpers.make_call_catch_err(
        cl.delete_role, RoleName=role_name
    )


def get_role(cl: boto3.client, role_name: str) -> dict:

    resp = helpers.make_call_catch_err(cl.get_role, RoleName=role_name)
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def delete_instance_profile(cl: boto3.client, instance_profile_name: str) -> dict:
    return helpers.make_call_catch_err(
        cl.delete_instance_profile, InstanceProfileName=instance_profile_name
    )


def get_all_users(cl: boto3.client) -> List[Dict]:
    return list(b3q.get(
        cl.list_users, attribute="Users"
    ))


def delete_user(cl: boto3.client, user_name: str) -> dict:
    return helpers.make_call_catch_err(
        cl.delete_user, UserName=user_name
    )


def get_user(cl: boto3.client, user_name: str) -> dict:

    resp = helpers.make_call_catch_err(
        cl.get_user, UserName=user_name
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def get_attached_user_policies(cl: boto3.client, user_name: str) -> List[Dict]:

    resp = helpers.make_call_catch_err(
        cl.list_attached_user_policies, UserName=user_name
    )
    return [] if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp.get("AttachedPolicies", [])


def get_user_access_keys(cl: boto3.client, user_name: str) -> List[Dict]:
    resp = helpers.make_call_catch_err(
        cl.list_access_keys, UserName=user_name
    )
    return [] if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp.get("AccessKeyMetadata", [])


def delete_access_key(cl: boto3.client, user_name: str, access_key_id: str) -> dict:
    return helpers.make_call_catch_err(
        cl.delete_access_key, UserName=user_name, AccessKeyId=access_key_id
    )


def get_instance_profile(cl: boto3.client, instance_profile_name: str) -> dict:

    resp = helpers.make_call_catch_err(cl.get_instance_profile, InstanceProfileName=instance_profile_name)
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def detach_policy_from_role(cl: boto3.client, policy_arn: str, role_id: str):
    pass


def detach_instance_profile_from_ec2_instance(cl: boto3.client, instance_profile_id: str, instance_id: str):
    pass


def detach_policy_from_user(cl: boto3.client, user_name: str, policy_arn: str):
    return helpers.make_call_catch_err(
        cl.detach_user_policy, UserName=user_name, PolicyArn=policy_arn
    )


def user_has_permissions_boundary(cl: boto3.client, user_name: str) -> bool:

    user_data = get_user(cl, user_name)

    # If user doesn't exist, return False
    if user_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return False

    # If user exists and they have a permissions boundary set, return True
    return user_data["User"].get("PermissionsBoundary") is not None


def policy_is_permissions_boundary_for_user(cl: boto3.client, user_name: str, policy_arn: str) -> bool:
    """
    Given some user name and a policy ARN, determine whether that policy ARN is being used as the
    permissions boundary for that user.
    """

    user_data = get_user(cl, user_name)

    # If user doesn't exist, return False
    if user_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return False

    # If user exists and they have a permissions boundary set, compare it to policy_arn
    if user_data["User"].get("PermissionsBoundary") is not None:
        return user_data["User"]["PermissionsBoundary"].get("PermissionsBoundaryArn") == policy_arn

    # If user exists and no permissions boundary is set, return False
    return False


def detach_permissions_boundary(cl: boto3.client, user_name: str) -> dict:
    return helpers.make_call_catch_err(
        cl.delete_user_permissions_boundary, UserName=user_name
    )
