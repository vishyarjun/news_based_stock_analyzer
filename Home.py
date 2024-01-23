import streamlit as st
from datetime import datetime, date
import pandas as pd
import os
from news_tech_trader import nt
import time

st.set_page_config(layout="wide")
bgs = [
    "#8B0000","#B22222","#DC143C","#FF4500", "#FF6347","#FF7F50","#FFA07A","#FFD700", "#ADFF2F","#008000"
]

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def delete_historical_data():
    folder_path = './data/'  # Replace with your folder path
    # Get a list of all files in the folder
    files = os.listdir(folder_path)
    # Iterate through the files and delete if the file is a CSV file
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)

def get_data_frame(file_name):
    df = pd.read_csv(file_name)
    if 'ImageURL' not in df.columns:
        df['ImageURL'] = None
    
    if 'recommendation' not in df.columns:
        df['recommendation'] = None
    
    if 'PRICE_AT_TIME' not in df.columns:
        df['PRICE_AT_TIME'] = None
    else:
        df = df[df['PRICE_AT_TIME'].notna()]
    df = df.sort_values(by='impact', ascending = False)
    return df

local_css('./styles.css')
def display_news_cards(selected_date):
    col1, col2, col3 = st.columns(3)
    cols = [col1, col2, col3]   
    file_name = f'./data/news/{selected_date}.csv'
    if os.path.exists(file_name):
        df = get_data_frame(file_name)
        chunk_size = 3
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
                                    <p class="sentiment">AI Sentiment(ranges from -1 to 1): {row['impact']}</p>
                                    <p class="sentiment">AI Recommendation: {row['recommendation']}</p>
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


but_click = st.button(f'Download Latest {date.today()}')
if but_click:
    d = None
    progress_bar()
    d = date.today()
    but_click = False

d = st.date_input(label=":blue[Select a date]",format="YYYY-MM-DD")
if d:
    with st.expander("News"):
        display_news_cards(d)
