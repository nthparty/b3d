"""
IAM helper functions
"""
from typing import List, Dict, Tuple
import boto3
import b3q
from b3d.aws import helpers


@helpers.attempt_api_call_multiple_times
def delete_policy(cl: boto3.client, policy_arn: str, dry: bool) -> dict:
    """
    Delete a policy
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_policy, PolicyArn=policy_arn
    )


def get_policy(cl: boto3.client, policy_arn: str) -> dict:
    """
    Describe a policy, if it exists
    """

    resp = helpers.make_call_catch_err(cl.get_policy, PolicyArn=policy_arn)
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def get_all_policies(cl: boto3.client, scope: str = "Local", prefix: str = "/"):
    """
    Get all policies in some region
    """
    return list(b3q.get(
        cl.list_policies, attribute="Policies", arguments={"PathPrefix": prefix, "Scope": scope}
    ))


def policy_has_tags(cl: boto3.client, policy_arn: str, tags: List[Tuple]) -> bool:
    """
    Determine whether a policy is associated with any in some list of tag pairs
    """

    policy_data = get_policy(cl, policy_arn)
    if policy_data is None:
        return False

    for tag_key, tag_value in tags:
        for t in policy_data["Policy"].get("Tags", []):

            if t["Key"] == tag_key and t["Value"] == tag_value:
                return True

    return False


def get_all_policy_arns_with_tags(cl: boto3.client, tags: List[Tuple]) -> List[str]:
    """
    Get all policies associated with this AWS account that at least one tag from <tags>
    is attached to
    """

    ret = []
    all_policies = get_all_policies(cl)
    for p in all_policies:

        policy_arn = p.get("Arn", None)
        if policy_arn is not None:
            if policy_has_tags(cl, policy_arn, tags):
                ret.append(policy_arn)

    return ret


def list_entities_policy_attached(cl: boto3.client, policy_arn: str) -> dict:
    """
    List all resources that are associated with some policy ARN
    """
    return helpers.make_call_catch_err(
        cl.list_entities_for_policy, PolicyArn=policy_arn
    )


def list_policy_versions(cl: boto3.client, policy_arn: str) -> dict:
    """
    List all versions for a policy
    """
    return helpers.make_call_catch_err(
        cl.list_policy_versions, PolicyArn=policy_arn
    )


@helpers.attempt_api_call_multiple_times
def delete_policy_version(cl: boto3.client, policy_arn: str, version_id: str, dry: bool) -> dict:
    """
    Delete a version of a policy
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_policy_version, PolicyArn=policy_arn, VersionId=version_id
    )


@helpers.attempt_api_call_multiple_times
def delete_role(cl: boto3.client, role_name: str, dry: bool) -> dict:
    """
    Delete a role
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_role, RoleName=role_name
    )


@helpers.attempt_api_call_multiple_times
def delete_role_permissions_boundary(cl: boto3.client, role_name: str, dry: bool) -> dict:
    """
    Delete the permissions boundary assocatied with some role, if it exists
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_role_permissions_boundary, RoleName=role_name
    )


@helpers.attempt_api_call_multiple_times
def delete_role_policy(cl: boto3.client, role_name: str, policy_name: str, dry: bool) -> dict:
    """
    Delete an inline policy from a role
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_role_policy, RoleName=role_name, PolicyName=policy_name
    )


@helpers.attempt_api_call_multiple_times
def detach_role_policy(cl: boto3.client, role_name: str, policy_arn: str, dry: bool) -> dict:
    """
    Detach a policy from a role
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.detach_role_policy, RoleName=role_name, PolicyArn=policy_arn
    )


def get_role(cl: boto3.client, role_name: str) -> dict:
    """
    Describe a role, if it exists
    """

    resp = helpers.make_call_catch_err(cl.get_role, RoleName=role_name)
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def get_all_roles(cl: boto3.client, prefix: str = "/") -> List[Dict]:
    """
    List all roles associated with this AWS account
    """
    return list(b3q.get(
        cl.list_roles, attribute="Roles", arguments={"PathPrefix": prefix}
    ))


def role_has_permissions_boundary(cl: boto3.client, role_name: str) -> bool:
    """
    Determine whether a role has a permissions boundary
    """

    role_data = get_role(cl, role_name)
    if role_data is not None:
        # If this role has a nonempty permissions boundary, there will be a
        # "PermissionsBoundary" key present in its object record
        return role_data["Role"].get("PermissionsBoundary") is not None

    return False


def list_embedded_role_policies(cl: boto3.client, role_name: str):
    """
    List all inline policies for a role
    """
    return helpers.make_call_catch_err(
        cl.list_role_policies, RoleName=role_name
    )


def list_attached_role_policies(cl: boto3.client, role_name: str):
    """
    List all attached policies for a role
    """
    return helpers.make_call_catch_err(
        cl.list_attached_role_policies, RoleName=role_name
    )


def role_has_tags(cl: boto3.client, role_name: str, tags: List[Tuple]) -> bool:
    """
    Determine whether any in some list of tag key / value pairs is associated with
    some role
    """

    role_data = get_role(cl, role_name)
    if role_data is None:
        return False

    for tag_key, tag_value in tags:
        for t in role_data["Role"].get("Tags", []):

            # For Role resources, tag key is always a single string (not a list)
            if t["Key"] == tag_key and t["Value"] == tag_value:
                return True

    return False


