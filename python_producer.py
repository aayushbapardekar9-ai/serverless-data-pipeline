import boto3
import json
import time
import uuid
import random
from faker import Faker

# --- CONFIGURATION ---
# Replace with the Queue URL you copied in Phase 1
QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/926095813248/TweetQueue'
REGION = 'ap-south-1'

# Initialize the Faker library for data generation
fake = Faker()

# Initialize the Boto3 SQS client
# Ensure you have run 'aws configure' on your machine before running this
sqs = boto3.client('sqs', region_name=REGION)

def generate_tweet():
    """
    Generates a dictionary representing a fake tweet.
    Injects hashtags randomly to test extraction logic.
    """
    tweet_text = fake.text()
    
    # FIXED: Added a list of dummy hashtags
    hashtags = ['#AWS', '#Python', '#Serverless', '#Cloud', '#Coding', '#DevOps']
    
    # FIXED: random.choice needs a list to choose from (True/False)
    if random.choice([True, False]):
        selected_tags = random.sample(hashtags, k=random.randint(1, 3))
        tweet_text += " " + " ".join(selected_tags)
    
    return {
        'id': str(uuid.uuid4()),
        'message': tweet_text,
        'timestamp': str(fake.date_time_this_year()),
        'username': fake.user_name(),
        'location': fake.city()
    }

def send_messages(count=50):
    """
    Generates and sends 'count' number of messages to the SQS queue.
    """
    print(f"--- Starting Producer: Sending {count} tweets ---")
    
    for i in range(count):
        # 1. Generate Data
        tweet = generate_tweet()
        
        # 2. Serialize to JSON
        # SQS MessageBody must be a String
        message_body = json.dumps(tweet)
        
        try:
            # 3. Send to SQS
            response = sqs.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=message_body,
                MessageAttributes={
                    'Author': {
                        'StringValue': 'FakerScript',
                        'DataType': 'String'
                    }
                }
            )
            print(f"[{i+1}/{count}] Sent Tweet ID: {tweet['id']} | Message ID: {response['MessageId']}")
        except Exception as e:
            print(f"Error sending message: {e}")
        
        # Simulate real-time data ingestion delay
        time.sleep(0.1)

if __name__ == "__main__":
    send_messages(100)
    print("--- Producer Finished ---")