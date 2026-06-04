import boto3
from datetime import datetime, timedelta
import json

def lambda_handler(event, context):
    """
    Lambda function to manage EBS snapshots:
    - Create a snapshot for a specified EBS volume
    - List and delete snapshots older than 30 days (5 minutes for testing purposes)
    """
    # Initialize boto3 EC2 client
    ec2_client = boto3.client('ec2')
    
    created_snapshots = []
    deleted_snapshots = []
    
    try:
        # Get the volume ID from the event or use a default
        volume_id = event.get('volume_id', None)
        
        if not volume_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Error: volume_id is required in the event'
                })
            }
        
        print(f"Processing snapshots for volume: {volume_id}")
        
        # Step 1: Create a snapshot for the specified EBS volume
        print(f"\nStep 1: Creating snapshot for volume {volume_id}...")
        try:
            snapshot_response = ec2_client.create_snapshot(
                VolumeId=volume_id,
                Description=f'Automated snapshot created by Lambda at {datetime.now().isoformat()}'
            )
            snapshot_id = snapshot_response['SnapshotId']
            created_snapshots.append(snapshot_id)
            print(f"✓ Snapshot created successfully: {snapshot_id}")
        except Exception as e:
            print(f"✗ Error creating snapshot: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': f'Error creating snapshot: {str(e)}'
                })
            }
        
        # Step 2: List snapshots for this volume and delete those older than 30 days (5 mins for testing)
        print(f"\nStep 2: Listing snapshots for volume {volume_id}...")
        try:
            snapshots_response = ec2_client.describe_snapshots(
                Filters=[
                    {
                        'Name': 'volume-id',
                        'Values': [volume_id]
                    }
                ]
            )
            snapshots = snapshots_response['Snapshots']
            print(f"Total snapshots found for this volume: {len(snapshots)}")
            
            # Calculate the time 5 minutes ago
            five_mins_ago = datetime.now(snapshots[0]['StartTime'].tzinfo) - timedelta(minutes=5)
            
            # Check each snapshot
            for snapshot in snapshots:
                snapshot_id = snapshot['SnapshotId']
                start_time = snapshot['StartTime']
                
                if start_time < five_mins_ago:
                    try:
                        ec2_client.delete_snapshot(SnapshotId=snapshot_id)
                        deleted_snapshots.append(snapshot_id)
                        print(f"✓ Deleted old snapshot: {snapshot_id} (created: {start_time})")
                    except Exception as e:
                        print(f"✗ Error deleting snapshot {snapshot_id}: {str(e)}")
                else:
                    print(f"  Snapshot {snapshot_id} is recent (created: {start_time}), keeping it")
        
        except Exception as e:
            print(f"✗ Error listing or deleting snapshots: {str(e)}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'message': f'Error managing snapshots: {str(e)}'
                })
            }
        
        # Step 3: Print summary
        print("\n" + "="*60)
        print("SUMMARY - EBS Snapshot Management:")
        print("="*60)
        print(f"Created Snapshots: {len(created_snapshots)}")
        for snapshot_id in created_snapshots:
            print(f"  + {snapshot_id}")
        
        print(f"\nDeleted Snapshots (older than 5 minutes): {len(deleted_snapshots)}")
        for snapshot_id in deleted_snapshots:
            print(f"  - {snapshot_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'EBS snapshot management completed successfully',
                'volume_id': volume_id,
                'created_snapshots': created_snapshots,
                'deleted_snapshots': deleted_snapshots,
                'total_created': len(created_snapshots),
                'total_deleted': len(deleted_snapshots)
            })
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': f'Error during EBS snapshot management: {str(e)}'
            })
        }
