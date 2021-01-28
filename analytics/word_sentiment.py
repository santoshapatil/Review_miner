import matplotlib.pyplot as plt

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from textblob import TextBlob
from analytics.word_emotion import word_emo
from plots.word_mood_plot import word_mood_meter
from plots.word_emo_pie import word_feelings
def get_sentiment(text):
  blob = TextBlob(text)
  result = blob.sentiment.polarity
  return result


def word_senti(word,df):
    pol=df["text"].apply(get_sentiment)
    polarity=pol.mean()
    v=word_emo(df)
    # st.write("Vibe Score for the word",word)
    st.subheader("")
    w1,w2=st.beta_columns(2)
    w1.plotly_chart(word_mood_meter(word,polarity),use_container_width=True)
    w2.plotly_chart(word_feelings(word,v),use_container_width=True)
    

    
