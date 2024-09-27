import requests
import json

url = "http://API도메인/shorten"

long_url = "단축할 링크"

data = {
    "url": long_url
}


headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(data), headers=headers)


if response.status_code == 200:
    short_url = response.json().get("short_url")
    print(f"단축된 URL: {short_url}")
else:
    print(f"Error: {response.status_code}")
