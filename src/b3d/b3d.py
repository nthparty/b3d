from src.b3d import aws, utils
import boto3


DELETE_PROTOCOL_OBJECT_MAP = utils.build_resource_map("src.b3d.delete")


def _get_all_resources_with_tag(tag_key: str, tag_value: str, region: str):
    """
    TODO: need to manually query User [DONE], IAM Role [DONE], & InstanceProfile resources, as they're
     not covered by the ResourceGroupsTaggingApi
    """

    ret = []

    resource_groups_tagging_client = boto3.client("resourcegroupstaggingapi", region_name=region)
    # Retrieve ARNs of all objects with the supplied name/tag pair using the ResourceGroupsTaggingApi.
    # Note that this API does not support *all* AWS resource types, so some manual ARN querying is
    # performed below.
    ret.extend(
        aws.resource_groups_tagging.get_resources_by_tag(
            resource_groups_tagging_client, tag_key, tag_value
        )
    )

    iam_client = boto3.client("iam", region_name=region)
    # Retrieve ARNs of all IAM Users with supplied key/value tag pair
    ret.extend(
        aws.iam.get_all_user_arns_with_tags(iam_client, [(tag_key, tag_value)])
    )
    # Retrieve ARNs of all IAM Roles with supplied key/value tag pair
    ret.extend(
        aws.iam.get_all_role_arns_with_tags(iam_client, [(tag_key, tag_value)])
    )

    return ret


def _parse_arn(arn: str):
    """
    Parse an ARN with the following form:
    'arn:aws:<SERVICE>:<REGION>:<ACCT_ID>:<RESOURCE_TYPE>/<RESOURCE_ID>', and
    return (<SERVICE>, <RESOURCE_TYPE>) tuples for each ARN.
    """

    splt = arn.split(":")
    return splt[2], splt[-1].split("/")[0]


def _map_arn(arn: str):
    """
    Map an ARN to its corresponding entry in DELETE_PROTOCOL_OBJECT_MAP. If it has no
    corresponding entry (i.e. - this library doesn't currently support that resource
    type), then the UnsupportedResource delete object is returned.
    """

    parsed_arn = _parse_arn(arn)
    try:
        return DELETE_PROTOCOL_OBJECT_MAP[parsed_arn[0]][parsed_arn[1]]
    except KeyError:
        return DELETE_PROTOCOL_OBJECT_MAP["unsupported-service"]["unsupported-resource"]


def _map_arns(arns: list) -> zip:
    """
    Map each ARN to its corresponding delete protocol object.
    """
    mapped_arns = [_map_arn(arn) for arn in arns]
    return zip(arns, mapped_arns)


def delete_resources(tag_key: str, tag_value: str, region: str = "us-east-1", dry=True):

    # Retrieve ARNs of all objects with the supplied name/tag pair
    resource_arns = _get_all_resources_with_tag(tag_key, tag_value, region)

    # Map each ARN to it's corresponding delete object
    mapped_arns = _map_arns(resource_arns)

    # For each resource, detach it from all dependent objects, delete it, and produce a report
    # of all performed actions, whether they were successful, and error messages for any actions
    # that were unsuccessful. Only reports with length > 0 are returned, because an empty report
    # indicates that the resource had already been deleted.
    reports = [obj.destroy(arn, region, dry) for arn, obj in mapped_arns]

    # Flatten 2D list and return it
    return [elem for reports_list in [r for r in reports if len(r) > 0] for elem in reports_list]
