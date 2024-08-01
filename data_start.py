#from datasets import load_dataset
#ds = load_dataset("wikimedia/wit_base")
# this is too much data for my machine so I will read in from indicidual splits I downloaded 
import pandas as pd

import os
from groq import Groq

# Create the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"), )


system_prompt = {
    "role": "system",
    "content":
    "You will briefly answer the following summary questions given input. If a question cannot be answered from the text respond with NA. Seperate answers with ','. Who is the first person mentioned in the text? What role does that person have in relation to the title?"
}

# Initialize the chat history
chat_history = [system_prompt]

user_input = '''Scolopendra gigantea, also known as the Peruvian giant yellow-leg centipede or Amazonian giant centipede, is a centipede in the genus Scolopendra. It is the largest centipede species in the world, with a length exceeding 30 centimetres (12 in).[2] Specimens may have 21 or 23 segments.[3] It is found in various places throughout South America and the extreme south Caribbean, where it preys on a wide variety of animals, including other sizable arthropods, amphibians, mammals and reptiles.[4]
Distribution and habitat

It is naturally found in northern South America. Countries from which verified museum specimens have been collected include Aruba, Brazil, Curaçao, Colombia, Venezuela (including Margarita Island) and Trinidad.[2] Records from Saint Thomas, U.S. Virgin Islands, Hispaniola (both Haiti and the Dominican Republic), Mexico, Puerto Rico and Honduras are assumed to be accidental introductions or labelling errors.[2]

Scolopendra gigantea can be found in tropical or sub-tropical rainforest and tropical dry forest, in dark, moist places such as in leaf litter or under rocks.[3]
Behavior and diet

It is a carnivore that feeds on any other animal it can overpower and kill. It is capable of overpowering not only other invertebrates such as large insects, worms, snails, spiders, millipedes, scorpions, and even tarantulas, but also small vertebrates including small lizards, frogs (up to 95 millimetres (3+3⁄4 in) long), snakes (up to 25 centimetres (10 in) long), sparrow-sized birds, mice, and bats.[4][5] Large individuals of S. gigantea have been known to employ unique strategies to catch bats with muscular strength. They climb cave ceilings and hold or manipulate their heavier prey with only a few legs attached to the ceiling.[4] Natural predators to the giant centipedes include large birds, spiders, and arthropod-hunting mammals, including coati, kinkajou, and opossum.
Venom

At least one human death has been attributed to the venom of S. gigantea. In 2014, a four-year-old child in Venezuela died after being bitten by a giant centipede which was hidden inside an open soda can. Researchers at Universidad de Oriente later confirmed the specimen to be S. gigantea.[6] '''
chat_history.append({"role": "user", "content": user_input})
response = client.chat.completions.create(model="llama3-70b-8192",
                                            messages=chat_history,
                                            max_tokens=100,
                                            temperature=1.2)
print("Assistant:", response.choices[0].message.content)
df = pd.read_parquet('./train/train-00000-of-00330.parquet',engine='pyarrow')
print(df.columns)
print(df.embedding)
print(df.head())
