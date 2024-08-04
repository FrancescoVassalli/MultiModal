from twelvelabs import TwelveLabs
import json
from io import StringIO
import requests
import pandas as pd
import numpy as np
import os
from io import StringIO
from groq import Groq

def format_table(raw:str) -> pd.DataFrame:
    pipe_index = raw.find('|')
    out = raw[pipe_index+1:]
    table_io = StringIO(out)
    df = pd.read_csv(table_io,sep='|', skipinitialspace=True,engine='python')
    df.replace('-', np.nan, inplace=True)
    df.columns = df.columns.str.strip()
    return df

def get_one_trick_categories(input):
    """
    takes a text input and outputs a table with categorization
    """

    groq_client = Groq()
    
    transcript = input
    system_prompt = """
You are an AI trained to categorize a snowboard trick into predefined categories. 
The categories are:

['Grabs', 'Spins', 'Flips', 'Jumps', 'Slides', 'Buttering', 'Other']

For the trick provided, you will determine which categories each trick falls into and provide a binary indicator (1 or 0) for each category. A trick
can fall into multiple categories. 
If the trick provided is invalid or null, then the binary indicator should be set to 0 for each category. 


The output columns should be: 

['Trick Name','Grabs', 'Spins', 'Flips', 'Jumps', 'Slides', 'Buttering', 'Other']

You will return a table with one row. The table should be in a table format with a column for the trick and then a column for each category
and the values being 1 or 0 for all columns. Do not provide a text explanation, 
text introduction, or any text that doesn't belong in the table. Only return a table with a header and one row. 

"""

    user_prompt = """
    Please categorize the following snowboard trick: {transcript}
    """.format(transcript=transcript)
    
    
    
    completion = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
        temperature=.5,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,

    )

    formatted_table = format_table(completion.choices[0].message.content)
    
    trick_df = formatted_table
    trick_df = trick_df[['Trick Name','Grabs', 'Spins', 'Flips', 'Jumps', 'Slides', 'Buttering',
       'Other']]
    trick_df[['Grabs', 'Spins', 'Flips', 'Jumps', 'Slides', 'Buttering',
        'Other']]= trick_df[['Grabs', 'Spins', 'Flips', 'Jumps', 'Slides', 'Buttering',
        'Other']].apply(lambda row: pd.to_numeric(row,errors='coerce'),axis=0)

    return trick_df

def get_subcategories_dict():
    subcategories_dict = {
        'Slides': {'description':
    f"""Boardslide: Sliding with the board perpendicular to the rail.
    Lipslide: Approaching from the opposite side and sliding with the board perpendicular to the rail.
    50-50: Sliding straight along a rail with the board parallel.
    Nose Slide: Sliding on the nose of the board.
    Tail Slide: Sliding on the tail of the board.
    Blunt Slide: Sliding on the tail of the board with the nose raised.""",

    'columns': f"""[Trick Name, Boardslide, Lipslide, 50-50, Nose Slide, Tail Slide, Blunt Slide]"""},

        'Spins': {'description':
    f"""180: A half-spin, rotating 180 degrees.
    360: A full spin, rotating 360 degrees.
    540: A spin with one and a half rotations.
    720: A double spin with two full rotations.
    900: Two and a half rotations.
    1080: Three full rotations.
    1260: Three and a half rotations.
    1440: Four full rotations.
    1620: 4.5 rotations.
    1800: 5 rotations.
    1980: 5.5 rotations.
    2160: 6 rotations
    """,

    'columns': f"""[Trick Name, 180, 360, 540, 720, 900, 1080, 1260, 1440, 1620, 1800, 1980, 2160]"""},
    
    #removed grabs 
    #Indy: Grabbing the toe edge of the board between the bindings with the back hand.
    #Mute: Grabbing the toe edge of the board between the bindings with the front hand.
        
    'Grabs': {'description':
    f"""
    Stalefish: Grabbing the heel edge of the board between the bindings with the back hand.
    Melon: Grabbing the heel edge of the board between the bindings with the front hand.
    Tail Grab: Grabbing the tail of the board.
    Nose Grab: Grabbing the nose of the board.
    Method: Grabbing the heel edge of the board with the front hand while arching the back and extending the legs.
    Japan: Grabbing the toe edge of the board with the front hand while tucking the knees and rotating the board.
    Seatbelt: Grabbing the nose of the board with the back hand.
    Truck Driver: Grabbing the nose of the board with the front hand and the tail with the back hand simultaneously.""",

    'columns': f"""[Trick Name, Indy, Mute, Stalefish, Melon, Tail Grab, Nose Grab, Method, Japan, Seatbelt, Truck Driver]"""},

    'Flips': {'description':
    f"""Backflip: A backward somersault.
    Frontflip: A forward somersault.
    Double Backflip: Two backward somersaults.
    Double Frontflip: Two forward somersaults.
    Rodeo: A backward flip with a 180 or 540-degree spin.
    Misty: A forward flip with a 180 or 540-degree spin.
    Cork: An off-axis spin, where the boarder is tilted.
    Double Cork: A double off-axis spin.
    Wildcat: A backflip with a rotation around the snowboarder’s side.""",

    'columns': f"""[Trick Name, Backflip, Frontflip, Double Backflip, Double Frontflip, Rodeo, Misty, Cork, Double Cork, Wildcat]"""},

    'Jumps': {'description':
    f"""Ollie: Lifting the front foot, followed by the back foot, to jump.
    Nollie: Lifting the back foot, followed by the front foot, to jump.
    """,

    'columns': f"""[Trick Name, Ollie, Nollie]"""},

    'Buttering': {'description':
    f"""Nose Butter: Pressing down on the nose of the board while rotating the tail.
    Tail Butter: Pressing down on the tail of the board while rotating the nose.
    Nose Roll: A 180-degree rotation while buttering on the nose.
    Tail Roll: A 180-degree rotation while buttering on the tail.

    """,

    'columns': f"""[Trick Name, Nose Butter, Nose Roll, Tail Roll]"""}

    }
    return subcategories_dict

