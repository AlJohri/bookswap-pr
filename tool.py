import os, pprint
import environment

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook.graphapi import get_feed

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')

api = GraphAPI(FACEBOOK_USER_TOKEN)

pp = pprint.PrettyPrinter(indent=4)

for item in get_feed(api, '357858834261047'):
	print "-------------------------------------------------"
	print pp.pprint(item)
