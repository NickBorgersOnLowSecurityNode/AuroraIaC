import requests
import os
import json
import argparse

# Setup
parser = argparse.ArgumentParser(description='Set a particular Aurora to a particular effect')
parser.add_argument(nargs='?', dest='target', type=str, help='A device name to act on')
parser.add_argument("--effect", type=str, help='An effect to activate')
args = parser.parse_args()

config_raw = open('.devices.json').read()
config = json.loads(config_raw)

if args.target is None:
  print("Must provide a target device to pull from")
  exit(1)
  
if args.effect is None:
  print("Must provide an effect to activate")
  exit(1)

target = None

for device in config["devices"]:
  if device["name"] == args.target:
    print("Matched target: " + args.target)
    target = device

if target is None:
  print("Did not match target: " + args.target)
  exit(1)

# Set desired effect
request = {}
request["select"] = args.effect
response = requests.put('http://' + target["address"] + ':16021/api/v1/' + target["token"] + '/effects', data=json.dumps(request))
if response.status_code >=200 and response.status_code <300 :
  print("Activated effect: " + args.effect)
else:
  print("Failed to activate: " + args.effect)
  print(delete_response)
  exit(1)
