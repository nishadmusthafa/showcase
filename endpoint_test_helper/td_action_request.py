import requests
import json

pay_load = {
	    "auth": {
		"api_key": "ab74bc7b13b939fd6e662c09f47d248e34a12c27",
	    },
	    "meta": {
		"contact_external_id": "46010392",
		"agent_external_id": "2"
	    },
	    "data": {
		"subject": "Call missed in Talkdesk",
		"body": "A call from Jane Doe was missed.",
		"mailbox": "37924"
	    }}
headers = {'Content-type': 'application/json'}
url = 'https://talkdesk-integrator.herokuapp.com/integrations/nishadhelpscout/actions/create_ticket/'
response = requests.post(url=url,data=json.dumps(pay_load), headers=headers)
print response.status_code
print response.content
