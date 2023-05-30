import requests
import json, os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
# Register the metadata to be stored by Discord. This should be a one time action.
# Note: uses a Bot token for authentication, not a user token.

url = f"https://discord.com/api/v10/applications/{os.environ.get('CLIENT_ID')}/role-connections/metadata"
print(url)
# supported types: number_lt=1, number_gt=2, number_eq=3 number_neq=4, datetime_lt=5, datetime_gt=6, boolean_eq=7, boolean_neq=8
# You can read more here https://discord.com/developers/docs/resources/application-role-connection-metadata
body = [
  {
    'key': 'verified',
    'name': 'Verificado',
    'description': 'Que haya sido comprobado por las autoridades.',
    'type': 7,
  },
  {
    'key': 'time',
    'name': 'Time',
    'description': 'DATETIME_GREATER_THAN_OR_EQUAL',
    'type': 6,
  },
]
response = requests.put(url, data=json.dumps(body), headers={
  'Content-Type': 'application/json',
  'Authorization': f"Bot {os.environ.get('TOKEN')}",
})
if response.ok:
  data = response.json()
else:
  data = response.text
  
print(data)