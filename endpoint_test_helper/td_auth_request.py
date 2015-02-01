import requests
import json

pay_load = {
	    "auth": {
		"api_key": "b74bc7b13b939fd6e662c09f47d248e34a12c27",
	    }
	    }
headers = {'Content-type': 'application/json'}
url = 'https://talkdesk-integrator.herokuapp.com/integrations/nishadhelpscout/auth_validation/'
response = requests.post(url=url,data=json.dumps(pay_load), headers=headers)
print response.status_code
print response.content
