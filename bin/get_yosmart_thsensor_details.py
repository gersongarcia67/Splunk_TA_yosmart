#!/usr/bin/python3

# This script get yosmart THSensor details
# http://doc.yosmart.com/docs/yolinkapi/THSensor

import requests
from requests.exceptions import HTTPError
import json
import sys
import datetime

debug=False

uaid="ua_54946F6B5D494AC48AE9009798C26623"
client_secret="sec_v1_sPbZJE8jR39N/0JEKKD1uA=="

def get_yolink_token(uaid,client_secret,debug):

	api="https://api.yosmart.com/open/yolink/token"

	params={ 'grant_type':'client_credentials',
         	 'client_id':uaid,
         	 'client_secret':client_secret }
         

	try:
		response=requests.post(api,params)

		response.raise_for_status()

	except HTTPError as http_err:
        	print(f'HTTP error occurred: {http_err}')
	except Exception as err:
        	print(f'Other error occurred: {err}')

	try:
		json_response = response.json()

		if debug:
			print(json.dumps(json_response, indent=4))

	except:

		print('Uanable to convert to json.')
		sys.exit()

	if 'access_token' not in json_response:
		print('Unable to get access_token, skip. %s' % json.dumps(json_response, indent=4))
		sys.exit()

	access_token=json_response['access_token']
	return access_token


if len(sys.argv) != 3:
	print(f'Error: Invalid number of paramenters: {sys.argv[0]} <device_id> <net_token>')
	sys.exit(2)

access_token=get_yolink_token(uaid,client_secret,debug)
if debug:
	print('%s access_token=%s' % (datetime.datetime.utcnow(),access_token))


api='https://api.yosmart.com/open/yolink/v2/api'

headers={ 'Content-Type':'application/json',
          'Authorization': f'Bearer {access_token}' }

bddp={ 'method':'THSensor.getState',
       'targetDevice':f'{sys.argv[1]}',
       'token' : f'{sys.argv[2]}' }

try:
	response=requests.post(api,json=bddp,headers=headers)
	response.raise_for_status()

except HTTPError as http_err:
	print(f'HTTP error occurred: {http_err}')
	sys.exit(2)
except Exception as err:
	print(f'Other error occurred: {err}')
	sys.exit(2)

try:
	json_response = response.json()
except:
	print(f'Unable to parse response to json. {response}')


if debug:
	print(json.dumps(json_response, indent=4))

if json_response['desc'] != 'Success':
	print(f'Unable to read output from {api}: {json.dumps(json_response, indent=4)}')
	sys.exit(2)

# Before dump to Splunk, add collector date/time (when script ran)
#print(f"Collect time: NOW: {datetime.datetime.utcnow()} FROM API: {json_response['time']}")
#print(f"Collect time: NOW: {datetime.datetime.utcnow()} FROM API: {json_response['time']} {datetime.datetime.utcfromtimestamp(int(json_response['time'])/1000)}")

json_response['time_str']=f"{datetime.datetime.utcfromtimestamp(int(json_response['time'])/1000)}"
print(json.dumps(json_response))