def get_all_role_arns_with_tags(cl: boto3.client, tags: List[Tuple]) -> List[str]:
    """
    Return the ARNs of all roles that have at least one tag from the tags list
    """

    ret = []
    all_roles = get_all_roles(cl)
    for r in all_roles:

        role_name = r.get("RoleName", None)
        if role_name is not None:
            if role_has_tags(cl, role_name, tags):
                ret.append(r.get("Arn"))

    return ret


@helpers.attempt_api_call_multiple_times
def delete_instance_profile(cl: boto3.client, instance_profile_name: str, dry: bool) -> dict:
    """
    Delete an instance profile
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_instance_profile, InstanceProfileName=instance_profile_name
    )


@helpers.attempt_api_call_multiple_times
def delete_access_key(cl: boto3.client, user_name: str, access_key_id: str, dry: bool) -> dict:
    """
    Delete an access key pair associated with an IAM user
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_access_key, UserName=user_name, AccessKeyId=access_key_id
    )


def get_instance_profile(cl: boto3.client, instance_profile_name: str) -> dict:
    """
    Describe an instance profile, if it exists
    """

    resp = helpers.make_call_catch_err(cl.get_instance_profile, InstanceProfileName=instance_profile_name)
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


def get_attached_user_policies(cl: boto3.client, user_name: str) -> List[Dict]:
    """
    List all policies attached to a user
    """

    resp = helpers.make_call_catch_err(
        cl.list_attached_user_policies, UserName=user_name
    )
    return [] if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp.get("AttachedPolicies", [])


def get_inline_user_policies(cl: boto3.client, user_name: str) -> List[str]:
    """
    List all inline policies attached to a user
    """

    resp = helpers.make_call_catch_err(
        cl.list_user_policies, UserName=user_name
    )
    return [] if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp.get("PolicyNames", [])


def get_user_access_keys(cl: boto3.client, user_name: str) -> List[Dict]:
    """
    List all access keys associated with a user
    """
    resp = helpers.make_call_catch_err(
        cl.list_access_keys, UserName=user_name
    )
    return [] if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp.get("AccessKeyMetadata", [])


def get_all_users(cl: boto3.client) -> List[Dict]:
    """
    List all users for this AWS account
    """
    return list(b3q.get(
        cl.list_users, attribute="Users"
    ))


@helpers.attempt_api_call_multiple_times
def delete_user(cl: boto3.client, user_name: str, dry: bool) -> dict:
    """
    Delete a user
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_user, UserName=user_name
    )


def get_user(cl: boto3.client, user_name: str) -> dict:
    """
    Describe a user, if it exists
    """

    resp = helpers.make_call_catch_err(
        cl.get_user, UserName=user_name
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


@helpers.attempt_api_call_multiple_times
def detach_policy_from_user(cl: boto3.client, user_name: str, policy_arn: str, dry: bool):
    """
    Detach a policy from a user
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.detach_user_policy, UserName=user_name, PolicyArn=policy_arn
    )


@helpers.attempt_api_call_multiple_times
def delete_inline_user_policy(cl: boto3.client, user_name: str, policy_name: str, dry: bool) -> dict:
    """
    Delete an inline policy for some user
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_user_policy, UserName=user_name, PolicyName=policy_name
    )


def user_has_permissions_boundary(cl: boto3.client, user_name: str) -> bool:
    """
    Determine whether a permissions boundary exists for a user
    """

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


def policy_is_permissions_boundary_for_role(cl: boto3.client, role_name: str, policy_arn: str) -> bool:
    """
    Given some role name and a policy ARN, determine whether that policy ARN is being used as the
    permissions boundary for that role.
    """

    role_data = get_role(cl, role_name)

    # If role doesn't exist, return False
    if role_data["ResponseMetadata"]["HTTPStatusCode"] != 200:
        return False

    # If role exists and it has a permissions boundary set, compare it to policy_arn
    if role_data["Role"].get("PermissionsBoundary") is not None:
        return role_data["Role"]["PermissionsBoundary"].get("PermissionsBoundaryArn") == policy_arn

    # If role exists and no permissions boundary is set, return False
    return False


@helpers.attempt_api_call_multiple_times
def delete_user_permissions_boundary(cl: boto3.client, user_name: str, dry: bool) -> dict:
    """
    Delete a permissions boundary from a user
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_user_permissions_boundary, UserName=user_name
    )


def user_has_tags(cl: boto3.client, user_name: str, tags: List[Tuple]) -> bool:
    """
    Determine whether any in some list of tag key / value pairs is associated with
    some user profile
    """

    user_data = get_user(cl, user_name)
    if user_data is None:
        return False

    for tag_key, tag_value in tags:
        for t in user_data["User"].get("Tags", []):

            # For User resources, tag key is always a single string (not a list)
            if t["Key"] == tag_key and t["Value"] == tag_value:
                return True

    return False


def get_all_user_arns_with_tags(cl: boto3.client, tags: List[Tuple]) -> List[str]:
    """
    Return the ARNs of all users that have at least one tag from the tags list
    """

    ret = []
    all_users = get_all_users(cl)
    for u in all_users:

        user_name = u.get("UserName", None)
        if user_name is not None:
            if user_has_tags(cl, user_name, tags):
                ret.append(u.get("Arn"))

    return ret


@helpers.attempt_api_call_multiple_times
def detach_policy_from_group(cl: boto3.client, group_name: str, policy_arn: str, dry: bool):
    """
    Detach a policy from a group
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.detach_group_policy, GroupName=group_name, PolicyArn=policy_arn
    )
