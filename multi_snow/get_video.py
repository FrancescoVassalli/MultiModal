import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

key = os.environ.get("TWELVE_LABS_API_KEY")

def get_video_data(query:str,retry:int=0)->str:
    """get the video id for a given query"""
    BASE_URL = "https://api.twelvelabs.io/v1.2"
    data = {
        "index_id": "66ad59fa0af328de7c937e50",
        "query": query,
        "group_by": "clip",
        "search_options": [
            "visual",
            "conversation"
        ],
        "threshold": "low",
        "page_limit": 12
    }
    response = requests.post(f"{BASE_URL}/search", json=data, headers={"x-api-key": key})
    search = json.loads(response.text)
    if 'data' in search and retry < len(search['data']):
        return search['data'][retry]
    else:
        print(response.text)


def get_video_id(query:str,retry:int=0)->str:
    """get the video id for a given query"""
    video_data = get_video_data(query,retry)
    if not video_data is None:
        return video_data['video_id']
    else:
        None

def get_video_from_id(video_id:str):
    """ get the HLS URL for the video"""

    url = f"https://api.twelvelabs.io/v1.2/indexes/66ad59fa0af328de7c937e50/videos/{video_id}"

    headers = {
        "accept": "application/json",
        "x-api-key": key,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    return json.loads(response.text)['hls']['video_url']

def get_video_hls_from_query(query:str,retry:int=0) -> str:
    ''' given a query return a hls url'''
    video_id = get_video_id(query,retry)
    if not video_id is None:
        return get_video_from_id(video_id)


if __name__ == "__main__":
    query = '''Triple court 14-40 double grab'''
    print(get_video_hls_from_query(query))
