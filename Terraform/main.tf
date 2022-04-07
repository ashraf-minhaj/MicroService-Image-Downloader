provider "aws" {
	profile = "${var.aws_profile}"
    region  = "${var.aws_region}"
}

terraform {
  backend "s3" {

  }
}

locals {
  resource_component = "${var.component_prefix}-${var.component_name}"
}