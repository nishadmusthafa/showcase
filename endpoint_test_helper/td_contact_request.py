import requests
import json

pay_load = {
	    "auth": {
		"api_key": "ab74bc7b13b939fd6e662c09f47d248e34a12c27",
	    },
            "meta": {
            "offset": "1",
#            "synchronization_checkpoint": "2015-01-31 00:00:00 UTC",
	    }
	    }
headers = {'Content-type': 'application/json'}
url = 'https://talkdesk-integrator.herokuapp.com/integrations/nishadhelpscout/contact_sync/'
response = requests.post(url=url,data=json.dumps(pay_load), headers=headers)
print response.status_code
print response.content
