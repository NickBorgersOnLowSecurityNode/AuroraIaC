import requests
import os
import json
import time
import threading

# Setup
config_raw = open('.devices.json').read()
config = json.loads(config_raw)

## Read effects to apply
effects_to_apply_raw = open('effects.json').read()
effects_to_apply = json.loads(effects_to_apply_raw)
print("Read effects.json")
  
def clear_and_configure(target, effects_to_apply):
  print("Clearing and configuring " + target["name"])
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
      print(target["name"] + ": Deleted: " + existing_effect["animName"])
      time.sleep(0.5)
    else:
      print(target["name"] + ": Failed to delete " + existing_effect["animName"])
      print(delete_response)
      exit(1)

  # Apply effects to target
  ## Create effects
  for effect_to_apply in effects_to_apply["animations"]:
    request = {}
    request["write"] = effect_to_apply
    request["write"]["command"] = "add"
    create_response = requests.put(url, data=json.dumps(request))
    if create_response.status_code >=200 and create_response.status_code <300 :
      print(target["name"] + ": Created: " + effect_to_apply["animName"])
      time.sleep(0.5)
    else:
      print(target["name"] + ": Failed to create " + effect_to_apply["animName"])
      print(delete_response)
      exit(1)

threads = list()

for target in config["devices"]:
  thisThread = threading.Thread(target=clear_and_configure, args=(target, effects_to_apply))
  threads.append(thisThread)
  thisThread.start()
  
for thread in threads:
  thread.join()

print("Configured all Auroras")
