

def log_msg_destroy(resource_type: str, resource_id: str, resp: dict) -> dict:

    log_msg = {}
    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        log_msg["result"] = "failure"
        log_msg["err"] = resp["Error"]
        prefix = "Unable to delete"
    else:
        log_msg["result"] = "success"
        prefix = "Successfully deleted"
    log_msg["msg"] = f"{prefix} {resource_type} with ID {resource_id}"

    return log_msg


def log_msg_detach(
        resource_type_detached_from: str, resource_type_detached: str,
        resource_id_detached_from: str, resource_id_detached: str,
        resp: dict
) -> dict:

    log_msg = {}
    if resp["ResponseMetadata"]["HTTPStatusCode"] != 200:
        log_msg["result"] = "failure"
        log_msg["err"] = resp["Error"]
        prefix = "Unable to detach"
    else:
        log_msg["result"] = "success"
        prefix = "Successfully detached"
    log_msg["msg"] = f"{prefix} {resource_type_detached} with ID {resource_id_detached} " \
                     f"from {resource_type_detached_from} with ID {resource_id_detached_from}"

    return log_msg


def log_msg_unsupported_resource(resource_arn: str):
    return {
        "result": "failure",
        "msg":
            f"Unable to delete resource with ARN {resource_arn} because "
            f"this library currently doesn't support that resource type."
    }
