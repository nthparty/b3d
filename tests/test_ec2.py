from b3d import delete_resources
from tests.aws import ec2
from tests import config


def test_instance_only(generate_tag):
    """
    Start an EC2 instance, tag it, and use the b3d delete_resources function to remove it by tag
    """

    instance_id = ec2.create_instance()
    ec2.tag_ec2_resources([instance_id], [generate_tag])
    resp = delete_resources(generate_tag["Key"], generate_tag["Value"], config.AWS_REGION, dry=False)

    assert all([r["result"] == "success" for r in resp])


def test_security_group_only(generate_tag):
    """
    Create a security group, tag it, and use the b3d delete_resources function to remove it by tag
    """

    security_group_id = ec2.create_security_group("test-security-group-only")
    ec2.tag_ec2_resources([security_group_id], [generate_tag])
    resp = delete_resources(generate_tag["Key"], generate_tag["Value"], config.AWS_REGION, dry=False)

    assert all([r["result"] == "success" for r in resp])


def test_volume_only(generate_tag):
    """
    Create a volume, tag it, and use the b3d delete_resources function to remove it by tag
    """

    volume_id = ec2.create_volume()
    ec2.tag_ec2_resources([volume_id], [generate_tag])
    resp = delete_resources(generate_tag["Key"], generate_tag["Value"], config.AWS_REGION, dry=False)

    assert all([r["result"] == "success" for r in resp])


def test_all_ec2_resources(generate_tag):
    """
    Create a security group, EC2 instance, and volume. Attach the security group and volume to the
    instance, and tag all three resources. Then, use the b3d delete_resources function to remove
    them all by tag
    """

    security_group_id = ec2.create_security_group("test-all-ec2-resources")
    instance_id = ec2.create_instance(
        SecurityGroupIds=[security_group_id]
    )

    volume_id = ec2.create_volume()
    ec2.attach_volume(instance_id, volume_id)
    ec2.tag_ec2_resources(
        [security_group_id, instance_id, volume_id], [generate_tag]
    )

    resp = delete_resources(generate_tag["Key"], generate_tag["Value"], config.AWS_REGION, dry=False)

    assert all([r["result"] == "success" for r in resp])