def get_scoring_dict():
    scoring_dict = {
    # Grabs
    'Indy': 100,
    'Mute': 100,
    'Stalefish': 150,
    'Melon': 150,
    'Tail Grab': 200,
    'Nose Grab': 200,
    'Method': 250,
    'Japan': 250,
    'Seatbelt': 300,
    'Truck Driver': 400,
    'Uncategorized_Grabs': 100,

    # Spins
    '180': 50,
    '360': 100,
    '540': 150,
    '720': 200,
    '900': 300,
    '1080': 400,
    '1260': 500,
    '1440': 600,
    '1620': 700,
    '1800': 800,
    '1980': 900,
    '2160': 1000,

    # Flips
    'Backflip': 200,
    'Frontflip': 200,
    'Double Backflip': 400,
    'Double Frontflip': 400,
    'Rodeo': 300,
    'Misty': 300,
    'Cork': 350,
    'Double Cork': 700,
    'Wildcat': 250,

    # Jumps
    'Ollie': 50,
    'Nollie': 50,

    # Slides and Grinds
    'Boardslide': 100,
    'Lipslide': 150,
    '50-50': 100,
    'Nose Slide': 150,
    'Tail Slide': 150,
    'Blunt Slide': 200,

    # Buttering
    'Nose Butter': 100,
    'Tail Butter': 100,
    'Nose Roll': 150,
    'Tail Roll': 150,

    # Uncategorized Tricks
    'Uncategorized_Grabs': 100,
    'Uncategorized_Spins': 50,
    'Uncategorized_Flips': 200,
    'Uncategorized_Jumps': 50,
    'Uncategorized_Slides': 100,
    'Uncategorized_Buttering': 100,

    'Other': 100
    }
    return scoring_dict



def subcategories_one_trick_table(trick_df,subcategories_dict,category):
    


    groq_client = Groq()
    
    subcategories_dict = get_subcategories_dict()
    subcategories_description = subcategories_dict[category]['description']
    subcategories_columns = subcategories_dict[category]['columns']
    
    
    
    transcript = trick_df[trick_df[category]==1].drop_duplicates(subset='Trick Name')['Trick Name']
    transcript = list(transcript)
    system_prompt = """
You are an AI trained to categorize snowboard tricks into predefined categories. 
The categories are:

{subcategories_description}


For the trick provided, you will determine which categories it falls into and provide a binary indicator (1 or 0) for each category. A trick
can fall into multiple categories. 
If the trick provided is invalid or null, then the binary indicator should be set to 0 for each category. 


The output columns should be: 

{subcategories_columns}
 
The output for each trick should be in a table format with a column for the trick and then a column for each category
and the values being 1 or 0 for all columns. 
Do not provide a text explanation or a text introduction. Only return a table with a header and one row.
If you receive an invalid input or an empty table, the value for each column should be 0. 



""".format(subcategories_description=subcategories_description, subcategories_columns=subcategories_columns)

    user_prompt = """
    Please categorize the following snowboard trick(s):

    [{transcript}]
    """.format(transcript=transcript)
    
    
    
    completion = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
        temperature=.5,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    
    formatted_table = format_table(completion.choices[0].message.content)
    numcols = [col for col in formatted_table.columns if 'Trick Name' not in col]
    dropcols = [col for col in formatted_table.columns if 'Unnamed' in col]
    sub_cols = [col for col in numcols if 'Unnamed' not in col]
    
    if 'Trick Name' not in formatted_table.columns:
        #this is an LLM error
        formatted_table['Trick Name'] = transcript
        print('added trick names')
        
    trick_df=trick_df.merge(formatted_table,on='Trick Name', how='left').fillna(0)
    trick_df[numcols] = trick_df[numcols].apply(lambda row: pd.to_numeric(row, errors='coerce'),axis=1).fillna(0)
    
    trick_df = trick_df.drop(columns=dropcols,errors='ignore')
    

    return trick_df, sub_cols

