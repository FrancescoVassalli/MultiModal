import requests
import os
import json
from typing import Dict, Any, List
key = os.environ.get("TWELVE_LABS_API_KEY")

def get_indicies() ->Dict[str,Dict[str,str]]:
    """ Get all the indicies for your account into a dict dict"""

    get_indicies_url = "https://api.twelvelabs.io/v1.2/indexes?page=1&page_limit=10&sort_by=created_at&sort_option=desc"

    headers = {
        "accept": "application/json",
        "x-api-key": key,
        "Content-Type": "application/json"
    }

    response = requests.get(get_indicies_url, headers=headers)

    response_dict = json.loads(response.text)
    index_data = response_dict['data']
    index_name_id_map = {}


    for entry in index_data:
        index_name_id_map[entry['index_name']] = {'id':entry['_id']}


    print(index_name_id_map)
    return index_name_id_map

def get_videos(index_map:Dict[str,Dict[str,str]]) -> None:
    """ get all the videos for your indicies added to the input map"""
    for index_name, index_data in index_map.items():

        video_get_url = f"https://api.twelvelabs.io/v1.2/indexes/{index_data['id']}/videos?page=1&page_limit=10&sort_by=created_at&sort_option=desc"

        headers = {
            "accept": "application/json",
            "x-api-key": key,
            "Content-Type": "application/json"
        }

        response = requests.get(video_get_url, headers=headers)
        response_dict = json.loads(response.text)
        video_data = response_dict['data']
        video_id_list: List[str] = []
        for entry in video_data:
            video_id_list.append(entry['_id'])
        print(f"{index_name}: {video_id_list}")
        index_map[index_name]['video_ids'] = video_id_list

def get_transcript_string(transcript:List[Dict[str,Any]]) -> str:
    """convert the transcript dictionary 12 labs makes to a single single with \n between the breaks it makes"""
    if not transcript is None:
        all_str = [phrase['value'] for phrase in transcript]
        return "\n".join(all_str)
    else:
        return None


def get_transcripts(index_map:Dict[str,Dict[str,Any]]) -> None:
    """ get the transcript for each video added to the index map"""
    for index_name, index_data in index_map.items():
        index_id = index_data['id']
        transcript_dicts = []
        transcript_strs = []
        for video_id in index_data['video_ids']:
            transcript_get_url = f"https://api.twelvelabs.io/v1.2/indexes/{index_id}/videos/{video_id}/transcription"


            headers = {
                "accept": "application/json",
                "x-api-key": key,
                "Content-Type": "application/json"
            }

            response = requests.get(transcript_get_url, headers=headers)
            response_dict = json.loads(response.text)
            transcript_dicts.append(response_dict['data'])
            transcript_strs.append(get_transcript_string(response_dict['data']))

        print(f"{index_name}: {transcript_strs}")
        index_map[index_name]['transcript_dicts'] = transcript_dicts
        index_map[index_name]['transcript_str'] = transcript_strs


if __name__ == "__main__":
    index_map = get_indicies()
    get_videos(index_map)
    get_transcripts(index_map)
