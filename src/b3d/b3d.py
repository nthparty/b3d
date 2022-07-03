from src.b3d import utils


DELETE_PROTOCOL_OBJECT_MAP = utils.build_resource_map("src.b3d.resources")


def delete_resources(name: str, tag: str, region: str, dry_run=True):
    """
    1. query all resources with name/tag pair, get list of arns
    2. iterate over arns list, passing each to the appropriate resource container class
    from b3d.resources, running resource.destroy() for each
    3. each destroy() function will return a list of arns, along with whether deletion / detachment
    was successful or not
    4. These lists can be parsed and written to a b3d.state file at the end
    """

    resource_arns = utils.ResourceGroupsTaggingApi.get_resources_by_tag(name, tag, region)
