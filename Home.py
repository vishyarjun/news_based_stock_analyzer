import streamlit as st
from datetime import datetime, date
import pandas as pd
import os
from news_tech_trader import nt
import time

st.set_page_config(layout="wide")
col1, col2, col3 = st.columns(3)

cols = [col1, col2, col3]

bgs = [
    "#8B0000",  # Dark Red
    "#B22222",
    "#DC143C",
    "#FF4500",  # Orange-Red
    "#FF6347",
    "#FF7F50",
    "#FFA07A",
    "#FFD700",  # Gold
    "#ADFF2F",  # Green-Yellow
    "#008000"   # Dark Green
]

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css('./styles.css')
def extract_news_from_date(selected_date):
    file_name = f'./data/news/{selected_date}.csv'
    file_name
    if os.path.exists(file_name):
        df = pd.read_csv(file_name)
        if 'ImageURL' not in df.columns:
            df['ImageURL'] = None
        
        if 'recommendation' not in df.columns:
            df['recommendation'] = None
        
        if 'PRICE_AT_TIME' not in df.columns:
            df['PRICE_AT_TIME'] = None
        else:
            df = df[df['PRICE_AT_TIME'].notna()]
        chunk_size = 3
        df = df.sort_values(by='impact', ascending = False)
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size].reset_index(drop=True)
            for idx, row in chunk.iterrows():
                with cols[idx]:
                    new_value = int((row['impact'] + 1) * 50)
                    disp = new_value - (new_value%10)
                    bg = bgs[disp//10]
                    container = st.container()
                    container.markdown(
                        f"""
                            <div class="card">
                                <img src={row['ImageURL']} alt="News Image">
                                <div class="content">
                                    <h2><a href="{row['URL']}" target="_blank">{row['Title']}</a></h2>
                                    <p class="organization">{row['name']} - {row['symbol']}</p>
                                    <p class="sentiment">AI Sentiment: {row['recommendation']}</p>
                                </div>
                                <div class="sentiment-container">
                                    <!-- Sentiment Fill -->
                                    <div class="sentiment-slider" style="width: {disp}%; background-color:{bg};"></div>  
                                </div>
                            </div>""", unsafe_allow_html=True)
                
    else:
        st.text_area(label="Empty data display",value="No Data Available.",label_visibility="collapsed")
        
def progress_bar():
    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete,progress_text in nt.run(date.today()):
        time.sleep(0.01)
        my_bar.progress(percent_complete, text=progress_text)
    time.sleep(1)
    my_bar.empty()



if st.button(f'Download Latest {date.today()}'):
    d = None
    progress_bar()
    d = date.today()
d = st.date_input(label=":blue[Select a date]",value="today",format="YYYY-MM-DD")
if d:
    extract_news_from_date(d)


