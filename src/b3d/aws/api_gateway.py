from b3d.aws import helpers
import boto3
import b3q


def get_rest_api(cl: boto3.client, api_id: str):

    resp = helpers.make_call_catch_err(
        cl.get_rest_api, restApiId=api_id
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


@helpers.attempt_api_call_multiple_times
def delete_rest_api(cl: boto3.client, api_id: str, dry: bool):
    """
    TODO: create custom waiter for something like RestApiTerminated
     Could just call cl.get_rest_apis() until api_id is not in the
     returned object list
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_rest_api, restApiId=api_id
    )


def get_base_path_mappings(cl: boto3.client, rest_api_id: str, stage_name: [str, None] = None):
    """
    Get all base path mappings associated with some rest api, and optionally a stage within
    that rest api
    """

    mappings = []
    constraints = {
        "restApiId": rest_api_id
    }
    if stage_name is not None:
        constraints["stage"] = stage_name

    domains = get_custom_domain_names(cl)
    for domain in [item["domainName"] for item in domains]:
        for item in b3q.get(
            cl.get_base_path_mappings,
            arguments={"domainName": domain},
            constraints=constraints
        ):
            mappings.append({
                "domain": domain,
                "base_path": item.get("basePath")
            })

    return mappings


@helpers.attempt_api_call_multiple_times
def delete_base_path_mapping(cl: boto3.client, domain_name: str, base_path: str, dry: bool):
    """
    TODO: create custom waiter for BasePathMappingDeleted, could call
     cl.get_base_path_mappings until base_path is not in returned object
     list
    """

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_base_path_mapping, domainName=domain_name, basePath=base_path
    )


def get_usage_plan(cl: boto3.client, usage_plan_id: str):

    resp = helpers.make_call_catch_err(
        cl.get_usage_plan, usagePlanId=usage_plan_id
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


@helpers.attempt_api_call_multiple_times
def delete_usage_plan(cl: boto3.client, usage_plan_id: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_usage_plan, usagePlanId=usage_plan_id
    )


@helpers.attempt_api_call_multiple_times
def delete_stage(cl: boto3.client, rest_api_id: str, stage_name: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_stage, restApiId=rest_api_id, stageName=stage_name
    )


def get_custom_domain_names(cl: boto3.client):
    return list(b3q.get(cl.get_domain_names))


def get_api_key(cl: boto3.client, api_key_id: str, include_value: bool = True):

    resp = helpers.make_call_catch_err(
        cl.get_api_key, apiKey=api_key_id, includeValue=include_value
    )
    return None if resp["ResponseMetadata"]["HTTPStatusCode"] != 200 else resp


@helpers.attempt_api_call_multiple_times
def delete_api_key(cl: boto3.client, api_key_id: str, dry: bool):

    if dry:
        return helpers.dry_run_success_resp()

    return helpers.make_call_catch_err(
        cl.delete_api_key, apiKey=api_key_id
    )
