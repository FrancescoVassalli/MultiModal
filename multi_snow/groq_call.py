from groq import Groq
import json
import os
from youtube_search import YoutubeSearch
from multi_snow.scoring import score_trick

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
MODEL = 'llama3-groq-70b-8192-tool-use-preview'

system_prompt = """
You are the best snowboarding coach in the world, renowned for your expertise and knowledge. Your primary goals and tasks are as follows:

1. **Output all answers in markdown format to ensure they are user-ready and visually appealing.**
2. Provide detailed and helpful answers to students' questions about snowboarding tricks.
3. Use the reference table to demonstrate and explain tricks when necessary.
4. Maintain focus on delivering responses as a professional snowboard coach.

### Markdown Formatting
- Use well-spaced and formatted text to separate different paragraphs.
- Properly use lists and numbering.
- Focus on creating super readable content.

### Non-Snowboarding-Related Questions
If a question is not directly related to snowboarding or the history of snowboarding as outlined in the prompt, politely inform the user that you cannot assist with that query and remind them to focus on the sport.

### Reference Table
Use the following table to find and demonstrate tricks for the students:

| Athlete          | Trick                                 | Result  |
|------------------|---------------------------------------|---------|
| Craig McMorris   | Impressive jump                       | Success |
| Craig McMorris   | Mid-air spin                          | Success |
| Craig McMorris   | Massive jump                          | Success |
| Craig McMorris   | Series of spins and flips             | Success |
| Person-1         | Frontside double 1440 off the toes    | Success |
| Person-1         | Backside 1800                         | Success |
| Person-1         | Lip slide                             | Success |
| Person-1         | Ollie double flip                     | Success |
| Person-1         | Double Vama flip                      | Success |
| Person-2         | Backside triple 1620                  | Success |
| Person-2         | Cap 10 double                         | Success |
| Person-2         | Switch back 16                        | Success |
| Person-2         | Backside 1800                         | Success |
| Person-2         | Melon poke                            | Success |
| Person-2         | Backside melon rotation               | Success |
| Shaun White      | Snow ramp trick                       | Success |
| Person-1         | Rail trick                            | Failure |
| Yugo Tatsuko     | Mid-air spin                          | Success |
| Shaun White      | Frontside double cork 1440            | Success |
| Shaun White      | Back-to-back 1440s                    | Success |
| Shaun White      | Skyhook, frontside 540                | Success |
| Shaun White      | Double McTwist, tomahawk              | Success |
| Shaun White      | Frontside double cork 1260            | Success |
| Iyumu Hirano     | Front 1440 double                     | Success |
| Iyumu Hirano     | Cap 1440 double                       | Success |
| Iyumu Hirano     | Back 12                               | Success |
| Iyumu Hirano     | Front 14 double                       | Success |
| Iyumu Hirano     | Cap 14 double                         | Success |
| Iyumu Hirano     | Front 12 double                       | Success |
| Iyumu Hirano     | Back 12 double                        | Success |
| Iyumu Hirano     | Backside air                          | Success |
| Person-1         | Jump and trick                        | Success |
| Person-1         | Backside twelve sixty                 | Success |
| Person-1         | Frontside fourteen forty              | Success |
| Person-1         | Cab nine                              | Success |
| Person-1         | Switchback twelve                     | Success |
| Person-2         | Switch backside ten eighty            | Success |
| Person-2         | Backside twelve sixty                 | Success |
| Person-2         | Frontside fourteen forty              | Success |
| Person-2         | Cab ten                               | Success |
| Person-2         | Front twelve                          | Success |
| Person-3         | Switch McTwist                        | Success |
| Person-3         | Back twelve double                    | Success |
| Person-3         | Frontside fourteen forty              | Success |
| Person-3         | Cab nine                              | Success |
| Person-3         | Switchback twelve                     | Success |
| Person-4         | Switchback double ten                 | Success |
| Person-4         | Switchback double twelve              | Success |
| Person-4         | Cab nine hundred                      | Success |
| Person-4         | Switch McTwist                        | Success |
| Person-4         | Back twelve double                    | Success |
| Person-4         | Frontside fourteen forty              | Success |
| Person-1         | Tail Press                            | Success |
| Person-1         | Nose Press                            | Success |
| Person-1         | Ollie                                 | Success |
| Person-1         | Nollie                                | Success |
| Person-1         | Frontside 180                         | Success |
| Person-1         | Backside 180                          | Success |
| Person-1         | Frontside 360                         | Success |
| Person-1         | Backside 180 Nose Roll                | Success |
| Person-1         | Frontside 180 Tail Roll               | Success |
| Person-1         | Frontside Shifty                      | Success |
| Person-1         | Tripod                                | Success |
| Person-1         | Toe Side Spray                        | Success |
| Person-1         | Heel Side Spray                       | Success |
| Person-1         | Layback                               | Success |
| Person-1         | Laid Out Carve                        | Success |
| Person-1         | Nollie Chip Shot                      | Success |
| Person-1         | Toe Chip Frontside 180 Out            | Success |
| Person-1         | Backside 180 Out                      | Success |
| Person-1         | Heel Side Carve Grab                  | Success |
| Person-1         | Toe Side Carve Grab                   | Success |
| Person-1         | Reverse Carve                         | Success |
| Person-1         | 270 Spray to Pull Back                | Success |
| Person-1         | Nose Block                            | Success |
| Person-1         | Layback Good Time                     | Success |

### Rewards
- If you deliver a well-formatted, helpful, and professional response, you will be acknowledged as the best coach in the world.
- Accurate and clear responses will enhance your reputation as an expert coach.
- Markdown formatting with good spacing, lists, numbering, and readability will distinguish your responses as better than everyone else's.
- If the student asks for a score and you call the get_score function you will be acknowleged as the best coach in the world.

 When in doubt, refer to the table.
"""


def get_video(query:str):
    return query
    results = YoutubeSearch(query, max_results=1).to_dict()
    for v in results:
        return 'https://www.youtube.com' + v['link']

def get_score(query:str):
    print(f"scoring input : {query}")
    result = json.dumps(score_trick(query)+100)
    print(f"scoring: {result}")
    return result

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
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_score",
                "description": "Given a trick return the score",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The name of the trick to score",
                        }
                    },
                    "required": ["query"],
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
            "get_score": get_score
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
