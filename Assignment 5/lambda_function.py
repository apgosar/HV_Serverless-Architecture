import boto3
from datetime import datetime
import json


def lambda_handler(event, context):
    """Lambda handler to tag a newly launched EC2 instance."""
    ec2_client = boto3.client('ec2')

    # Retrieve the instance ID from the event payload.
    #instance_id = event{'detail'}{'instance-id'}
    instance_id = event.get('detail', {}).get('instance-id')
    
    if not instance_id:
        # Common EventBridge payload shape for EC2 launch events
        instance_id = event.get('detail', {}).get('instance-id')

    if not instance_id:
        message = 'Error: instance ID not found in event payload.'
        print(message)
        return {
            'statusCode': 400,
            'body': json.dumps({'message': message})
        }

    current_date = datetime.utcnow().strftime('%Y-%m-%d')
    custom_tag_value = 'LambdaAutoTagged'

    tags = [
        {'Key': 'LaunchDate', 'Value': current_date},
        {'Key': 'TagOwner', 'Value': custom_tag_value}
    ]

    try:
        ec2_client.create_tags(
            Resources=[instance_id],
            Tags=tags
        )

        message = (
            f"Tagged EC2 instance {instance_id} with LaunchDate={current_date} "
            f"and TagOwner={custom_tag_value}."
        )
        print(message)

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': message,
                'instance_id': instance_id,
                'tags': tags
            })
        }

    except Exception as e:
        error_message = f"Failed to tag instance {instance_id}: {str(e)}"
        print(error_message)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': error_message})
        }