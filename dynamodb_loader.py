import boto3
import json
import yaml
from decimal import Decimal

yaml_file = open('settings.yaml', 'r')
settings = yaml.safe_load(yaml_file)

dynamodb = boto3.resource('dynamodb', settings['REGION_NAME'])
table = dynamodb.Table(settings['TABLE_NAME'])

with open(settings['FILE_NAME']) as json_file:
  heartbeats = json.load(json_file)
  heartbeat_converted = json.loads(json.dumps(heartbeats),
  parse_float=Decimal)

  for heartbeat in heartbeat_converted:
    user_id = heartbeat['user_id']
    time_stamp = heartbeat['time_stamp']
    latitude = heartbeat['latitude']
    longitude = heartbeat['longitude']
    speed = heartbeat['speed']

    try:
      response = table.put_item(
        Item = {
          'userId': user_id,
          'timestamp': time_stamp,
          'latitude': latitude,
          'longitude': longitude,
          'speed': speed
          }
        )
    except Exception as e:
      print(f"unable to load data into dynamoDB table heartbeat: {e}")
