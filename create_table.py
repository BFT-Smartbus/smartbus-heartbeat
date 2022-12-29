from flask import Flask
import boto3

REGION_NAME = "us-east-1"
ENDPOINT_URL = "https://dynamodb.us-east-1.amazonaws.com/"

app = Flask(__name__)

# use boto3, a AWS SDK for Python to appoint which region to find your dynamodb table



dynamodb = boto3.resource(
    "dynamodb",
    region_name= REGION_NAME,
    endpoint_url= ENDPOINT_URL,
)

# create a dynamodb table named heartbeat, with a partition key:user_id, and a range key: time_stamp
table = dynamodb.create_table(
    TableName="heartbeat",
    KeySchema=[
        {"AttributeName": "user_id", "KeyType": "HASH"},
        {"AttributeName": "time_stamp", "KeyType": "RANGE"},
    ],  # Partition key
    AttributeDefinitions=[
        {"AttributeName": "user_id", "AttributeType": "S"},
        {"AttributeName": "time_stamp", "AttributeType": "N"},
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)
