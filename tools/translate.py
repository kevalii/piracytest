import requests
from os import environ

def get_translated(text):
	url = f"https://api.funtranslations.com/translate/pirate.json?text={text}"
	headers = {'X-FunTranslations-Api-Secret': environ.get('API-KEY', None)}
	request = requests.get(url, headers=headers).json()
	return request['contents']['translated']