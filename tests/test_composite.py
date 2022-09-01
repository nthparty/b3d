"""
For each test function below, a tag pair and a list of composite resource
targets are provided. These resources are constructed by terraform before being
deleted by b3d according to their tag. The output from b3d is then checked for
correctness
"""
import pytest
import tests.utils as utils


@pytest.fixture(
    params=[
        [
            "aws_instance.instance_composite",
            "aws_ebs_volume.volume_composite",
            "aws_security_group.security_group_composite",
            "aws_volume_attachment.volume_composite_attach"
        ]
    ]
)
def targets_ec2_composite(request):
    """
    Return a list of EC2 target resource(s) to be constructed & deleted by b3d
    """
    return request.param


def test_ec2_composite(generate_tag, targets_ec2_composite):
    utils.build_delete_evaluate(generate_tag, targets_ec2_composite)
