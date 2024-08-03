import requests
import os
import json
import pandas as pd
from typing import Dict, Any, List, Tuple
from groq import Groq
from multi_snow.twelve_start import get_table_for_video

key = os.environ.get("TWELVE_LABS_API_KEY")
client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )

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

def get_transcript(index_id:str,video_id:str) -> Tuple[List[Dict[str,Any]],str]:
    """get the transcript for a single video returns the same data in 12labs dict format and as a combined string"""
    transcript_get_url = f"https://api.twelvelabs.io/v1.2/indexes/{index_id}/videos/{video_id}/transcription"


    headers = {
        "accept": "application/json",
        "x-api-key": key,
        "Content-Type": "application/json"
    }
    response = requests.get(transcript_get_url, headers=headers)
    response_dict = json.loads(response.text)
    return (response_dict['data'],get_transcript_string(response_dict['data']))


def get_transcripts(index_map:Dict[str,Dict[str,Any]]) -> None:
    """ get the transcript for each video added to the index map"""
    for index_name, index_data in index_map.items():
        index_id = index_data['id']
        transcript_dicts = []
        transcript_strs = []
        for video_id in index_data['video_ids']:
            transcript_dict, transcript_str = get_transcript(index_id,video_id)
            transcript_dicts.append(transcript_dict)
            transcript_strs.append(transcript_str)

        print(f"{index_name}: {transcript_strs}")
        index_map[index_name]['transcript_dicts'] = transcript_dicts
        index_map[index_name]['transcript_str'] = transcript_strs


def make_trick_table_from_transcript_with_groq(transcript:str) -> str:
    system_prompt = {
        "role": "system",
        "content":
        "You will be given a transcript from a snowboarding video. Summarize this trancript by making a table with one row per trick performed. Add columns for the name of the person performing the trick, the name of the trick, and success/failure"
    }
    chat_history = [system_prompt]
    chat_history.append({"role": "user", "content": transcript})
    response = client.chat.completions.create(model="llama3-70b-8192",
                                            messages=chat_history,
                                            max_tokens=100,
                                            temperature=1.2)
    print(response.choices[0].message.content)




if __name__ == "__main__":
    index_map = get_indicies()
    filtered_index_map = {'SNOW4':index_map['SNOW4']}
    get_videos(filtered_index_map)
    filtered_video_ids:List[str] = filtered_index_map['SNOW4']['video_ids']
    print(f"Video ids: {filtered_video_ids}")
    video_tables:List[pd.DataFrame] = []
    for video_id in filtered_video_ids:
        df = get_table_for_video(video_id)
        if df is None:
            continue
        video_tables.append(df)
    df = pd.concat(video_tables,ignore_index=True)
    df['Result'] = df['Result'].apply(lambda x: x.strip() if not x is None else x)

    print(df)
    df.to_csv('output.csv',index=False)
    print(df[df['Result'] == 'Failure'])


