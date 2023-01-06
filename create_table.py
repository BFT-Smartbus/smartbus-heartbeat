import boto3
import yaml
SETTINGS = 'settings.yaml'

with open(SETTINGS, "r") as yaml_file:
    settings = yaml.safe_load(yaml_file)

dynamodb = boto3.resource(
    "dynamodb",
    region_name = settings['REGION_NAME'],
    endpoint_url= settings['ENDPOINT_URL']
)

try:
    table = dynamodb.create_table(
        TableName= settings['TABLE_NAME'],
        KeySchema= settings['KEYSCHEMA'],
        AttributeDefinitions= settings['ATTRIBUTEDEFINITIONS'],
        ProvisionedThroughput= settings['PROVISIONEDTHROUGHPUT'],
    )
except Exception as e:
    print(f"unable to create dynamo table heartbeat: {e}")




