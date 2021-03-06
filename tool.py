import os, re, sys, json, pprint
import environment

from facebook import GraphAPI, GraphAPIError
from socialscraper.facebook.graphapi import get_feed

from dateutil.parser import parse

FACEBOOK_USER_TOKEN = os.getenv('FACEBOOK_USER_TOKEN')

RELEVANT_STRINGS = [
	'textbook',
	'book'
]

regex = lambda test_string: re.compile(r'\b%s\b' % test_string, flags=re.I | re.U)

api = GraphAPI(FACEBOOK_USER_TOKEN)
try:
	api.get_object('me')
except GraphAPIError as e:
	print e
	print "Update your .secret file"
	sys.exit()

# Formatting/Tabbing to make the JSON data look good
pp = pprint.PrettyPrinter(indent=4)

# Take a post and traverse its message and comments
# while checking its relevancy
def check_relevant(item):

	def test_message_relevant(message):

		for test_string in RELEVANT_STRINGS:
			if regex(test_string).findall(message):
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

###############################################################
# Main code
###############################################################

if __name__ == "__main__":

	if len(sys.argv) == 1:
		start = None
		end = None
	elif len(sys.argv) == 3:
		start = parse(sys.argv[1])
		end = parse(sys.argv[2])
	else:
		print "usage: python tool.py 4-1-2014 4-2-2014"
		sys.exit()

	# start = parse("4-1-2014")
	# end = parse("4-2-2014")

	groups = [
		('Free and For Sale', '357858834261047'), 
		('Textbook Exchange', '357858800927717')
	]

	relevant_posts = []

	for group in groups:
		print "Scraping %s (%s)" % group
		for item in get_feed(api, group[1], start=start, end=end):
			is_relevant, message = check_relevant(item)
			print item['id'], item['created_time'], item['updated_time'], is_relevant
			if is_relevant: relevant_posts.append(item)

	# highlight the RELEVANT_STRINGS in relevant_posts
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
		blah += 	".comment { text-indent: 1em; }"
		blah += 	".author::after {content: ': '; padding-right: 5px; }"
		blah += "</style>"

		for post in relevant_posts:

			blah += "<div class='post'>"
			
			blah += "<div class='stamp'>"
			blah +=		"Location: %s <br>" % post['to']['data'][0]['name']
			blah += 	"Created: %s, Last Edited: %s" % (post["created_time"][:10], post["updated_time"][:10])
			blah += "</div>"

			blah += "<span class='author'>"
			blah += 	"<a href='https://www.facebook.com/%s'>" % post["from"]["id"]
			blah += 		post["from"]["name"]
			blah += 	"</a>"
			blah += "</span>"

			blah += "<span class='message'>"
			blah += 	"<a href='%s'>" % post['actions'][0]['link']
			blah += 		post['message']
			blah += 	"</a>"
			blah += "</span>"

			blah += "<div></div>"

			if post.get('comments'):
				for comment in post['comments']['data']:
					blah += "<div class='comment'>"

					blah += 	"<span class='author'>"
					blah += 		"<a href='https://www.facebook.com/%s'>" % post['from']['id']
					blah += 			post['from']['name']
					blah += 		"</a>"
					blah += 	"</span>"

					blah += 	comment['message']

					blah += "</div>"

			blah += "</div>"
			blah += "<hr>"
			
		f.write(blah.encode('utf-8', 'ignore'))

