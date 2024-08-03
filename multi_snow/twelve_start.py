from twelvelabs import TwelveLabs
import json
from io import StringIO
import requests
import pandas as pd
import numpy as np
from pandas.errors import EmptyDataError


import os
key = os.environ.get("TWELVE_LABS_API_KEY")
client = TwelveLabs(api_key=key)

def generate(video_id:str)->str:
    BASE_URL = "https://api.twelvelabs.io/v1.2"
    data = {
        "video_id": video_id,
        "type": "summary",
        "prompt": "This video has a snowboarding competition. Generate a table that records one row per trick performed. Add one column called Athlete to label which person performed each trick. If you do not know their names just refer to them as person-1 or person-2 as they appear sequentially in the video. In a second column called Trick, name the trick. In the third column called Result note if the trick was a Success or a Failure. Keep your response brief and do not include anything aside from the table.",
        "temperature": 0.5
    }

    response = requests.post(f"{BASE_URL}/summarize", json=data, headers={"x-api-key": key})
    response_dict = json.loads(response.text)
    if 'summary' in response_dict:
        return response_dict['summary']
    else:
        print(f"Summary for {video_id} unable to be generated. Got response {response}")

def get_temp_file_name(vid_id:str) -> str:
    """generate a temp name to store responses in"""
    return f"temp_{vid_id}.txt"

def store_gen(vid_id:str)->None:
    generate_text = generate(vid_id)
    if not generate_text is None:
        with open(get_temp_file_name(vid_id),'w') as gen_holder:
            gen_holder.write(generate_text)

def get_local_gen(vid_id)->str:
    with open(get_temp_file_name(vid_id),'r') as file:
        return file.read()

def format_table(raw:str) -> pd.DataFrame:
    pipe_index = raw.find('|')
    out = raw[pipe_index+1:]
    table_io = StringIO(out)
    try:
        df = pd.read_csv(table_io,sep='|', skipinitialspace=True,engine='python')
        df.replace('-', np.nan, inplace=True)
        df.columns = df.columns.str.strip()
        return df
    except EmptyDataError as e:
        return



def get_table_for_video(video_id:str) -> pd.DataFrame:
    #store_gen(video_id)
    gen_text = get_local_gen(video_id)
    return format_table(gen_text)


if __name__ == "__main__":
    vid_id = "66ad42ce7b2deac81dd12825"
    df = get_table_for_video(vid_id)
    print(df.columns)
    print(df)

