import matplotlib.pyplot as plt

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from textblob import TextBlob

from plots.mood_plot import mood_meter
def get_sentiment(text):
  blob = TextBlob(text)
  result = blob.sentiment.polarity
  return result


def word_senti(word,df):
    pol=df["text"].apply(get_sentiment)
    polarity=pol.mean()
    st.write("Vibe Score for the word",word)
    st.subheader("")
    with st.beta_container():
        st.plotly_chart(mood_meter(polarity),use_container_width=True)

    

    
