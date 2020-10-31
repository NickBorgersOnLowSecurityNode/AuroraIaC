import requests
import os
import json
import argparse
import time

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

base_url = 'http://' + target["address"] + ':16021/api/v1/' + target["token"]
url = base_url + '/effects'

# Clear existing effects
## Get existing effects
existing_effects_response = requests.put(url, data='{"write" : {"command" : "requestAll"}}')
existing_effects  = json.loads(existing_effects_response.text)
## Iterate and delete
for existing_effect in existing_effects["animations"]: 
  request = {}
  request["write"] = {}
  request["write"]["command"] = "delete"
  request["write"]["animName"] = existing_effect["animName"]
  delete_response = requests.put(url, data=json.dumps(request))
  if delete_response.status_code >=200 and delete_response.status_code <300 :
    print("Deleted: " + existing_effect["animName"])
    time.sleep(0.1)
  else:
    print("Failed to delete " + existing_effect["animName"])
    print(delete_response)
    exit(1)

# Apply effects to target
## Read effects to apply
effects_to_apply_raw = open('effects.json').read()
effects_to_apply = json.loads(effects_to_apply_raw)
print("Read effects.json")
## Create effects
for effect_to_apply in effects_to_apply["animations"]:
  request = {}
  request["write"] = effect_to_apply
  request["write"]["command"] = "add"
  create_response = requests.put(url, data=json.dumps(request))
  if create_response.status_code >=200 and create_response.status_code <300 :
    print("Create: " + effect_to_apply["animName"])
    time.sleep(0.1)
  else:
    print("Failed to create " + effect_to_apply["animName"])
    print(delete_response)
    exit(1)
