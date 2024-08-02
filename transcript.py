import requests
url = "https://api.twelvelabs.io/v1.2/indexes/66abfc02dde98afa0afb285f/videos/66abfc8b7b2deac81dd12814/transcription?start=0&end=293"


headers = {
    "accept": "application/json",
    "x-api-key": "tlk_1DFFA7P17P2G9G289EBM33Q40FR2",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.text)
