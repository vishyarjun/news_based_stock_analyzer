import yfinance as yf
from datetime import datetime, timedelta, date
from tech_analysis import TA
import pandas as pd
import os

class YahooFinanceInterface:
    def __init__(self):
        self.interval = '1d'
        self.period  = '1y'
        self.file_path = f'./data/historical/analysis/'
        
    
    def get_default_data(self,yahoo_symbol):
        sym = yf.Ticker(yahoo_symbol)
        his = sym.history(interval=self.interval, period=self.period)
        return his

    def get_dated_data(self,yahoo_symbol, start_date):
        print(f'download starting {start_date}')
        sym = yf.Ticker(yahoo_symbol)
        his = sym.history(interval=self.interval, start=start_date)
        return his

    
    def convert_to_epoch(self, given_date):
        unix_epoch_time = int(datetime.combine(given_date, datetime.now().time()).timestamp())
        return unix_epoch_time
    



    def download_data(self, symbol, location):
        if not symbol.endswith('.NS'):
            symbol+='.NS'
        full_path = f'{location}/{symbol}.csv'
        
        if not os.path.exists(location):
            os.makedirs(location)
        
        if not os.path.exists(full_path):
            his = self.get_default_data(symbol)
            his.columns = his.columns.str.upper()
            his['SYMBOL'] = symbol
            his = his.rename_axis(index={'Date': 'TIMESTAMP'})
        else:
            existing_data = pd.read_csv(full_path, index_col='TIMESTAMP', parse_dates=True)
            last_date = existing_data.index[-1] + timedelta(days=1)
            if last_date.date() >= date.today():
                return None
            his = self.get_dated_data(symbol,last_date)
            his.columns = his.columns.str.upper()
            his['SYMBOL'] = symbol
            his = his.rename_axis(index={'Date': 'TIMESTAMP'})
            his = pd.concat([existing_data, his])
        
        
        
        if not his.empty and len(his)>=50:
            his = TA.calculate_technicals(his)
            his.to_csv(full_path)
            return his.iloc[-1]
        else:
            return None

yfi = YahooFinanceInterface()