def add_subcategories_one_trick(trick_df):

    subcategories_dict = get_subcategories_dict()
    main_cats = list(subcategories_dict.keys())
    trick_df2 = trick_df.copy()


    cat_dict = {}

    for cat in main_cats:
        #print(cat)
        trick_df2, sub_cols = subcategories_one_trick_table(trick_df2,subcategories_dict=subcategories_dict,category=cat)
        cat_dict[cat] = sub_cols
        

    return trick_df2

def add_uncategorized_categories(trick_df2):
    """adds a column for tricks that fit a category but not a subcategory"""
    subcategories_dict = get_subcategories_dict()
    trick_df2 = trick_df2.fillna(0)
    for cat in list(subcategories_dict.keys()):
        try:
            sub_cols = cat_dict[cat]
            trick_df2['Uncategorized_'+cat] = trick_df2.apply(
            lambda row: 1 if row[cat] == 1 and all(row[sub_cols] == 0) else 0,
            axis=1)
        except:
            pass
    

    #get rid of the main categories. Now we only have subcategories    
    trick_df3 = trick_df2.drop(columns=list(subcategories_dict.keys()))
    return trick_df3

def filter_numeric_columns(trick_df3):
    # Select numeric columns
    numeric_cols = trick_df3.select_dtypes(include='number').columns

    # Always keep the 'Trick Name' column
    columns_to_keep = list(numeric_cols) + ['Trick Name'] if 'Trick Name' in trick_df3.columns else list(numeric_cols)

    # Filter the dataframe to keep only the selected columns
    filtered_df = trick_df3[columns_to_keep]
    
    return filtered_df


def get_scoring(trick_df3):
    """
    
    Args:
        trick_df3 (_type_): tricks dataframe with detected trip per subcategory
        scoring_dict (_type_): score per trick

    Returns:
        scoring_df: tricks dataframe with scores 
        
    Also applies multiplier for combos
    """
    
    scoring_dict = get_scoring_dict()
    trick_df3 = filter_numeric_columns(trick_df3)
    
    scoring_cols = list(trick_df3.columns.drop(['Trick Name']))
    trick_df3['num_tricks'] = trick_df3[scoring_cols].sum(axis=1)
    scoring_df = trick_df3.copy()
    
    for trick in scoring_cols:
        score = scoring_dict[trick]
        scoring_df[trick] = scoring_df[trick] * score

    multiplier = (np.maximum(scoring_df['num_tricks'],1) - 1)*0.5 + 1
    scoring_df['multiplier'] = multiplier
    scoring_df['score'] = scoring_df[scoring_cols].sum(axis=1)*multiplier
    
    #total score
    total_score = int(scoring_df['score'].sum())
    
    #summary
    scoring_summary = scoring_df.sort_values(by='score',ascending=False)[['Trick Name','score']]
    
    #best trick
    best_trick = scoring_df.sort_values(by='score',ascending=False).iloc[0,1:].drop('Trick Name',errors='ignore').reset_index()
    trick_name = scoring_df.sort_values(by='score',ascending=False).iloc[0,0]
    best_trick.columns = ['Trick','Score']
    best_trick= best_trick[best_trick['Score'] > 0]

    
    return scoring_df, scoring_summary, best_trick, total_score

def score_trick(input):
    trick_df = get_one_trick_categories(input)
    trick_df2 = add_subcategories_one_trick(trick_df)
    trick_df3 = add_uncategorized_categories(trick_df2)
    scoring_df, scoring_summary, best_trick, total_score = get_scoring(trick_df3)
    return scoring_df, scoring_summary, best_trick, total_score