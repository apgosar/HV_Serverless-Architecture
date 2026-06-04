# Assignment 4
Automatic EBS Snapshot and Cleanup Using AWS Lambda and Boto3

## Objective
To automate the backup process for your EBS volumes and ensure that backups older than a specified retention period are cleaned up to save costs.

## Task 
Automate the creation of snapshots for specified EBS volumes and clean up snapshots older than 30 days.

## Instructions

1. EBS Setup:
   - Navigate to the EC2 dashboard and identify or create an EBS volume you wish to back up.
   - Note down the volume ID.

2. Lambda IAM Role:
   - In the IAM dashboard, create a new role for Lambda.
   - Attach policies that allow Lambda to create EBS snapshots and delete them (`AmazonEC2FullAccess` for simplicity, but be more restrictive in real-world scenarios).

3. Lambda Function:
   - Navigate to the Lambda dashboard and create a new function.
   - Choose Python 3.x as the runtime.
   - Assign the IAM role created in the previous step.
   - Write the Boto3 Python script to:
     1. Initialize a boto3 EC2 client.
     2. Create a snapshot for the specified EBS volume.
     3. List snapshots and delete those older than 30 days.
     4. Print the IDs of the created and deleted snapshots for logging purposes.

4. Event Source (Bonus):
   - Attach an event source, like Amazon CloudWatch Events, to trigger the Lambda function at your desired backup frequency (e.g., every week).

5. Manual Invocation:
   - After saving your function, either manually trigger it or wait for the scheduled event.
   - Go to the EC2 dashboard and confirm that the snapshot is created and old snapshots are deleted.