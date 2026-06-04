![EC2 instance with Volume ID](image-5.png)

### Note:
Configured the Lambda function to delete snapshots older than 5 mins for test and demonstration purposes. It is not practically possible to wait for 30 days to complete this assignment.

![Lambda function](image.png)

### Lambda function code: [lambda_function.py](lambda_function.py)

![Provided EC2 permissions to the Lambda Execution IAM Role](image-4.png)

![Test event created to provide Volume ID as input](image-1.png)

![First invocation done manually](image-3.png)

![Added an EventBridge trigger to run the Lambda Function every 10 mins](image-2.png)

### Note
The initial invocations of the Lambda was not showing any input. Later realized that need to configure the input for the trigger. Once done, the Lambda execution started showing results.

![Configured the EventBridge trigger with the specified Volume ID as input](image-7.png)

![Lambda invocation happening automatically every 10 mins](image-9.png)

![Automatically created Snapshot by Lambda](image-6.png)

![CloudWatch Logs: Created new snapshot and deleted old one since it was older than 5 mins](image-8.png)