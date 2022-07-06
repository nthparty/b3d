from src.b3d import utils


DELETE_PROTOCOL_OBJECT_MAP = utils.build_resource_map("src.b3d.delete")


def _parse_arn(arn: str, region: str):
    """
    Parse an ARN with the following form:
    'arn:aws:<SERVICE>:<REGION>:<ACCT_ID>:<RESOURCE_TYPE>/<RESOURCE_ID>', and
    return (<SERVICE>, <RESOURCE_TYPE>) tuples for each ARN whose <REGION> value
    is either empty (global) or matches 'region'.
    """

    splt = arn.split(":")
    return (splt[2], splt[-1].split("/")[0]) if splt[3] == "" or splt[3] == region else None


def map_arns(arns: list, region: str) -> zip:
    """
    Map each ARN to its corresponding delete protocol object
    """

    parsed_arns = [_parse_arn(a, region) for a in arns if _parse_arn(a, region) is not None]
    return zip(arns, [DELETE_PROTOCOL_OBJECT_MAP[pa[0]][pa[1]] for pa in parsed_arns])


def delete_resources(name: str, tag: str, region: str, dry_run=True):

    resource_arns = utils.ResourceGroupsTaggingApi.get_resources_by_tag(name, tag, region)
    mapped_arns = map_arns(resource_arns, region)
    state_reports = [obj.destroy(arn, name, tag, region) for arn, obj in mapped_arns]
