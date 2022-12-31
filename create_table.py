import boto3
from yaml import load
from yaml import Loader

with open("settings.yaml", "r") as stream:
    data = load(stream, Loader=Loader)



dynamodb = boto3.resource(
    "dynamodb",
    region_name = data['REGION_NAME'],
    endpoint_url= data['ENDPOINT_URL']
)

table = dynamodb.create_table(
    TableName= data['TABLE_NAME'],
    KeySchema= data['KEYSCHEMA'],
    AttributeDefinitions= data['ATTRIBUTEDEFINITIONS'],
    ProvisionedThroughput= data['PROVISIONEDTHROUGHPUT'],
)



