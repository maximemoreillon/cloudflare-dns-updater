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


print(f'Updating DNS record {RECORD_NAME} with IP {ip}')
response = requests.get(
  f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/', 
  headers={
    "X-Auth-Email": EMAIL,
    "X-Auth-Key": GLOBAL_API_KEY,
  },
)

record = next(item for item in response.json()["result"] if item["name"] == RECORD_NAME)


# print(f'Updating DNS record {RECORD_NAME} with IP {ip}')
response = requests.put(
  f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record["id"]}', 
  headers={
    "X-Auth-Email": EMAIL,
    "X-Auth-Key": GLOBAL_API_KEY,
  }, 
  json={
    "content": ip,
    "name": RECORD_NAME,
    "type": "A",
    "proxied": True
  }
)
print(response.text)

