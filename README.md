##### **Serverless Data Processing Pipeline**



**Project Overview**

This project simulates a real-time data streaming pipeline for social media data. It mimics a "firehose" of tweets using a local Python producer, buffers the data using Amazon SQS, and processes it using a serverless AWS Lambda function.

The system demonstrates an Event-Driven Architecture (EDA) capable of handling bursty traffic without managing servers. It implements a "Polyglot Persistence" strategy by saving structured data to a NoSQL database and raw data to object storage.



**Architecture**

Flow: Producer (Local) --> AWS SQS --> AWS Lambda --> DynamoDB \& S3

1\.	Ingestion (Producer): A Python script uses the Faker library to generate synthetic tweets containing hashtags, timestamps, and messages. It sends these as JSON objects to an Amazon SQS queue.

2\.	Buffering (SQS): SQS acts as a buffer to decouple the producer from the consumer, ensuring no data is lost during traffic spikes.

3\.	Processing (Lambda): An AWS Lambda function triggers automatically when messages arrive in the queue. It parses the JSON and extracts hashtags using Regex.

4\.	Storage:

o	Hot Storage (DynamoDB): Parsed metadata (Tweet ID, Message, Hashtags) is stored in Amazon DynamoDB for fast querying.

o	Cold Storage (S3): The raw JSON payload is archived in Amazon S3 for compliance and data replay.



**Technologies Used**

•	Cloud Provider: Amazon Web Services (AWS)

•	Core Services: Lambda, Simple Queue Service (SQS), DynamoDB, S3, CloudWatch, IAM.

•	Language: Python 3.9

•	Libraries: boto3 (AWS SDK), faker (Data Generation), json.

Project Structure

•	producer.py: Local Python script that generates fake data and pushes it to the SQS queue.

•	lambda\_function.py: The logic deployed on AWS Lambda to process incoming messages.

•	README.md: Project documentation.



**Setup \& Installation**

**Prerequisites**

•	An active AWS Account.

•	Python 3.x installed on your local machine.

•	AWS CLI configured locally with aws configure.

1\. AWS Infrastructure Setup

Resources were created using the AWS Management Console:

•	SQS Queue: Created a standard queue named TweetQueue.

•	DynamoDB Table: Created a table named Tweets with Partition Key TweetID.

•	S3 Bucket: Created a unique bucket for raw data archival.

•	IAM Role: Configured a Lambda Execution Role with permissions: sqs:ReceiveMessage, sqs:DeleteMessage, dynamodb:PutItem, and s3:PutObject.

2\. Local Configuration

1\.	Clone this repository:bash

git clone https://github.com/aayushbapardekar9-ai/serverless-data-pipeline

2\.	Install required Python libraries:

Bash

pip install boto3 faker

3\.	Update Configuration:

o	Open producer.py and replace the QUEUE\_URL with your specific SQS Queue URL.

**How to Run**

1\.	Start the Producer:

Run the script locally to start sending 100 fake tweets to the cloud.

Bash

python producer.py

2\.	Verify Processing:

o	Check the DynamoDB table Tweets to see the structured data and extracted hashtags.

o	Check the S3 bucket to see the raw JSON files saved.

o	Check CloudWatch Logs (/aws/lambda/TweetProcessor) to view execution logs.



**Key Learnings**

•	Designing Event-Driven Architectures using SQS to decouple microservices.

•	Implementing Serverless ETL (Extract, Transform, Load) logic with AWS Lambda.

•	Working with Boto3 to interact with AWS services programmatically.

•	Handling Idempotency and error handling in distributed systems.





