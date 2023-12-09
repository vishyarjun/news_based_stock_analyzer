from news_api import news
import pandas as pd
from palm_interface import palm_interface
from yahoo_finance import yfi
import os
from datetime import date
from news_scrapper import factory
class NewsTrader:
    def __init__(self):
        self.strong_buy = []
        self.buy = []
        self.strong_sell = []
        self.sell = []

    def get_rsi(self, symbol):
        row = yfi.download_data(symbol,'./data/')
        if row is None:
            return 50.0
        else:
            return row['RSI14'] if row['RSI14'] else 50.0

    def run(self):
        results_list = []
        extracted_news_file = f'./data/news/{date.today()}.csv'
        df = pd.DataFrame()
        if os.path.exists(extracted_news_file):
            df = pd.read_csv(extracted_news_file)
        else:
            extracted_news_file = news.extract_news()
            df = pd.read_csv(extracted_news_file)
            
        
        if 'symbol' not in df:
            for index,row in df.iterrows():
                text = factory.create_and_scrape(row['URL'])
                if text is None or len(text)<10:
                    print('scrape not successful!')
                    text = str(row['Title']) + ' ' + str(row['Description'])
                #print(text)
                
                text = palm_interface.summarize(text)
                data = palm_interface.prompt(text)
                #print(index, data)
                results_list.append({
                'symbol': data['symbol'] if data else "",
                'name': data['name'] if data else "",
                'impact': data['impact'] if data else 0.0
                })
            df2 = pd.DataFrame(results_list)
            df = pd.concat([df, df2], axis=1)
            df.to_csv(extracted_news_file, index=False)

        for index, row in df.iterrows():
            if not pd.isna(row['symbol']) and len(row['symbol'])>0:
                rsi = self.get_rsi(row['symbol'])
                if row['impact'] > 0.4:
                    if rsi <=35:
                        self.strong_buy.append(row['symbol'])
                    else:
                        self.buy.append(row['symbol'])
                        
                elif row['impact'] < -0.4:
                    if rsi >=75:
                        self.strong_sell.append(row['symbol'])
                    else:
                        self.sell.append(row['symbol'])
        
        print(f'self.strong_buy - {self.strong_buy}')
        print(f'self.buy - {self.buy}')
        print(f'self.sell - {self.sell}')
        print(f'self.strong_sell - {self.strong_sell}')

nt = NewsTrader()
nt.run()













