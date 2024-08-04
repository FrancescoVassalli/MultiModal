import os
from twelvelabs import TwelveLabs
import json
from io import StringIO
import requests
import pandas as pd
import numpy as np
from pandas.errors import EmptyDataError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

key = os.environ.get("TWELVE_LABS_API_KEY")
client = TwelveLabs(api_key=key)

def generate(video_id:str)->str:
    BASE_URL = "https://api.twelvelabs.io/v1.2"
    trick_descriptions = '''Indy: Grabbing the toe edge of the board between the bindings with the back hand.
Mute: Grabbing the toe edge of the board between the bindings with the front hand.
Stalefish: Grabbing the heel edge of the board between the bindings with the back hand.
Melon: Grabbing the heel edge of the board between the bindings with the front hand.
Tail Grab: Grabbing the tail of the board.
Nose Grab: Grabbing the nose of the board.
Method: Grabbing the heel edge of the board with the front hand while arching the back and extending the legs.
Japan: Grabbing the toe edge of the board with the front hand while tucking the knees and rotating the board.
Seatbelt: Grabbing the nose of the board with the back hand.
Truck Driver: Grabbing the nose of the board with the front hand and the tail with the back hand simultaneously.
Rodeo: A backward flip with a 180 or 540-degree spin.
Misty: A forward flip with a 180 or 540-degree spin.
Cork: An off-axis spin, where the boarder is tilted.
Double Cork: A double off-axis spin.
Wildcat: A backflip with a rotation around the snowboarder’s side.
Jumps
Ollie: Lifting the front foot, followed by the back foot, to jump.
Nollie: Lifting the back foot, followed by the front foot, to jump.
Slides and Grinds
Boardslide: Sliding with the board perpendicular to the rail.
Lipslide: Approaching from the opposite side and sliding with the board perpendicular to the rail.
50-50: Sliding straight along a rail with the board parallel.
Nose Slide: Sliding on the nose of the board.
Tail Slide: Sliding on the tail of the board.
Blunt Slide: Sliding on the tail of the board with the nose raised.
Buttering
Nose Butter: Pressing down on the nose of the board while rotating the tail.
Tail Butter: Pressing down on the tail of the board while rotating the nose.
Nose Roll: A 180-degree rotation while buttering on the nose.
Tail Roll: A 180-degree rotation while buttering on the tail.
'''


    data = {
        "video_id": video_id,
        "type": "summary",
        "prompt": f"This video has a snowboarding competition. Use expert Generate a table that records one row per trick performed. Add one column called Athlete to label which person performed each trick. If you do not know their names just refer to them as person-1 or person-2 as they appear sequentially in the video. In a second column called Trick, name the trick. In the third column called Result note if the trick was a Success or a Failure. In a fourth column called Half say Yes if the video has a half pipe and No if it does not. In a fifth column called Rail say Yes if the video has a rail and no if it does not. Keep your response brief and do not include anything aside from the table. If you are unsure of what to call a track you may reference this vocabulary list {trick_descriptions}",
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

def format_table(raw:str,video_id:str) -> pd.DataFrame:
    pipe_index = raw.find('|')
    out = raw[pipe_index+1:]
    table_io = StringIO(out)
    try:
        df = pd.read_csv(table_io,sep='|', skipinitialspace=True,engine='python')
        df.replace('-', np.nan, inplace=True)
        df.columns = df.columns.str.strip()
        df['ID'] = video_id
        return df
    except EmptyDataError as e:
        return


def get_table_for_video(video_id:str) -> pd.DataFrame:
    store_gen(video_id)
    gen_text = get_local_gen(video_id)
    return format_table(gen_text,video_id)


if __name__ == "__main__":
    vid_id = "66ad42ce7b2deac81dd12825"
    df = get_table_for_video(vid_id)
    print(df.columns)
    print(df)
