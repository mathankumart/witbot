from wit import Wit

import actions
import utils

if __name__ == "__main__":
	actions = {
		'send': actions.send,
		'find_weather': actions.forecast,
		'wiki_desc': actions.wikipedia_description,
	}

	client = Wit(access_token=utils.wit_access_token(), actions=actions)
	client.interactive()
