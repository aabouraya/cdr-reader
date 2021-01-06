Serverless POC
==============

this is a POC `Not A Real Business Case` to demonstrate the capabilities of serverless architecture using serverless framework and AWS cloud
provider

----------

###POC Scenario

- User upload a cdr (Call Details Record) file to S3 bucket.
- S3 trigger an asynchronous event when a new Object is created in the bucket, this even start to execute `parse_cdr`
  lambda function.
- `parse_cdr` lambda function load the file from the `S3` bucket, read the file line by line , extracts a specific fields from the line and
  send it as a message to `SQS`.
  that means if the cdr file contains 100 line , the lambda function will send 100 message to the `SQS`
- `aggregate_cdrs` lambda function is starts to poll the new message from the `SQS`and save the record in a `DynamoDB` table.


