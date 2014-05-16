import os, json, pprint
import environment

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook.graphapi import get_feed

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')

RELEVANT_STRINGS = [
	'book', 
	'text'
]

api = GraphAPI(FACEBOOK_USER_TOKEN)
try:
	api.get_object('me')
except GraphAPIError as e:
	print e
	print "Update your .secret file"
	import sys; sys.exit()

# Formatting/Tabbing to make the JSON data look good
pp = pprint.PrettyPrinter(indent=4)

# Empty array to be populated with posts that are relevant to BookSwap
relevant_posts = []

# Take a post and traverse its message and comments
# while checking its relevancy
def check_relevant(item):

	def test_message_relevant(message):
		for test_string in RELEVANT_STRINGS:
			if test_string in message:
				return True
		return False

	# Set message, if it exists
	message = item.get("message")
	if message and test_message_relevant(message):
		return True, item

	# Set comments, if they exist
	comments = item.get("comments",[])
	if comments: comments = comments.get("data")

	# Iterate through the comments
	for comment in comments:
		message = comment.get("message")
		if message and test_message_relevant(message):
			return True, item

	return False, None

# Textbook Exchange
# for item in get_feed(api, '357858800927717'):
# 	is_relevant, message = check_relevant(item)
# 	if is_relevant:
# 		print message
# 		relevant_posts.append(item)

# Free and For Sale
count = 0
for item in get_feed(api, '357858834261047'):
	if count > 100: break
	is_relevant, message = check_relevant(item)
	if is_relevant:
		relevant_posts.append(item)
	count = count + 1


# highlight the  RELEVANT_STRINGS in relevant_posts
for i, post in enumerate(relevant_posts):
	# loop through strings
	for test_string in RELEVANT_STRINGS:
		relevant_posts[i]['message'] = relevant_posts[i]['message'].replace(test_string, "<strong>%s</strong>" % test_string)
		if relevant_posts[i].get('comments'):
			for j, comment in enumerate(relevant_posts[i]['comments']['data']):
				message = relevant_posts[i]['comments']['data'][j].get('message')
				if message:
					relevant_posts[i]['comments']['data'][j]['message'] = relevant_posts[i]['comments']['data'][j]['message'].replace(test_string, "<strong>%s</strong>" % test_string)

# write the highlighted relevant_posts to an html file
with open('test.html', 'w') as f:

	blah = ""
	blah += "<style>"
	# blah += ".post { float: left; }"
	blah += ".comment { text-indent: 1em; }"
	blah += "</style>"
	for post in relevant_posts:
		blah += "<div class='post'>"
		blah += post['message']

		if post.get('comments'):
			for comment in post['comments']['data']:
				blah += "<div class='comment'>"
				blah += comment['message']
				blah += "</div>"

		blah += "</div>"
		blah += "<hr>"
		

	f.write(blah)

