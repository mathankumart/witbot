import os
import socket

import OpenSSL
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

def wit_access_token():
	"""
	Returns Wit.ai access token from environment

	:return: (string) Wit access token
	"""
	return os.environ.get('WIT_ACCESS_TOKEN')

def get_key(dictionary, key):
	"""
	Returns the key if it presents in dictionary else None

	:param dictionary: Input dictionary
	:param key: Key to retrieve from dictionary
	:return: (object) Key value
	"""
	if dictionary is None or key not in dictionary:
		return None
	return dictionary[key]

def first_entity_value(entities, entity):
	"""
	Returns the first entity value if present else None

	:param entities: Entity dictionary
	:param entity: Entity key to retrieve
	:return: (object)First value
	"""
	if entity not in entities:
		return None

	value = entities[entity][0]['value']
	if value is None:
		return None
	return value['value'] if isinstance(value, dict) else value

def http_request(url):
	"""
	Returns http response object of the given url

	:param url: URL to make http request
	:return: Response object
	"""
	headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0", "Accept-Encoding": "gzip, deflate, br"}
	try:
		result = requests.get(url, headers=headers, verify=False, timeout=3)
		return result
	except (requests.ConnectionError, requests.RequestException, requests.HTTPError, requests.URLRequired, requests.TooManyRedirects, requests.Timeout, OpenSSL.SSL.ZeroReturnError, socket.timeout, socket.error, OpenSSL.SSL.SysCallError):
		return None

def get_json(url):
	"""
	Returns json object of the given url

	:param url: JSON URL
	:return: (JSON) response
	"""
	response = http_request(url)
	if response is not None:
		return response.json()
	return None

def forecast(location):
	"""
	Returns the weather forecast of the given location

	:param location: Name of the city
	:return: (string)Weather forecast
	"""
	if location is None:
		return None

	yahoo_query = "https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22" + location + "%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys"
	response = get_json(yahoo_query)
	result = get_key(get_key(get_key(get_key(get_key(response, 'query'), 'results'), 'channel'), 'item'), 'forecast')
	if result is not None and len(result) > 0:
		return result[0]['text']
	else:
		return None

def wikipedia_description(name):
	"""
	Returns the wikipedia summary of the given name

	:param name: Name to search in wikipedia title
	:return: (string) wikipedia summary
	"""
	if name is None:
		return None

	wiki_query = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=" + name
	response = get_json(wiki_query)
	result = get_key(get_key(response, 'query'), 'pages')
	if result is None:
		return None
	for page in result:
		# Returning First page in the result
		return result[page]['extract']
