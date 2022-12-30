from flask import Flask
import boto3
import yaml
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

app = Flask(__name__)

with open("settings.yaml", "r") as stream:
    data = load(stream, Loader=Loader)


app = Flask(__name__)


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



