import utils


def send(request, response):
	"""
	Prints the response in the console
	"""
	print response['text']

def wikipedia_description(request):
	"""
	Returns the context to wit.ai with description key in success scenario or invalid_name, missing_name based on the sorrow cases

	:param request: dict('context', 'entities') from wit.ai server
	:return: request with updated context
	"""
	context = request['context']
	entities = request['entities']

	wikipedia_title = utils.first_entity_value(entities, 'contact')
	if wikipedia_title is not None:
		result = utils.wikipedia_description(wikipedia_title)
		if result is None:
			context['invalid_name'] = True
		else:
			context['description'] = result
	else:
		context['missing_name'] = True
	return context

def forecast(request):
	"""
	Returns the context to wit.ai with forecast key in success scenario or invalid_location, missing_location based on the sorrow cases

	:param request: dict('context', 'entities') from wit.ai server
	:return: request with updated context
	"""
	context = request['context']
	entities = request['entities']

	location = utils.first_entity_value(entities, 'location')
	if location is not None:
		result = utils.forecast(location)
		if context.get('missing_location') is not None:
			del context['missing_location']
		if result is None:
			context['invalid_location'] = True
		else:
			context['forecast'] = result
	else:
		context['missing_location'] = True
	return context
