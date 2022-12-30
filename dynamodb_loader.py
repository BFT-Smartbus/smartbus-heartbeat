import boto3
import json
from decimal import Decimal
from yaml import load

# try:
#     from yaml import CLoader as Loader
# except ImportError:
#     from yaml import Loader

# with open("settings.yaml", "r") as stream:
#     data = load(stream, Loader=Loader)



# dynamodb = boto3.resource('dynamodb', data['REGION_NAME'])
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

table = dynamodb.Table('heartbeat')

with open('heartbeat_data.json') as json_file:
  heartbeats = json.load(json_file)
  heartbeat_converted = json.loads(json.dumps(heartbeats), parse_float=Decimal)
  for heartbeat in heartbeat_converted:
    user_id = heartbeat['user_id']
    time_stamp = heartbeat['time_stamp']
    latitude = heartbeat['latitude']
    longitude = heartbeat['longitude']
    speed = heartbeat['speed']
    response = table.put_item(
      Item = {
        'userId': user_id,
        'timestamp': time_stamp,
        'latitude': latitude,
        'longitude': longitude,
        'speed': speed
      }
    )
