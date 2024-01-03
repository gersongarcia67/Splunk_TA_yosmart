
# This script get yosmart token
# http://doc.yosmart.com/docs/overall/qsg_uac

import requests
import json
import sys
import datetime

debug=False

uaid="ua_54946F6B5D494AC48AE9009798C26623"
client_secret="sec_v1_sPbZJE8jR39N/0JEKKD1uA=="
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
else:
        print('Success!')

try:
	json_response = response.json()

	if debug:
		print(json.dumps(json_response, indent=4))

except:

	print('Uanable to convert to json.')
	sys.exit()

if 'msg' in json_response:
	print(json.dumps(json_response, indent=4))

if 'access_token' not in json_response:
	print('Unable to get access_token, skip.')
	sys.exit()

print('%s access_token=%s' % (datetime.datetime.utcnow(),json_response['access_token']))






