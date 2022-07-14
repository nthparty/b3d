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
                cl, IAM.User.extract_resource_name_from_arn(resource_arn)
            ) is not None

        @staticmethod
        def _detach_permissions_boundary(cl: boto3.client, user_name: str, dry: bool = True) -> Dict:
            return log_msg.log_msg_detach(
                resource_type_detached="permissions-boundary",
                resource_type_detached_from="user",
                resource_id_detached="N/A",
                resource_id_detached_from=user_name,
                resp=aws.iam.detach_permissions_boundary_from_user(cl, user_name, dry)
            )

        @staticmethod
        def _detach_all_policies(cl: boto3.client, user_name: str, dry: bool = True) -> List[Dict]:

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
        def _detach_all_access_keys(cl: boto3.client, user_name: str, dry: bool = True) -> List[Dict]:

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
            user_name = IAM.User.extract_resource_name_from_arn(arn)

            # Abort if this resource doesn't exist
            if not IAM.User.query(cl, arn):
                return resps

            # Remove permissions boundary for this user, if one exists
            if aws.iam.user_has_permissions_boundary(cl, user_name):
                resps.append(IAM.User._detach_permissions_boundary(cl, user_name))

            # Detach all policies attached to this user
            resps.extend(IAM.User._detach_all_policies(cl, user_name))

            # Detach and delete all access keys associated with this user
            resps.extend(IAM.User._detach_all_access_keys(cl, user_name))

            # Delete this user
            resps.append(
                log_msg.log_msg_destroy(
                    resource_type="user",
                    resource_id=arn,
                    resp=aws.iam.delete_user(cl, user_name, dry)
                )
            )

            return resps
