
import requests
import re
import datetime
import datetime as dt

from bs4 import BeautifulSoup
from bs4.builder._lxml import LXML
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from seleniumDriver import *



def getTwitterFeed(twitterHandle):
        base_url = u'https://twitter.com/'
        url = base_url + twitterHandle 
        r = requests.get(url)
        return r.text



def getAccountStatus(soups):
	accountStatus = soups.findAll('div', {'class': "ProtectedTimeline"})
	return accountStatus



def getJoinDate(soup):
	joindate=''
        spans= soup.findAll('span')
        for s in spans:
                if s.has_attr('class'):
                        if 'ProfileHeaderCard-joinDateText' in s['class']:
                                sDict = s.attrs 
                                joindate = sDict.get('title') 
	if joindate == '':
		joindate= 'unknown'
	return joindate



def getTweetsAmmount(soup):
	number=''
        As= soup.findAll('a')
        for a in As:
                if a.has_attr('class'):
                        if 'ProfileNav-stat' in a['class'] and 'js-nav' in a['class']:
                                aDict = a.attrs 
                                number = aDict.get('title') 
				number = number.split(" ", 1)
				number = number[0]
	if number == '':
		number= 'unknown'
	return number



def getTweetLis(soup):
	tweetLis= ['N/A']
        tweetFound = False
        lis = soup.findAll('li')
        for li in lis:
                if li.has_attr('class'):
                        if 'js-stream-item' in li['class']:
                                if tweetFound == False:
                                        tweetFound = True
                                        tweetLis.pop(0)
                                tweetLis.append(li)
        return tweetLis



def getTweetsPerRange(soup):
	tweetLis= ['N/A']
        tweetFound = False
        lis = soup.findAll('li')
        for li in lis:
            if li.has_attr('class'):
                        if 'stream-item' in li['class']:
                                if tweetFound == False:
                                        tweetFound = True
                                        tweetLis.pop(0)
                                tweetLis.append(li)
        return len(tweetLis)

def tweetType(li):
	if li == 'N/A':
		return li
        divs= li.findAll('div')
        for div in divs:
                if div.has_attr('data-retweet-id'):
                        return "Retweet"
        for div in divs:
                if div.has_attr('class'):
                        if 'QuoteTweet' in div['class']:
                                return 'Quote'
        allAs = li.findAll('a')
        for div in divs:
                if div.has_attr('class'):
                        if 'withheld-tweet' in div['class']:
                                return 'WithheldTweet'
        for a in allAs:
                if a.has_attr('class'):
                        if 'twitter-atreply' in a['class']:
                                return "Reply"
        return "Tweet"

def getTimeStamp(li):
	if li == 'N/A':
                return li
        allAs= li.findAll('a')
        for a in allAs:
                if a.has_attr('class'):
                        if 'tweet-timestamp' in a['class']:
                                aDict = a.attrs 
                                timestamp = aDict.get('title')
                                return timestamp


def getTweetID(li):
	if li == 'N/A':
                return li
        tweetID = 'N/A'
        divs = li.findAll('div')
        for div in divs:
                if div.has_attr('class'):
                        if 'original-tweet' in div['class']:
                                divDict = div.attrs 
                                tweetID = divDict.get('data-tweet-id')
                                tweetID = str(tweetID)
        return tweetID

def getTweetText(li):
	if li == 'N/A':
                return li
        ps = li.findAll('p')
        content = ''
        for p in ps:
                if p.has_attr('class'):
                        if 'tweet-text' in p['class']:
                                for contentItem in p.contents:
                                        filteredContent= re.sub(r"<.*?>", "", str(contentItem))
                                        filteredContent= re.sub(r"\n", "<newline>", str(filteredContent))
                                        filteredContent= re.sub(r'"', "<quote>", str(filteredContent))
                                        content= content + filteredContent
        return content

def getTweetUrl(li):
	if li == 'N/A':
                return li
        tweetKind = tweetType(li)
        tweetUrl = 'N/A'
        if tweetKind == 'Retweet':
                allAs= li.findAll('a')
                for a in allAs:
                        if a.has_attr('class'):
                                if 'tweet-timestamp' in a['class']:
                                        aDict = a.attrs
                                        tweetUrl = aDict.get('href') 
        if tweetKind == 'Quote':
                divs = li.findAll('div')
                for div in divs:
                        if div.has_attr('class'):
                                if 'QuoteTweet-innerContainer' in div['class']:
                                        divDict = div.attrs
                                        tweetUrl = divDict.get('href')
        return tweetUrl
def getHandle(li):
	if li == 'N/A':
                return li
        tweetKind = tweetType(li)
        tweetHandle = 'N/A'
        if tweetKind == 'Retweet':
                divs = li.findAll('div')
                for div in divs:
                        if div.has_attr('class'):
                                if 'original-tweet' in div['class']:
                                        divDict = div.attrs 
                                        tweetHandle = divDict.get('data-screen-name') 
        if tweetKind == 'Quote':
                divs = li.findAll('div')
                for div in divs:
                        if div.has_attr('class'):
                                if 'QuoteTweet-innerContainer' in div['class']:
                                        divDict = div.attrs
                                        tweetHandle = divDict.get('data-screen-name')
        if tweetKind == 'Reply':
                divs = li.findAll('div')
                for div in divs:
                        if div.has_attr('class'):
                                if 'js-profile-popup-actionable' in div['class']:
                                        divDict = div.attrs
                                        tweetHandle = divDict.get('data-mentions')
        return tweetHandle


def getLanguage(li):
	if li == 'N/A':
                return li
	lang = ''
        ps = li.findAll('p')
        for p in ps:
                if p.has_attr('lang'):
                        pattrs = p.attrs
                        lang = (pattrs.get('lang'))
			break
	if lang == '':
		lang = 'N/A'
	return lang
	

def getReplies(li):
	if li == 'N/A':
                return li
	replies = ''
        pattern1 = re.compile('.*repl.*')
        spans = li.findAll('span')
        for span in spans:
                if span.has_attr('class'):
                        if 'ProfileTweet-actionCountForAria' in span['class'] and pattern1.match(span.contents[0]):
                                replies = span.contents[0]
                                replies = replies.rsplit(' ',1)[0]
                       		break
	if replies == '':
		replies = 'N/A'
	return replies 

def getRetweets(li):
	if li == 'N/A':
                return li
	retweets = ''
        pattern1 = re.compile('.*retw.*')
        spans = li.findAll('span')
        for span in spans:
                if span.has_attr('class'):
                        if 'ProfileTweet-actionCountForAria' in span['class'] and pattern1.match(span.contents[0]):
                                retweets = span.contents[0]
                                retweets = retweets.rsplit(' ',1)[0]
				break
	if retweets == '':
		retweets = 'N/A'
	return retweets



def getLikes(li):
	if li == 'N/A':
                return li
	likes = ''
        pattern1 = re.compile('.*like.*')
        spans = li.findAll('span')
        for span in spans:
                if span.has_attr('class'):
                        if 'ProfileTweet-actionCountForAria' in span['class'] and pattern1.match(span.contents[0]):
                                likes = span.contents[0]
                                likes = likes.rsplit(' ',1)[0]
				break
	if likes == '':
		likes = 'N/A'
	return likes