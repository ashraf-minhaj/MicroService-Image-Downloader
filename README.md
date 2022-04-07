#### Problem: Create Terrafrom Code to download profile image and store in s3 in two format.

#### This program does 
   - Gets triggered by SNS 
   - Gets message data from Sns event
   - Creates image in two size for full and thumbnail view
   - Stores both the images in private/id directory in designated bucket
   - Logs the data in between operations

### Things I did
* upload lambda code files to s3
* make that s3 object a lambda
* subscribe to SNS
* invoke by sns
* added terrafrom variables 
* Scripts
* and config files
* made some changes for naming conventions
* Added tfvars files
* added gitignore
* added lambda python file

##### Note: This repository is to demonstrate my experience in AWS, Terraform. Credentials and Crucial informations are not added. 