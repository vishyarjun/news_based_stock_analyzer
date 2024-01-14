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

        article_1 = "Tech giant Apple Inc. reports record-breaking quarterly earnings, surpassing market expectations and driving stock prices to new highs. Investors express optimism for the company's future prospects."

        article_2 = "Alphabet Inc., the parent company of Google, faces a setback as regulatory concerns lead to a sharp decline in share prices. The market reacts negatively to uncertainties surrounding the company's antitrust issues."

        prompt = f"""
        Few-shot prompt:
        Task: Analyze the impact of the news on stock prices.
        Instructions: As a seasoned finance expert specializing in the Indian stock market, you possess a keen understanding \
        of how news articles can influence market dynamics. In this task, you will be provided with a news article \
        or analysis. Upon thoroughly reading the article, if it contains specific information about a company's \
        stock, please provide the associated Stock Symbol (NSE or BSE Symbol), the Name of the stock, and the \
        anticipated Impact of the news.The Impact value should range between -1.0 and 1.0, with -1.0 signifying \
        highly negative news likely to cause a significant decline in the stock price in the coming days/weeks, \
        and +1.0 representing highly positive news likely to lead to a surge in share price in the next few days/weeks.\
        Your response must be strictly in the JSON format.Consider the following factors while determining the impact: \
        The magnitude of the news, The sentiment of the news,Market conditions at the date of the news, Liquidity \
        of the stock, The sector in which the company operates, The JSON response should include the keys: symbol, \
        name, and impact. If the news is not related to the Indian stock market or any \
        specific Indian company, leave the values blank. Do not invent values; maintain accuracy and integrity in your response.\
        
         Examples:
        1. Article: "{article_1}"
        Response: {{"symbol": "AAPL", "name": "Apple Inc.", "impact": 0.9}}

        2. Article: "{article_2}"
        Response: {{"symbol": "GOOGL", "name": "Alphabet Inc.", "impact": -0.5}}

        3. Article: "{article}"
        Response: 
        """
        return prompt
    

    def summarize(self,full_news):
        template3 = f"You excel in succinctly summarizing business and finance-related news articles.\
        Upon receiving a news article, your objective is to craft a concise and accurate summary while \
        retaining the name of the company mentioned in the original article. The essence of the article \
        should be preserved in your summary. Summarized text should be less than length of original text\
        Please proceed with the provided full news article. {full_news}"
        try:
            defaults = { 'model': 'models/text-bison-001' }
            response = palm.generate_text(**defaults, prompt=template3)
            return response.result
        except Exception as e:
            print(e)
            return None
        

palm_interface=PalmInterface()
# news_article = """Crude oil exhibited significant volatility as prices surged following Iran's seizure of an oil tanker and the US launching an airstrike on Houthi-controlled areas, according to analysts. On Thursday, Iran seized a tanker carrying Iraqi crude bound for Turkey, retaliating against the US's confiscation of the same vessel and its oil last year, as reported by Iranian state media. 
# ‘’Anticipating ongoing geopolitical tensions, we project crude oil prices to remain volatile. Crude oil finds support in the range of $73.10–72.40, with resistance expected at $74.65–75.10 for the current session. In terms of Indian Rupees (INR), crude oil is supported at ₹5,940–5,870, while resistance is observed at ₹6,110–6,190,'' said Rahul Kalantri, VP Commodities, Mehta Equities Ltd."""

# print(palm_interface.prompt(news_article))