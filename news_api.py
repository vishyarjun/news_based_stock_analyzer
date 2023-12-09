import os
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
from datetime import datetime, timedelta
import requests
import pandas as pd
from datetime import date
from newsapi import NewsApiClient

class NewsApi:
    def __init__(self):
        self.token = os.getenv("NEWS_API_TOKEN")
        self.country = 'in'
        self.category='business'
        self.csv_location = './data/news/'
        self.filename = f'{date.today()}.csv'
        self.newsapi = NewsApiClient(api_key=self.token)


    def extract_news(self):
        page = 1 
        total_news_count = 0
        all_articles = []
        try:
            while True:
                top_headlines = self.newsapi.get_top_headlines(
                                            country=self.country,
                                            language='en',
                                            category=self.category,
                                            page=page
                                            )
                if top_headlines.get('status')=='ok':
                    for row in top_headlines.get("articles",None):
                        article = [row['publishedAt'],row['title'],row['description'],row['url']]
                        all_articles.append(article)
                page+=1
                
                if len(all_articles)>=top_headlines['totalResults']:
                    break
            self.all_articles = pd.DataFrame(all_articles,columns=['Date','Title','Description','URL'])
            self.all_articles.to_csv(f'{self.csv_location}{self.filename}')
            return f'{self.csv_location}{self.filename}'
        except Exception as e:
            print(e)


news = NewsApi()
#news.extract_news()



