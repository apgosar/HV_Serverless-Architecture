<p align="center">
    <img src="image-5.png" alt="EC2 instance with Volume ID" />
    <br />
    <em>EC2 instance with Volume ID</em>
</p>

### Note:
Configured the Lambda function to delete snapshots older than 5 mins for test and demonstration purposes. It is not practically possible to wait for 30 days to complete this assignment.

<p align="center">
    <img src="image.png" alt="Lambda function" />
    <br />
    <em>Lambda function</em>
</p>

### Lambda function code: [lambda_function.py](lambda_function.py)

<p align="center">
    <img src="image-4.png" alt="Provided EC2 permissions to the Lambda Execution IAM Role" />
    <br />
    <em>Provided EC2 permissions to the Lambda Execution IAM Role</em>
</p>

<p align="center">
    <img src="image-1.png" alt="Test event created to provide Volume ID as input" />
    <br />
    <em>Test event created to provide Volume ID as input</em>
</p>

<p align="center">
    <img src="image-3.png" alt="First invocation done manually" />
    <br />
    <em>First invocation done manually</em>
</p>

<p align="center">
    <img src="image-2.png" alt="Added an EventBridge trigger to run the Lambda Function every 10 mins" />
    <br />
    <em>Added an EventBridge trigger to run the Lambda Function every 10 mins</em>
</p>

### Note
The initial invocations of the Lambda was not showing any input. Later realized that need to configure the input for the trigger. Once done, the Lambda execution started showing results.

<p align="center">
    <img src="image-7.png" alt="Configured the EventBridge trigger with the specified Volume ID as input" />
    <br />
    <em>Configured the EventBridge trigger with the specified Volume ID as input</em>
</p>

<p align="center">
    <img src="image-9.png" alt="Lambda invocation happening automatically every 10 mins" />
    <br />
    <em>Lambda invocation happening automatically every 10 mins</em>
</p>

<p align="center">
    <img src="image-6.png" alt="Automatically created Snapshot by Lambda" />
    <br />
    <em>Automatically created Snapshot by Lambda</em>
</p>

<p align="center">
    <img src="image-8.png" alt="CloudWatch Logs: Created new snapshot and deleted old one since it was older than 5 mins" />
    <br />
    <em>CloudWatch Logs: Created new snapshot and deleted old one since it was older than 5 mins</em>
</p>