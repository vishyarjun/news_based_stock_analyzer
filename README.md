# News bases Stock Recommender
This simple app leverages the ability of News Aggregation Services and combining it with Large Language Models to gather sentiments and combine it with Technicals and Fundamentals to build a Stock recommender System.

## Prerequisites
1. Python Virtual Environment - Follow this [simple guide](https://medium.com/datacat/a-simple-guide-to-creating-a-virtual-environment-in-python-for-windows-and-mac-1079f40be518) to create a virtual environment.
2. NEWS API TOKEN - Follow this [simple guide](https://newsapi.org/) to get the API token
3. Google PALM2 API Token - Follow this [simple guide](https://developers.generativeai.google/models/language) to the paLM2 API token.

## Installation
1. Create and Enter into your virtual environment.
2. cd to the root directory of the application.
3. Install the dependencies using following command `pip3 install -r requirements.txt`.
4. Create a .env file on the directory and Make sure to set your API keys on the .env file.

```sh
python3 news_tech_trader.py
```