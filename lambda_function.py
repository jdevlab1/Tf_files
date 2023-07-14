import boto3
import datetime

def is_after_hours(received_time):
    # Check if the received time is after business hours (5:00 pm - 8:00 am CT)
    start_time = datetime.time(8, 0)  # 8:00 am
    end_time = datetime.time(17, 0)  # 5:00 pm
    return received_time.time() <= start_time or received_time.time() > end_time

def is_recent_reply_sent(phone_number, received_time):
    # Check if an automatic reply has been sent to this phone number within the last hour
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('received_messages')

    response = table.get_item(
        Key={
            'phone_number': phone_number,
            'message_id': 'latest'
        }
    )

    if 'Item' in response:
        last_sent_time = response['Item'].get('last_sent_time')
        if last_sent_time:
            last_sent_time = datetime.datetime.strptime(last_sent_time, '%H:%M').time()
            print("last :",last_sent_time)
            
            current_time = received_time.time()
            print(current_time)
            # Convert time objects to datetime objects
            last_sent_datetime = datetime.datetime.combine(datetime.date.today(), last_sent_time)
            current_datetime = datetime.datetime.combine(datetime.date.today(), current_time)

            time_difference = current_datetime - last_sent_datetime
            print(time_difference.total_seconds())
            if time_difference.total_seconds() < 3600:  # 1 hour in seconds
                return True

    return False

def send_reply(phone_number):
    # Send an automated reply using the Amazon SNS service
    sns = boto3.client('sns')
    
    # Replace 'YOUR_SNS_TOPIC_ARN' with the ARN of your SNS topic
    response = sns.publish(
        PhoneNumber=phone_number,
        Message='Thank you for your message. We will get back to you during business hours.'
    )
    print("Message sent")

def store_last_sent_time(phone_number, sent_time):
    # Store the last sent time for the phone number in the database
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('received_messages')
    
    table.put_item(
        Item={
            'phone_number': phone_number,
            'message_id': 'latest',
            'last_sent_time': sent_time.strftime('%H:%M')
        }
    )

def store_message(phone_number, message, received_time):
    # Store the SMS message in the database (e.g., Amazon DynamoDB, Amazon RDS, etc.)
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('received_messages')
    
    table.put_item(
        Item={
            'phone_number': phone_number,
            'message_id': 'latest',
            'message': message,
            'last_sent_time': received_time.strftime('%H:%M')
        }
    )

def lambda_handler(event, context):
    # Extract relevant details from the incoming event
    sender_phone = event['payload']['object']['sender']['phone_number']
    message = event['payload']['object']['message']
    received_time = datetime.datetime.strptime(event['payload']['object']['date_time'], '%H:%M')
    
    # Check if the message was received during after-hours
    if is_after_hours(received_time):
        # Check if an automatic reply has been sent within the last hour
        if not is_recent_reply_sent(sender_phone, received_time):
            print("Ping")
            # Send automated reply
            send_reply(sender_phone)
            # Store the last sent time
            store_last_sent_time(sender_phone, datetime.datetime.now())
            print("Stored")
    
    # Store the received message
    store_message(sender_phone, message, received_time)
    
    return {
        'statusCode': 200,
        'body': 'SMS processing completed.'
    }
