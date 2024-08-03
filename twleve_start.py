from twelvelabs import TwelveLabs
import json
from io import StringIO
import requests
import pandas as pd
import numpy as np

import os
key = os.environ.get("TWELVE_LABS_API_KEY")
client = TwelveLabs(api_key=key)

def generate()->str:
    BASE_URL = "https://api.twelvelabs.io/v1.2"
    data = {
        "video_id": "66ad42ce7b2deac81dd12825",
        "type": "summary",
        "prompt": "This video has a snowboarding competition. Generate a table that records one row per trick performed. Add one column to label which person performed each trick. If you do not know their names just refer to them as person-1 or person-2 as they appear sequentially in the video. In a second column, name the trick. In the third column note if the trick was a Success or a Failure. Keep your response brief and do not include anything aside from the table.",
        "temperature": 0.43
    }

    response = requests.post(f"{BASE_URL}/summarize", json=data, headers={"x-api-key": key})
    response_dict = json.loads(response.text)
    return response_dict['summary']

def store_gen()->None:
    generate_text = generate()
    with open("temp.txt",'w') as gen_holder:
        gen_holder.write(generate_text)

def get_local_gen()->str:
    with open("temp.txt",'r') as file:
        return file.read()

def format_table(raw:str) -> str:
    pipe_index = raw.find('|')
    out = raw[pipe_index+1:]
    return out

#store_gen()
gen_text = get_local_gen()
gen_text = format_table(gen_text)
print(gen_text)
table_io = StringIO(gen_text)
df = pd.read_csv(table_io,sep='|', skipinitialspace=True,engine='python')
df.replace('-', np.nan, inplace=True)
df.columns = df.columns.str.strip()
print(df.columns)

print(df.head())

