from twelvelabs import TwelveLabs
import requests

import os
key = os.environ.get("TWELVE_LABS_API_KEY")
client = TwelveLabs(api_key=key)



# Variables
BASE_URL = "https://api.twelvelabs.io/v1.2"
data = {
    "video_id": "66abfc8b7b2deac81dd12814",
    "types": [
        "title",
        "hashtag",
        "topic"
    ]
}

# Send request
response = requests.post(f"{BASE_URL}/gist", json=data, headers={"x-api-key": api_key})

