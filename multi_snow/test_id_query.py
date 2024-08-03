import pandas as pd
from multi_snow.get_video import get_video_data

df = pd.read_csv('output.csv')
trick_list = df['Trick'].toList()
query_id = []
thumb_url = []
for trick in trick_list:
    video_data = get_video_data(trick)
    if video_data is None:
        query_id.append(0)
        thumb_url.append(0)
    else:
        query_id = video_data['video_id']
        thumb_url = video_data['thumbnail_url']

df['query_id'] = query_id
df['thumbnail_url'] = thumb_url

print(df)
df.to_csv('tested.csv',index=False)
