import requests
import os
import json
from typing import Dict
key = os.environ.get("TWELVE_LABS_API_KEY")

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
	

if __name__ == "__main__":
	index_map = get_indicies()
	get_videos(index_map)
