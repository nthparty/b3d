"""
Utility methods for b3d tests
"""
import os
import shutil
import logging
from b3d import delete_resources
import tests.config as config
from terrorform import init, apply


logger = logging.getLogger("b3d.test")
config.configure_logger()


def cleanup_terraform_files_on_disk():
    """
    Remove on-disk terraform build artifacts
    """

    terraform_file_resources = [
        "terraform.tfstate",
        "terraform.tfstate.backup",
        ".terraform.lock.hcl"
    ]

    terraform_dir_resources = [
        ".terraform"
    ]

    for resource in terraform_file_resources:
        if os.path.exists(os.sep.join([config.TF_DEPLOYMENT_DIR, resource])):
            os.remove(os.sep.join([config.TF_DEPLOYMENT_DIR, resource]))

    for resource in terraform_dir_resources:
        if os.path.exists(os.sep.join([config.TF_DEPLOYMENT_DIR, resource])):
            shutil.rmtree(os.sep.join([config.TF_DEPLOYMENT_DIR, resource]))


def build(generate_tag, targets: list):
    """
    Use terraform to build resources from a list of targets
    """

    logger.info(f"using the following tag pair: {str(generate_tag)}")
    init(kw_args=[("-chdir", config.TF_DEPLOYMENT_DIR)])
    apply(
        kw_args=[("-chdir", config.TF_DEPLOYMENT_DIR)] +
                [("-target", t) for t in targets],
        vars_dict={
            "tag": generate_tag["Value"]
        }
    )
    logger.info(f"terraform built from the following targets: {','.join(targets)}")


def delete(tag):
    """
    Use b3d to delete all resources with the provided tag pair
    """
    return [
        r for r
        in delete_resources(
            tag["Key"], tag["Value"], config.AWS_REGION, dry=False
        )
    ]


def evaluate(resps: list, target_len: int = None):
    """
    Ensure correctness of b3d output
    """

    logger.info(f"num delete reports: {len(resps)}")
    for i, resp in enumerate(resps):
        logger.info(f"report {i}: {resp}")

    # The number of delete reports equals the target number, if one was provided
    if target_len is not None:
        assert len(resps) == target_len

    # No empty reports were returned
    assert all([len(resp) > 0 for resp in resps])
    # All resource deletion reports were successful
    assert all([r["result"] == "success" for rr in resps for r in rr])


def build_delete_evaluate(generate_tag, targets, target_len: int = None):
    """
    Build & delete targets, ensure correctness of output. The target_len argument
    defaults to None because the number of top-level reports will vary for some
    tests depending on the order in which resources get deleted.
    """

    # Build target resources
    build(generate_tag, targets)

    # Delete resources by tag and evaluate output
    resps = delete(generate_tag)
    evaluate(resps, target_len)

    # Run delete procedure again and ensure returned resource list is empty
    resps = delete(generate_tag)
    assert len(resps) == 0
