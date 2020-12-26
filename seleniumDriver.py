
import time
import random

from selenium import webdriver
from selenium.webdriver.common.keys import Keys



def getSearchBody(url, browser):
        browser.get(url)
        browser.execute_script("document.body.style.zoom='50%'")
        time.sleep(1)

        body = browser.find_element_by_tag_name('body')
        bodylen = [1,2,3,4,5]
        i = 0
        while 1 == 1:
        try:
                	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                	sleepamt = float("{0:.2f}".format(random.uniform(0.5,0.8)))
                	time.sleep(sleepamt)
                	body_len = len(body.get_attribute('innerHTML'))
                	i = i + 1
                	bodylen[(i%5)] = body_len
                	if all(x == bodylen[0] for x in bodylen):
        break
		except:
			try: 
        			browser.get(url)
        			browser.execute_script("document.body.style.zoom='50%'")
				time.sleep(2)
                		browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                		sleepamt = float("{0:.2f}".format(random.uniform(0.5,0.8)))
                		time.sleep(sleepamt)
                		body_len = len(body.get_attribute('innerHTML'))
                		i = i + 1
                		bodylen[(i%5)] = body_len
                		if all(x == bodylen[0] for x in bodylen):
                        		break
			except:
				pass 
			
        body = body.get_attribute('innerHTML')
        return body


def getTweetsBody(twitterHandle, browser):
        base_url = u'https://twitter.com/'
        end_url = u'/with_replies'
        url = base_url + twitterHandle + end_url

        browser.get(url)
        browser.execute_script("document.body.style.zoom='50%'")
        time.sleep(1)

        body = browser.find_element_by_tag_name('body')
        bodylen = [1,2,3,4,5]
        i = 0
        while 1 == 1:
               
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleepamt = float("{0:.2f}".format(random.uniform(2.0,3.0)))
                time.sleep(sleepamt)
                body_len = len(body.get_attribute('innerHTML'))
                i = i + 1
                bodylen[(i%5)] = body_len
                if all(x == bodylen[0] for x in bodylen):
                        break
        body = body.get_attribute('innerHTML')
        return body
 

def getFollowingBody(twitterHandle,browser):

        base_url = u'https://twitter.com/'
        end_url = u'/following'
        url = base_url + twitterHandle + end_url

        browser.get(url)
        browser.execute_script("document.body.style.zoom='50%'")
        time.sleep(1)

        body = browser.find_element_by_tag_name('body')

        bodylen = [1,2,3,4,5]
        i = 0
        while 1 == 1:
              
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleepamt = float("{0:.2f}".format(random.uniform(0.8,2.6)))
                time.sleep(sleepamt)
                body_len = len(body.get_attribute('innerHTML'))
                i = i + 1
                bodylen[(i%5)] = body_len
                if all(x == bodylen[0] for x in bodylen):
                        break

        body = body.get_attribute('innerHTML')
        return body

def getFollowersBody(twitterHandle,browser):

        base_url = u'https://twitter.com/'
        end_url = u'/followers'
        url = base_url + twitterHandle + end_url

        browser.get(url)
        browser.execute_script("document.body.style.zoom='50%'")
        time.sleep(1)
        body = browser.find_element_by_tag_name('body')

        bodylen = [1,2,3,4,5]
        i = 0
        while 1 == 1:
               
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleepamt= float("{0:.2f}".format(random.uniform(1.0,2.0)))
                time.sleep(sleepamt)
                body_len = len(body.get_attribute('innerHTML'))
                i = i + 1
                bodylen[(i%5)] = body_len
                if all(x == bodylen[0] for x in bodylen):
                        break

        body = body.get_attribute('innerHTML')
        return body

