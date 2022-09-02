data "aws_vpc" "default_vpc" {
  default           = true
}

resource "aws_instance" "instance_simple" {
  ami               = var.test_ami_id
  instance_type     = "t2.micro"
}

resource "aws_ebs_volume" "volume_simple" {
  availability_zone = var.availability_zone
  size              = 1
}

resource "aws_security_group" "security_group_simple" {
  name              = "security_group_simple"
  vpc_id            = data.aws_vpc.default_vpc.id
}

resource "aws_instance" "instance_composite" {
  ami               = var.test_ami_id
  instance_type     = "t2.micro"
  security_groups   = [aws_security_group.security_group_composite.name]
  availability_zone = var.availability_zone
}

resource "aws_ebs_volume" "volume_composite" {
  availability_zone = var.availability_zone
  size              = 1
}

resource "aws_security_group" "security_group_composite" {
  name              = "security_group_composite"
  vpc_id            = data.aws_vpc.default_vpc.id

  ingress {
    description      = "TLS from VPC"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
}

resource "aws_volume_attachment" "volume_composite_attach" {
  device_name       = "/dev/sdh"
  volume_id         = aws_ebs_volume.volume_composite.id
  instance_id       = aws_instance.instance_composite.id
}