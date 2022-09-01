variable "tag" {
  default       = "b3d-test"
}

variable "availability_zone" {
  description   = "availability zone for resources created by tests"
  default = "us-east-1a"
}

variable "test_ami_id" {
  description   = "ID of AMI to use for EC2 instance tests"
  default = "ami-0c4cfe9aec8b21224"
}

variable "region" {
  default       = "us-east-1"
}