import boto3
import json
from decimal import Decimal
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

#load constant values from setting.yaml
with open("settings.yaml", "r") as stream:
    data = load(stream, Loader=Loader)

#use boto3, a AWS SDK for Python to appoint which region to find your dynamodb table
dynamodb = boto3.resource('dynamodb', data['REGION_NAME'])

table = dynamodb.Table('heartbeat')

#open the JSON file that has some heartbeat testing data, load this JSON file
with open('heartbeat_data.json') as json_file:
  heartbeats = json.load(json_file)

  #convert JSON data where it has float data structure to decimal data structure since AWS DynamoDB does not support float type, and convert it to a dictionary
  heartbeat_converted = json.loads(json.dumps(heartbeats), parse_float=Decimal)

  #loop over the heartbeat list, and write all heartbeat data to dynamoDB heartbeat table.
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
