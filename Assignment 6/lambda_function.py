import boto3
from datetime import datetime, timedelta
import json


def lambda_handler(event, context):
    """Lambda function to monitor AWS billing using Cost Explorer and send an SNS alert."""
    ce = boto3.client('ce', region_name='us-east-1')
    sns = boto3.client('sns')

    threshold = float(event.get('threshold', 0.01))
    email_address = event.get('email', 'ankur.gosar@gmail.com')
    topic_name = event.get('sns_topic_name', 'BillingAlertsTopic')

    now = datetime.utcnow().date()
    start_date = (now - timedelta(days=7)).isoformat()
    end_date = now.isoformat()

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['UnblendedCost']
        )

        results_by_time = response.get('ResultsByTime', [])
        if not results_by_time:
            message = 'No Cost Explorer data available for the last 7 days.'
            print(message)
            return {
                'statusCode': 200,
                'body': json.dumps({
                    'message': message,
                    'threshold': threshold,
                    'billing_amount': 0.0,
                    'alert_sent': False
                })
            }

        total_cost = sum(
            float(day['Total'].get('UnblendedCost', {}).get('Amount', '0'))
            for day in results_by_time
        )
        latest_cost = float(
            results_by_time[-1]['Total'].get('UnblendedCost', {}).get('Amount', '0')
        )

        print(f"Retrieved billing amount from Cost Explorer: total=${total_cost:.4f}, latest_day=${latest_cost:.4f}")

        alert_sent = False
        notification_message = ''

        if total_cost > threshold:
            print(f"Threshold exceeded: total=${total_cost:.4f} > ${threshold:.4f}")

            topic_response = sns.create_topic(Name=topic_name)
            topic_arn = topic_response['TopicArn']
            print(f"Using SNS topic: {topic_arn}")

            try:
                sns.subscribe(
                    TopicArn=topic_arn,
                    Protocol='email',
                    Endpoint=email_address
                )
                print(f"Subscription request sent to {email_address}. Confirm the subscription in email.")
            except Exception as sub_exc:
                print(f"Warning: could not subscribe email address: {sub_exc}")

            notification_message = (
                f"AWS billing alert: total cost over the last 7 days is ${total_cost:.4f}, "
                f"which exceeds threshold ${threshold:.4f}."
            )

            sns.publish(
                TopicArn=topic_arn,
                Subject='AWS Billing Alert',
                Message=notification_message
            )
            print(f"SNS notification published to topic {topic_arn}")
            alert_sent = True
        else:
            print(f"Billing amount is below threshold: total=${total_cost:.4f} <= ${threshold:.4f}")
            notification_message = 'Threshold not exceeded. No SNS notification sent.'

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': notification_message,
                'billing_amount': total_cost,
                'latest_day_cost': latest_cost,
                'threshold': threshold,
                'alert_sent': alert_sent,
                'email': email_address
            })
        }

    except Exception as e:
        error_message = f"Error checking billing via Cost Explorer or sending notification: {str(e)}"
        print(error_message)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': error_message})
        }
