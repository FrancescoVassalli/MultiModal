import requests

headers = {
    "accept": "application/json",
    "x-api-key": "tlk_1DFFA7P17P2G9G289EBM33Q40FR2",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.text)
