import os
import environment

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook.graphapi import get_feed

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')

api = GraphAPI(FACEBOOK_USER_TOKEN)

get_feed(api, '357858834261047')