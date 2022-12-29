from flask import Flask
import boto3

app = Flask(__name__)

# use boto3, a AWS SDK for Python to appoint which region to find your dynamodb table
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="https://dynamodb.us-east-1.amazonaws.com/",
)

# create a dynamodb table named heartbeat, with a partition key:user_id, and a range key: time_stamp
table = dynamodb.create_table(
    TableName="heartbeat",
    KeySchema=[
        {"AttributeName": "userId", "KeyType": "HASH"},
        {"AttributeName": "timestamp", "KeyType": "RANGE"},
    ],  # Partition key
    AttributeDefinitions=[
        {"AttributeName": "userId", "AttributeType": "S"},
        {"AttributeName": "timestamp", "AttributeType": "N"},
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)
