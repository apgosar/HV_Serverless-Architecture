<p align="center">
  <img src="image.png" alt="Old file uploaded to S3 bucket" />
  <br />
  <em>Old file uploaded to S3 bucket</em>
</p>

<p align="center">
    <img src="image-2.png" alt="Lambda function code" />
    <br />
    <em>Lambda function code</em>
</p>

### Lambda function code: [lambda_function.py](lambda_function.py)

<p align="center">
    <img src="image-3.png" alt="Adding S3 access Permission policy to Lambda Execution IAM Role" />
    <br />
    <em>Adding S3 access Permission policy to Lambda Execution IAM Role</em>
</p>

### Note:
There is no way to upload a file which AWS will consider as 30 days old. So I kept the timeout as 5 mins so that I can run the Lambda function and it will delete the file older than 5 mins.

<p align="center">
    <img src="image-1.png" alt="Lambda manual invocation" />
    <br />
    <em>Lambda manual invocation</em>
</p>

<p align="center">
    <img src="image-5.png" alt="Old file deleted from S3 bucket after Lambda execution" />
    <br />
    <em>Old file deleted from S3 bucket after Lambda execution</em>
</p>

<p align="center">
    <img src="image-4.png" alt="CloudWatch Logs" />
    <br />
    <em>CloudWatch Logs</em>
</p>