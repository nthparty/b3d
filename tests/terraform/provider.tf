provider "aws" {
  profile       = "default"
  region        = var.region
  default_tags {
    tags = {
      Name = var.tag
    }
  }
}