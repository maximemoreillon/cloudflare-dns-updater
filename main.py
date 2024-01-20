import requests
from os import environ
from dotenv import load_dotenv
from time import sleep
import json

load_dotenv()

RECORD_NAME = environ.get('CLOUDFLARE_RECORD_NAME')
EMAIL = environ.get('CLOUDFLARE_EMAIL')
GLOBAL_API_KEY = environ.get('CLOUDFLARE_GLOBAL_API_KEY')
ZONE_ID = environ.get('CLOUDFLARE_ZONE_ID')

ip = requests.get('https://api.ipify.org').content.decode('utf8')

headers = {
  "X-Auth-Email": EMAIL,
  "X-Auth-Key": GLOBAL_API_KEY,
}


print(f'Updating DNS record {RECORD_NAME} with IP {ip}')

response = requests.get(
  f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/', 
  headers=headers,
)

responseJSON = response.json()

if not responseJSON['success']:
  raise SystemExit(f'DNS update failed: {responseJSON["errors"][0]["message"]}')

# Find record in list
record = next(item for item in responseJSON["result"] if item["name"] == RECORD_NAME)

response = requests.put(
  f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record["id"]}', 
  headers=headers, 
  json={
    "content": ip,
    "name": RECORD_NAME,
    "type": "A",
    "proxied": True
  }
)

print(response.text)

