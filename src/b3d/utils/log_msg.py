

def _new_log_msg(result: str = None, err: str = None, msg: str = None):
    return {
        "result": result,
        "err": err,
        "msg": msg
    }


def log_msg_destroy(resource_type: str, resource_id: str, resp: dict) -> dict:
    """
    Produce a log message that describes the resource being deleted and whether the
    operation was successful.
    """

    log_msg = _new_log_msg()

    if resp["ResponseMetadata"]["HTTPStatusCode"] not in [200, 202, 204]:
        log_msg["result"] = "failure"
        log_msg["err"] = resp.get("Error", {})
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
    """
    Produce a log message that describes the resource being detached, the resource it is
    being detached from, and whether the operation was successful.
    """

    log_msg = _new_log_msg()
    if resp["ResponseMetadata"]["HTTPStatusCode"] not in [200, 202, 204]:
        log_msg["result"] = "failure"
        log_msg["err"] = resp.get("Error", {})
        prefix = "Unable to detach"
    else:
        log_msg["result"] = "success"
        prefix = "Successfully detached"
    log_msg["msg"] = f"{prefix} {resource_type_detached} with ID {resource_id_detached} " \
                     f"from {resource_type_detached_from} with ID {resource_id_detached_from}"

    return log_msg


def log_msg_disable(resource_type: str, resource_id: str, resp: dict):

    log_msg = _new_log_msg()
    if resp["ResponseMetadata"]["HTTPStatusCode"] not in [200, 202, 204]:
        log_msg["result"] = "failure"
        log_msg["err"] = resp.get("Error", {})
        prefix = "Unable to disable"
    else:
        log_msg["result"] = "success"
        prefix = "Successfully disabled"
    log_msg["msg"] = f"{prefix} {resource_type} with ID {resource_id}"

    return log_msg


def log_msg_unsupported_resource(resource_arn: str):
    """
    Produce a log message for a resource that this library does not currently support.
    """
    return _new_log_msg(
        result="failure",
        msg=f"Unable to delete resource with ARN {resource_arn} because "
        f"this library currently doesn't support that resource type."
    )

