# Assignment 1: Automated Instance Management with AWS Lambda and Boto3

## Objective

Create an AWS Lambda function that manages EC2 instances automatically using tags.

The Lambda function should:
- stop instances tagged with `Action=Auto-Stop`
- start instances tagged with `Action=Auto-Start`

## Overview

This assignment covers:
- EC2 instance tagging
- Lambda function creation
- IAM role setup for EC2 actions
- Boto3 usage to describe, stop, and start instances
- manual testing and verification

## Setup

### 1. EC2 Instances

1. Open the EC2 dashboard.
2. Launch two instances (for example, `t2.micro`).
3. Add the tags:
   - Instance 1: `Action=Auto-Stop`
   - Instance 2: `Action=Auto-Start`

### 2. IAM Role for Lambda

1. Open the IAM dashboard.
2. Create a new role for Lambda.
3. Attach the managed policy: `AmazonEC2FullAccess`

> Note: For production, use least-privilege permissions instead of full access.

### 3. Lambda Function

1. Open the Lambda dashboard.
2. Create a new function.
3. Choose Python 3.x as the runtime.
4. Attach the IAM role created earlier.

### 4. Lambda Code Requirements

The Lambda code should:
1. Initialize a Boto3 EC2 client.
2. Describe instances filtered by tag values:
   - `Action=Auto-Stop`
   - `Action=Auto-Start`
3. Stop the instances with `Action=Auto-Stop`.
4. Start the instances with `Action=Auto-Start`.
5. Log the affected instance IDs or names.

## Testing

1. Save the Lambda function.
2. Manually invoke the function.
3. Verify in the EC2 console that:
   - the `Auto-Stop` instance has stopped,
   - the `Auto-Start` instance has started.

## Verification

- Confirm the Lambda execution succeeds.
- Check CloudWatch logs for the instance actions.
- Verify EC2 instance state changes in the console.
