from src.b3d.delete import Service
from src.b3d import aws
from src.b3d.utils import log_msg
from typing import List, Dict
import boto3


class IAM(Service):
    """
    Container class for IAM resource deletion procedures
    """

    @staticmethod
    def service_type() -> str:
        return "iam"

    class User(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "user"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.iam.get_user(
                cl, IAM.User.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def _detach_permissions_boundary(cl: boto3.client, user_name: str, dry: bool) -> Dict:
            return log_msg.log_msg_detach(
                resource_type_detached="permissions-boundary",
                resource_type_detached_from="user",
                resource_id_detached="N/A",
                resource_id_detached_from=user_name,
                resp=aws.iam.detach_permissions_boundary_from_user(cl, user_name, dry)
            )

        @staticmethod
        def _detach_all_policies(cl: boto3.client, user_name: str, dry: bool) -> List[Dict]:

            resps = []

            all_policies_attached = aws.iam.get_attached_user_policies(cl, user_name)
            for p in all_policies_attached:
                resps.append(
                    log_msg.log_msg_detach(
                        resource_type_detached="policy",
                        resource_type_detached_from="user",
                        resource_id_detached=p.get("PolicyArn", "N/A"),
                        resource_id_detached_from=user_name,
                        resp=aws.iam.detach_policy_from_user(cl, user_name, p.get("PolicyArn", ""), dry)
                    )
                )

            return resps

        @staticmethod
        def _detach_all_access_keys(cl: boto3.client, user_name: str, dry: bool) -> List[Dict]:

            resps = []

            all_access_keys_attached = aws.iam.get_user_access_keys(cl, user_name)
            for ak in all_access_keys_attached:

                delete_resp = aws.iam.delete_access_key(cl, user_name, ak.get("AccessKeyId", ""), dry)
                resps.append(
                    log_msg.log_msg_detach(
                        resource_type_detached="access-key",
                        resource_type_detached_from="user",
                        resource_id_detached=ak.get("AccessKeyId", "N/A"),
                        resource_id_detached_from=user_name,
                        resp=delete_resp
                    )
                )
                resps.append(
                    log_msg.log_msg_destroy(
                        resource_type="access-key",
                        resource_id=ak.get("AccessKeyId", "N/A"),
                        resp=delete_resp
                    )
                )

            return resps

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("iam", region_name=region)
            user_name = IAM.User.extract_resource_id_from_arn(arn)

            # Abort if this resource doesn't exist
            if not IAM.User.query(cl, arn):
                return resps

            # Remove permissions boundary for this user, if one exists
            if aws.iam.user_has_permissions_boundary(cl, user_name):
                resps.append(IAM.User._detach_permissions_boundary(cl, user_name, dry=dry))

            # Detach all policies attached to this user
            resps.extend(IAM.User._detach_all_policies(cl, user_name, dry))

            # Detach and delete all access keys associated with this user
            resps.extend(IAM.User._detach_all_access_keys(cl, user_name, dry))

            # Delete this user
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="user",
                    resource_id=arn,
                    resp=aws.iam.delete_user(cl, user_name, dry)
                )
            )

            return resps

    class Role(Service.Resource):

        @staticmethod
        def resource_type() -> str:
            return "role"

        @staticmethod
        def query(cl: boto3.client, resource_arn: str) -> bool:
            return aws.iam.get_role(
                cl, IAM.Role.extract_resource_id_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def _remove_permissions_boundary(cl: boto3.client, role_name: str, dry: bool) -> dict:
            return log_msg.log_msg_destroy(
                resource_type="role-permissions-boundary",
                resource_id=f"permissions-boundary-{role_name}",
                resp=aws.iam.delete_role_permissions_boundary(cl, role_name, dry)
            )

        @staticmethod
        def _delete_embedded_policies(cl: boto3.client, role_name: str, dry: bool) -> List[Dict]:

            resps = []
            embedded_policies = aws.iam.list_embedded_role_policies(cl, role_name)
            for policy_name in embedded_policies.get("PolicyNames", []):
                resps.append(
                    log_msg.log_msg_destroy(
                        resource_type="embedded-policy",
                        resource_id=policy_name,
                        resp=aws.iam.delete_role_policy(cl, role_name, policy_name, dry)
                    )
                )

            return resps

        @staticmethod
        def _detach_policies(cl: boto3.client, role_name: str, dry: bool) -> List[Dict]:

            resps = []
            attached_policies = aws.iam.list_attached_role_policies(cl, role_name)
            for policy in attached_policies.get("AttachedPolicies", []):
                resps.append(
                    log_msg.log_msg_detach(
                        resource_type_detached_from="role",
                        resource_type_detached="policy",
                        resource_id_detached_from=role_name,
                        resource_id_detached=policy.get("PolicyArn"),
                        resp=aws.iam.detach_role_policy(cl, role_name, policy.get("PolicyArn"), dry)
                    )
                )

            return resps

        @staticmethod
        def destroy(arn: str, region: str, dry: bool = True) -> List[Dict]:

            resps = []
            cl = boto3.client("iam", region_name=region)
            role_name = IAM.Role.extract_resource_id_from_arn(arn)

            # Abort if this resource doesn't exist
            if not IAM.Role.query(cl, arn):
                return resps

            # Remove permissions boundary from this role, if it exists
            if aws.iam.role_has_permissions_boundary(cl, role_name):
                resps.append(IAM.Role._remove_permissions_boundary(cl, role_name, dry))

            # If this role has any embedded policies, delete them
            resps.extend(IAM.Role._delete_embedded_policies(cl, role_name, dry))

            # If this role has any policies attached, detach them
            resps.extend(IAM.Role._detach_policies(cl, role_name, dry))

            # Delete this role
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="role",
                    resource_id=role_name,
                    resp=aws.iam.delete_role(cl, role_name, dry)
                )
            )

            return resps
