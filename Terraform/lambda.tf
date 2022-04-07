# Zip the Lamda function on the fly
data "archive_file" "source" {
  type        = "${var.archive_file_type}"
  source_dir  = "../files/"
  output_path = "../output-files/--.zip"
}

# upload zip to s3 and then update lamda function from s3
resource "aws_s3_bucket_object" "s3_bucket" {
  bucket = "${var.s3_bucket}"
  key    = "${var.s3_key}"
  source = data.archive_file.source.output_path
}

# connect this lambda with uploaded s3 zip file
# lambda needs code and iam_role
# "${aws_s3_bucket_object.file_upload.key}"
# resource - resource_name
resource "aws_lambda_function" "lambda" {
    function_name   = "${var.component_prefix}-${var.component_name}"
    s3_bucket       = aws_s3_bucket_object.s3_bucket.bucket
    s3_key          = aws_s3_bucket_object.s3_bucket.key
    role            = aws_iam_role.lambda_role.arn 
    handler         = "${var.component_prefix}-${var.component_name}.${var.lambda_handler}"
    runtime         = "${var.lambda_runtime}"
	timeout			= "${var.lambda_timeout}"
}

# subscribe lambda to sns topic
resource "aws_sns_topic_subscription" "sns" {
  topic_arn = "arn:aws:sns:${var.aws_region}:${var.aws_account_id}:${var.sns_topic}"
  protocol  = "lambda"
  endpoint  = aws_lambda_function.lambda.arn
}

# give permission to be invoked by sns
resource "aws_lambda_permission" "lambda_sns_invoke_permission" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic_subscription.sns.topic_arn
}
