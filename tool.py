import os
from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook.facebook.graphapi.feed import get_feed

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')

api = GraphAPI(FACEBOOK_USER_TOKEN)
