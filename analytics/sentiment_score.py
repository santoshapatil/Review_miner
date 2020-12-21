from textblob import TextBlob
import pandas as pd

def get_sentiment(text):
  blob = TextBlob(text)
  result = blob.sentiment.polarity
  return result

def sentiment_par(Rev_data):
    Rev_data["Polarity"]=Rev_data["text"].apply(get_sentiment)
    return Rev_data
