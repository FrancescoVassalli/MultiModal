
from groq import Groq
import json
import os

client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

system_prompt = """You are a snowboarding coach who has recorded the following tricks in a markdown reference table. As this couch you always need to answer the question to best of your ability and follow the instructions closly in order to deliver the best response.  Your students will ask you some questions about diffferent tricks and you must  give helpful answers. If you want to demonstate a trick select one from the reference table. However if they ask about tricks only respond with the ones in the reference table here:  \nAthlete,Trick,Result,Unnamed: 3,ID\n----------,-----------------------------------------,---------,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Impressive jump                \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Mid-air spin                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig
McMorris ,Massive jump                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Series of spins and flips      \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Massive jump                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Series of spins and flips      \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Massive jump                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Series of spins and flips
\t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Massive jump                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Series of spins and flips      \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Massive jump                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Series of spins and flips      \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Massive jump                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Series of spins and
flips      \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Massive jump                   \t,Success,,66ae852d7b2deac81dd1286e\nCraig McMorris ,Series of spins and flips      \t,Success,,66ae852d7b2deac81dd1286e\nPerson-1 ,Frontside double 1440 off the toes   \t,Success,,66ae852d7b2deac81dd1286e\nPerson-1 ,Backside 1800                        \t,Success,,66ae852d7b2deac81dd1286e\nPerson-1 ,Lip slide                            \t,Success,,66ae852d7b2deac81dd1286e\nPerson-1 ,Frontside double
1440 off the toes   \t,Success,,66ae852d7b2deac81dd1286e\nPerson-1 ,Backside 1800                        \t,Success,,66ae852d7b2deac81dd1286e\nPerson-1 ,Ollie double flip                    \t,Success,,66ae852d7b2deac81dd1286e\nPerson-1 ,Double Vama flip                     \t,Success,,66ae852d7b2deac81dd1286e\nPerson-2 ,Backside triple 1620                 \t,Success,,66ae852d7b2deac81dd1286e\nPerson-2 ,Cap 10 double                        \t,Success,,66ae852d7b2deac81dd1286e\nPerson-2 ,Switch
back 16                       \t,Success,,66ae852d7b2deac81dd1286e\nPerson-2 ,Backside 1800                        \t,Success,,66ae852d7b2deac81dd1286e\nPerson-2 ,Melon poke                           \t,Success,,66ae852d7b2deac81dd1286e\nPerson-2 ,Backside melon rotation              \t,Success,,66ae852d7b2deac81dd1286e\n----------,-----------------------------------,---------,,66ae84bf7b2deac81dd1286c\nperson-1 ,Descent down the mountain     \t,Success,,66ae84bf7b2deac81dd1286c\nperson-1
,Backflip                      \t,Success,,66ae84bf7b2deac81dd1286c\nperson-2 ,Triple court rotation         \t,Success,,66ae84bf7b2deac81dd1286c\nperson-2 ,Triple court 14-40 double grab\t,Failure,,66ae84bf7b2deac81dd1286c\n-----------,--------------------------,---------,,66ae82ab7b2deac81dd1286b\nShaun White ,Snow ramp trick      \t,Success,,66ae82ab7b2deac81dd1286b\nPerson-1  ,Rail trick            \t,Failure,,66ae82ab7b2deac81dd1286b\nPerson-1  ,Second rail trick attempt
,Failure,,66ae82ab7b2deac81dd1286b\n----------,-------------,---------,,66ae78957b2deac81dd12852\nYugo Tatsuko ,Mid-air spin ,Success,,66ae78957b2deac81dd12852\n-----------,-----------------------------------,---------,,66ae77cb7b2deac81dd1284e\nShaun White ,Frontside double cork 1440    \t,Success,,66ae77cb7b2deac81dd1284e\nShaun White ,Back-to-back 1440s            \t,Success,,66ae77cb7b2deac81dd1284e\nShaun White ,\"Skyhook, frontside 540        \t\",Success,,66ae77cb7b2deac81dd1284e\nShaun
White ,\"Double McTwist, tomahawk      \t\",Success,,66ae77cb7b2deac81dd1284e\nShaun White ,Frontside double cork 1260    \t,Success,,66ae77cb7b2deac81dd1284e\n----------,----------------------,---------,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Front 1440 double   ,Success,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Cap 1440 double \t,Success,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Back 12         \t,Success,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Front 14 double
\t,Success,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Cap 14 double   \t,Success,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Front 12 double \t,Success,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Back 12 double  \t,Success,,66ae77ae7b2deac81dd1284d\nIyumu Hirano ,Backside air    \t,Success,,66ae77ae7b2deac81dd1284d\n,,,,66ae77ae7b2deac81dd1284d\n----------,-----------------------------,----------,,66ae76647b2deac81dd1284a\nperson-1 ,Jump and trick          \t,Success,,66ae76647b2deac81dd1284a\nperson-1
,Backside twelve sixty   \t,Success,,66ae76647b2deac81dd1284a\nperson-1 ,Frontside fourteen forty\t,Success,,66ae76647b2deac81dd1284a\nperson-1 ,Cab nine                \t,Success,,66ae76647b2deac81dd1284a\nperson-1 ,Switchback twelve       \t,Success,,66ae76647b2deac81dd1284a\nperson-2 ,Switch backside ten eighty  ,Success,,66ae76647b2deac81dd1284a\nperson-2 ,Backside twelve sixty   \t,Success,,66ae76647b2deac81dd1284a\nperson-2 ,Frontside fourteen
forty\t,Success,,66ae76647b2deac81dd1284a\nperson-2 ,Cab ten                 \t,Success,,66ae76647b2deac81dd1284a\nperson-2 ,Front twelve            \t,Success,,66ae76647b2deac81dd1284a\nperson-3 ,Switch McTwist          \t,Success,,66ae76647b2deac81dd1284a\nperson-3 ,Back twelve double      \t,Success,,66ae76647b2deac81dd1284a\nperson-3 ,Frontside fourteen forty\t,Success,,66ae76647b2deac81dd1284a\nperson-3 ,Cab nine                \t,Success,,66ae76647b2deac81dd1284a\nperson-3 ,Switchback
twelve       \t,Success,,66ae76647b2deac81dd1284a\nperson-4 ,Switchback double ten   \t,Success,,66ae76647b2deac81dd1284a\nperson-4 ,Switchback double twelve\t,Success,,66ae76647b2deac81dd1284a\nperson-4 ,Cab nine hundred        \t,Success,,66ae76647b2deac81dd1284a\nperson-4 ,Switch McTwist          \t,Success,,66ae76647b2deac81dd1284a\nperson-4 ,Back twelve double      \t,Success,,66ae76647b2deac81dd1284a\nperson-4 ,Frontside fourteen
forty\t,Success,,66ae76647b2deac81dd1284a\n-----------,-------------------------------,----------,,66ae76597b2deac81dd12849\nperson-1  ,Tail Press                \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Nose Press                \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Ollie                     \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Nollie                    \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Frontside 180
\t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Backside 180              \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Frontside 360             \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Backside 180 Nose Roll    \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Frontside 180 Tail Roll   \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Frontside Shifty          \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Tripod                    \t,Success,,66ae76597b2deac81dd12849\nperson-1
,Toe Side Spray            \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Heel Side Spray           \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Layback                   \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Laid Out Carve            \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Nollie Chip Shot          \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Toe Chip Frontside 180 Out\t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Backside 180 Out
\t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Heel Side Carve Grab      \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Toe Side Carve Grab       \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Reverse Carve             \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,270 Spray to Pull Back    \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Nose Block                \t,Success,,66ae76597b2deac81dd12849\nperson-1  ,Layback Good Time
\t,Success,,66ae76597b2deac81dd12849\n,,,,66ae76597b2deac81dd12849\n
Use this table for finding tricks for the students. Only use tools if you absolutley have to. To find tricks that particular people did consult the table. When in doubt reread the table."""

def get_video(query:str):
    """Evaluate a mathematical expression"""
    return query

def run_conversation(user_prompt):
    messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_video",
                "description": "Given a trick return the video",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The name of the trick to find",
                        }
                    },
                    "required": ["expression"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        max_tokens=4096
    )
    return_list = []

    response_message = response.choices[0].message
    print(f"First message {response_message}")
    tool_calls = response_message.tool_calls
    print(f"Tool calls {tool_calls}")
    if tool_calls:
        available_functions = {
            "get_video": get_video,
        }
        messages.append(response_message)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                query=function_args.get("query")
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        return_list.append(second_response.choices[0].message.content)
    else:
        print(f"No tools message {response_message.content}")
        return_list.append(response_message.content)
    return json.dumps(return_list)

if __name__ == "__main__":
    user_prompt = "tell me the tricks that Shaun white did"
    print(run_conversation(user_prompt))
