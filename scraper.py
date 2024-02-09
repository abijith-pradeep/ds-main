import snscrape.modules.twitter as sntwitter
import pandas as pd
import time
from urlparse import urlparse, parse_qs
import sys
import csv
import tweepy
import datetime
from newspaper import Article
import urllib
import requests
from bs4 import BeautifulSoup

"""We search for tweets on Twitter by using the `Cursor()` function. 
We pass the `api.search` parameter to the cursor, as well as the query string, which is specified through the `q` parameter of the cursor.
The query string can receive many parameters, such as the following (not mandatory) ones:
* `from:` - to specify a specific Twitter user profile
* `since:` - to specify the beginning date of search
* `until:` - to specify the ending date of search
The cursor can also receive other parameters, such as the language and the `tweet_mode`. If `tweet_mode='extended'`, all the text of the tweet is returned, otherwise only the first 140 characters.
"""

"""Optionally, we can extract tweets from a given places, by specifying in the query string one of the following keywords, followed by `:`: 
* `place` - the place name or the place ID
* `place_country` - the country code. See [here](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) to see the country code
* `point_radius` - the circular geographic area within which to search for
* `bounding_box` - the 4 sided geographic area, within which to search for.
For more details, you can read the full [Twitter Documentation](https://developer.twitter.com/en/docs/tutorials/filtering-tweets-by-location).
Here 
"""

"""Now we loop across the `tweets_list`, and, for each tweet, we extract the text, the creation date, the number of retweets and the favourite count. We store every tweet into a list, called `output`."""
class scraper():
    self.TWITTER_CONSUMER_KEY = 'vLcxeGYqPTm2De02u5Fa0c2Zs'
    self.TWITTER_CONSUMER_SECRET = 'htu890Ysc8RCdN5eMkh25P6qDehVCbpAh0zNIKH8M55AK5RHqo'
    self.TWITTER_ACCESS_TOKEN = '108051742-qVpGsVGEpCTf7B5xvbNs5jYHuHKaAwlpmqQQVjgq'
    self.TWITTER_ACCESS_TOKEN_SECRET = 'goRE81O2jfuvtCGWWjspF7Fsibk3VUi2qApbJ3nZCb4l5'
    
    self.auth = tweepy.OAuth1UserHandler(self.TWITTER_CONSUMER_KEY, self.TWITTER_CONSUMER_SECRET,
                                    acess_token=self.TWITTER_ACCESS_TOKEN,
                                    access_token_secret=self.TWITTER_ACCESS_TOKEN_SECRET)
    
    self.api = tweepy.API(auth,wait_on_rate_limit=True)
    
    def gen_tweet(query):
        tweets_list = tweepy.Cursor(self.api.search, q=query,tweet_mode='extended', lang='en').items()
        output = []
        for tweet in tweets_list:
            text = tweet._json["full_text"]
            favourite_count = tweet.favorite_count
            retweet_count = tweet.retweet_count
            created_at = tweet.created_at
            
            line = {'text' : text, 'likes' : favourite_count, 'retweet_count' : retweet_count, 'created_at' : created_at}
            output.append(line)
        tweets_df = pd.DataFrame(output)
        tweets_df.to_csv('output.csv', mode='a', header=False)
        tweets_df.to_csv('output.csv')
        return tweets_df

#extracts all comments. no limit.
    def gen_youtube(URL,api_key):


        # empty list for storing reply
        replies = []

        if url.startswith(('youtu', 'www')):
            url = 'http://' + url
            
        query = urlparse(url)
        
        if 'youtube' in query.hostname:
            if query.path == '/watch':
                video_id = parse_qs(query.query)['v'][0]
            elif query.path.startswith(('/embed/', '/v/')):
                video_id = query.path.split('/')[2]
        elif 'youtu.be' in query.hostname:
            video_id = query.path[1:]
        else:
            raise ValueError

        # creating youtube resource object
        youtube = build('youtube', 'v3',
                        developerKey=api_key)
      
        # retrieve youtube video results
        video_response=youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id
        ).execute()
      
        # iterate video response
        while video_response:
            
            # extracting required info
            # from each result object 
            for item in video_response['items']:
                
                # Extracting comments
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                  
                # counting number of reply of comment
                replycount = item['snippet']['totalReplyCount']
      
                # if reply is there
                if replycount>0:
                    
                    # iterate through all reply
                    for reply in item['replies']['comments']:
                        
                        # Extract reply
                        reply = reply['snippet']['textDisplay']
                          
                        # Store reply is list
                        replies.append(reply)
      
                # print comment with list of reply
                if !replies:
                    print(comment, replies, end = '\n\n')
                else:
                    print(comment)
                # empty reply list
                replies = []
      
            # Again repeat
            if 'nextPageToken' in video_response:
                video_response = youtube.commentThreads().list(
                        part = 'snippet,replies',
                        videoId = video_id
                    ).execute()
            else:
                break
    #The lang parameter needs to give
    #The URL is for only one news article not all.
    def gen_news_article(url,lang):
        n_article = Article(url, language=lang)
        output=[]
        line={'title':n_article.title, 'textline': n_article.text,'keywords':t_article.keywords}
        output.append(line)
        n_df = pd.DataFrame(output)
        n_df.to_csv('output_article.csv', mode='a', header=False)
        n_df.to_csv('output_article.csv')
        return n_df
    
    #quora question and answer for multiple Urls
    def gen_quora(url_list):
        df_q = pd.DataFrame({'question': [],'answers':[]})
        for url in url_list:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            question = soup.find('span', {'class': 'ui_qtext_rendered_qtext'})
            answers = soup.find_all('div', attrs={'class': 'ui_qtext_expanded'})
            for answer in answers:
                df_q = df_q.append({'question': question.text,'answers': answer.text
                               }, ignore_index=True)
            df_q.to_csv('output_quora.csv')
        return df_q
    
    
    
    def run_scraper(strin):
        if strin=="YouTube":
            URL,api=input("Please provide the URL and API key").split()
            gen_youtube(URL,api)
        elif strin=="Twitter":
            query=input("Please provide the twitter keyword query")
            gen_tweet(query)
        elif strin=="News":
            url,lang=input("Please provide URL(s) and Language").split()
            gen_news_article(url,lang)
        elif strin=="Quora":
            url_list=input("Enter URLs spaced with a comma").split(",")
            gen_quora(url_list)
        else:
            print("Invalid scraper method given")
