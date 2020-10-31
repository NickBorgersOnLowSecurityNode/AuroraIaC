import requests
import os
import json
import argparse

# Setup
parser = argparse.ArgumentParser(description='Take a device\'s effect config and save it')
parser.add_argument(nargs='?', dest='target', type=str, help='A device name to take config from')
args = parser.parse_args()

config_raw = open('.devices.json').read()
config = json.loads(config_raw)

if args.target is None:
  print("Must provide a target device to pull from")
  exit(1)

target = None

for device in config["devices"]:
  if device["name"] == args.target:
    print("Matched target: " + args.target)
    target = device

if target is None:
  print("Did not match target: " + args.target)
  exit(1)

# Get all effects
response = requests.put('http://' + target["address"] + ':16021/api/v1/' + target["token"] + '/effects', data='{"write" : {"command" : "requestAll"}}')
## Save effects
destination_file = open('effects.json', 'w')
destination_file.write(response.text)
destination_file.close()

print("Wrote effects.json")
