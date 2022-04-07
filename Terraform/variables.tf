variable "aws_region" {
}

variable "aws_account_id" {
}

variable "resource_prefix" {
}

variable "aws_profile" {
}

variable "env" {
}


variable "component_prefix" {
  default = "company-name"
}

variable "component_name" {
  default = "microservice-name"
}

# store the zip file here
variable "s3_bucket" {
}

variable "s3_key" {
  default     = "lambda/media-processor.zip"
  description = "Store zip file in this bucket path"
}

variable "archive_file_type" {
  default = "zip"
}

variable "lambda_handler" {
  default = "image_downloader"
}

variable "lambda_runtime" {
  default = "python3.7"
}

variable "lambda_timeout" {
  default = "15"
}

variable "sns_topic" {
}
