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

    def get_rsi_close(self, symbol):
        
        row = yfi.download_data(symbol,'./data/')
        
        if row is None:
            return None,None
        else:
            return row['RSI14'] if row['RSI14'] else 50.0, row['CLOSE']
    
    def delete_historical_data(self):
        folder_path = './data/'  # Replace with your folder path
        # Get a list of all files in the folder
        files = os.listdir(folder_path)
        # Iterate through the files and delete if the file is a CSV file
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(folder_path, file)
                os.remove(file_path)

    def generate_recommendation(self, df):
        df['recommendation'] = 'N/A'
        for index, row in df.iterrows():
            sym = row['symbol']
            if not pd.isna(row['symbol']) and len(row['symbol'])>0:
                rsi,close = self.get_rsi_close(row['symbol'])
                if rsi is not None:
                    if 'PRICE_AT_TIME' not in df.columns:
                        df['PRICE_AT_TIME'] = None
                        df['RSI_AT_TIME'] = None
                    df.loc[index,'PRICE_AT_TIME'] = close
                    df.loc[index,'RSI_AT_TIME'] = rsi
                    
                    if row['impact'] >= 0.4:
                        if rsi <=35:
                            self.strong_buy.append(row['symbol'])
                            df.loc[index,'recommendation'] = "STRONG BUY"
                        else:
                            self.buy.append(row['symbol'])
                            df.loc[index,'recommendation'] = "BUY"
                            
                    elif row['impact'] <= -0.4:
                        if rsi >=75:
                            self.strong_sell.append(row['symbol'])
                            df.loc[index,'recommendation'] = "STRONG SELL"
                        else:
                            self.sell.append(row['symbol'])
                            df.loc[index,'recommendation'] = "SELL"
        return df

    def run(self, day):
        results_list = []
        day = date.today() if not day else day
        extracted_news_file = f'./data/news/{day}.csv'
        df = pd.DataFrame()
        if not os.path.exists(extracted_news_file):
            extracted_news_file = news.extract_news()
        df = pd.read_csv(extracted_news_file)
        yield 5,"Download Completed.."
        df_len = len(df)
        i = 0
        if 'symbol' not in df:
            for index,row in df.iterrows():
                text = factory.create_and_scrape(row['URL'])
                if text is None or len(text)<10:
                    text = str(row['Title']) + ' ' + str(row['Description'])  
                text = palm_interface.summarize(text)
                data = palm_interface.prompt(text)
                symbol = yfi.get_symbol_from_name(data['name'],data['symbol']) if data else ""
                results_list.append({
                'symbol': symbol if symbol else "",
                'name': data['name'] if data else "",
                'impact': data['impact'] if data else 0.0
                })
                i+=1
                percentage = i/df_len*100
                yield int(percentage), "Scrapping and AI Analyzing in progress..."
            df2 = pd.DataFrame(results_list)
            df = pd.concat([df, df2], axis=1)

        yield 100, "Generating Recommendations"
        if 'PRICE_AT_TIME' not in df.columns:   
            df = self.generate_recommendation(df)
            df.to_csv(extracted_news_file, index=False)
        self.delete_historical_data()
        
        print(f'self.strong_buy - {self.strong_buy}')
        print(f'self.buy - {self.buy}')
        print(f'self.sell - {self.sell}')
        print(f'self.strong_sell - {self.strong_sell}')

nt = NewsTrader()
#nt.run(date.today())













