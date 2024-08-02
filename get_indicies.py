import requests
import json

url = "https://api.twelvelabs.io/v1.2/indexes?page=1&page_limit=10&sort_by=created_at&sort_option=desc"

headers = {
    "accept": "application/json",
    "x-api-key": "tlk_1DFFA7P17P2G9G289EBM33Q40FR2",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

response_dict = json.loads(response.text)
index_data = response_dict['data']
index_name_id_map = {}


for entry in index_data:
	index_name_id_map[entry['index_name']] = entry['_id']


print(index_name_id_map)
