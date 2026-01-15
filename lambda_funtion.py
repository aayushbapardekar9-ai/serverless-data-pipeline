import json
import boto3
import os
import uuid
from datetime import datetime

# --- CONFIGURATION ---
# We use your specific Bucket and Table names here
BUCKET_NAME = 'tweet-archive-aayush-123' 
TABLE_NAME = 'Tweets'
REGION = 'ap-south-1'

s3 = boto3.client('s3', region_name=REGION)
dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def lambda_handler(event, context):
    print("--- Starting Batch Processing ---")
    
    # This list tracks messages we failed to process so SQS can retry ONLY those
    batch_item_failures = []

    for record in event['Records']:
        try:
            # 1. Parse the "Body" (which is the JSON string sent by your Python script)
            payload = json.loads(record['body'])
            print(f"Processing Tweet ID: {payload.get('id', 'Unknown')}")

            # 2. Add a 'processed_timestamp' to show when Lambda touched it
            payload['processed_timestamp'] = datetime.now().isoformat()

            # --- ACTION A: Save to DynamoDB ---
            # DynamoDB expects a dictionary. 'id' is our Partition Key.
            # We map 'id' to 'TweetID' if your table schema expects that specific key name
            db_item = {
                'TweetID': payload['id'],       # Matches your Partition Key 'TweetID'
                'Message': payload['message'],
                'Username': payload['username'],
                'Timestamp': payload['timestamp'],
                'Location': payload['location']
            }
            table.put_item(Item=db_item)
            print(f"-> Saved to DynamoDB: {payload['id']}")

            # --- ACTION B: Save to S3 ---
            # S3 needs a unique filename. We'll use "tweet_{ID}.json"
            file_name = f"tweet_{payload['id']}.json"
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=file_name,
                Body=json.dumps(payload),
                ContentType='application/json'
            )
            print(f"-> Saved to S3: {file_name}")

        except Exception as e:
            print(f"[ERROR] Failed to process message {record['messageId']}: {str(e)}")
            # Add this message ID to the failure list so SQS tries again later
            batch_item_failures.append({"itemIdentifier": record['messageId']})

    print(f"--- Batch Finished. Failures: {len(batch_item_failures)} ---")
    
    # Return the list of failed messages (if any) to SQS
    return {
        'batchItemFailures': batch_item_failures
    }