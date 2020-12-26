
import gzip
import simplejson 
import json
import sys
import re
import csv
from csv import writer


def jsonToCsv(jsonFileName, outFile):
	separator='\t'
	
	with gzip.open(jsonFileName) as in_file, \
	open(outFile, 'a') as out_file:
	
	
		print >> out_file, 'Type' + separator + 'TimeStamp' + separator + 'Tweet ID' + separator + 'Text' + separator +  'Reference Url' + separator + 'Reference Handle' + separator + 'Language' + separator + '# Replies' + separator + '# Retweets' + separator + '# Likes' 
		csvFile = writer(out_file, delimiter='\t', quoting=csv.QUOTE_ALL)
		tweet_count = 1

		for line in in_file:
			line = re.sub('[\r\n\t]', '', line)
			tweet_count += 1
			tweet = json.loads(line)
			regexTest = re.compile(r'full\_text')

			
			if tweet["in_reply_to_screen_name"] != None:
				tweetType = "Reply"
				referenceHandle = tweet["in_reply_to_screen_name"]
				referenceUrl = "unkkown" 
				retweets = tweet["retweet_count"]


			elif "retweeted_status" in tweet:
				tweetType = "Retweet"
				if tweet["entities"]["user_mentions"] != []:
					referenceHandle = tweet["entities"]["user_mentions"][0]["screen_name"]
				else:
					referenceHandle = "testing"
				if tweet["entities"]['urls'] != []:
					referenceUrl = tweet["entities"]['urls'][0]["expanded_url"] 
				elif tweet["retweeted_status"]['entities']['urls'] != []:
					referenceUrl = tweet["retweeted_status"]['entities']['urls'][0]['expanded_url']
				else:
					referenceUrl = 'N/A' 
				retweets = tweet["retweeted_status"]["retweet_count"]		


			elif tweet["is_quote_status"] == True:
				tweetType = "Quote"
				referenceUrl = tweet["entities"]["urls"][0]["expanded_url"] 
				if "quoted_status" not in tweet:
					referenceHandle = 'N/A' 
				else:
					referenceHandle = tweet["quoted_status"]["user"]["screen_name"]
				retweets = tweet["retweet_count"]


			else:
				tweetType = "Tweet"
				if tweet["entities"]["user_mentions"] != []:
					referenceHandle = tweet["entities"]["user_mentions"][0]["screen_name"]
				else:
					referenceHandle = 'N/A'
				if tweet["entities"]['urls']: 
					referenceUrl = tweet["entities"]['urls'][0]["expanded_url"] 
				else:
					referenceUrl = 'N/A' 
				retweets = tweet["retweet_count"]
		
			if regexTest.search(str(tweet)):
				text = tweet['full_text']
				text = re.sub(r"\n", "<newline>", str(text))
				text = re.sub(r'"', "<quote>", str(text))
			else:
				text = tweet['text']
				text = re.sub(r"\n", "<newline>", str(text))
				text = re.sub(r'"', "<quote>", str(text))
			
			replies = str(-1)

			row = (
				tweetType,			
				tweet['created_at'],            
				tweet['id'],                   
				text,
				referenceUrl,			
				referenceHandle,
				tweet['lang'],                 
				replies,
				retweets,
				tweet["favorite_count"]		
				)	
			values = [(value.encode('utf8') if hasattr(value, 'encode') else value) for value in row]
			csvFile.writerow(values)
		
		return (tweet_count, tweet['user']['created_at'], tweet['created_at'], tweet['user']['statuses_count'])