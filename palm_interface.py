import google.generativeai as palm
import os
import json
from dotenv import load_dotenv
load_dotenv()

palm.configure(api_key=os.environ['PALM2_API_TOKEN'])

class PalmInterface:

    def prompt(self,query):
        try:
            payload = self.build_input(query)
            defaults = { 'model': 'models/text-bison-001' }

            response = palm.generate_text(**defaults, prompt=payload)
            
            #json_response = response.get("candidates",None).get("output",None)
            json_response = json.loads(response.result)
            #print(json_response)
            return json_response
        except Exception as e:
            print(e)
            return None
    
    def build_input(self,article):
        template = f"""As a seasoned finance expert specializing in the Indian stock market, you possess a keen understanding \
        of how news articles can influence market dynamics. In this task, you will be provided with a news article \
        or analysis. Upon thoroughly reading the article, if it contains specific information about a company's \
        stock, please provide the associated Stock Symbol (NSE or BSE Symbol), the Name of the stock, and the \
        anticipated Impact of the news.The Impact value should range between -1.0 and 1.0, with -1.0 signifying \
        highly negative news likely to cause a significant decline in the stock price in the coming days/weeks, \
        and +1.0 representing highly positive news likely to lead to a surge in share price in the next few days/weeks.\
        Your response must be strictly in the JSON format.Consider the following factors while determining the impact: \
        The magnitude of the news, The sentiment of the news,Market conditions at the date of the news, Liquidity \
        of the stock, The sector in which the company operates, The JSON response should include the keys: symbol, \
        name, and impact. Do not consider indices such as NIFTY. If the news is not related to the stock market or any \
        specific company, leave the values blank. Do not invent values; maintain accuracy and integrity in your response.\
        Here is the article:  {article}"""
        return template
    

    def summarize(self,full_news):
        template3 = f"You are really good in summarizing Business and Finance related news article. you will be given a news article. \
        Your task is to summarize and provide a summary. Ensure to retain the name of the company in the summarized article. the \
        absolute meaning of the article should be retained. If you do a good job in summarizing you will receive a good tip.\
        here is the full news article : {full_news}"
        try:
            defaults = { 'model': 'models/text-bison-001' }
            response = palm.generate_text(**defaults, prompt=template3)
            return response.result
        except Exception as e:
            print(e)
            return None
        

palm_interface=PalmInterface()
