import emoji
import nltk
#import enchant
import pandas as pd
from dateutil.parser import parse
import numpy as np
from nltk.corpus import stopwords
import streamlit as st
import pickle
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from sklearn.naive_bayes import MultinomialNB
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
#from sklearn.externals import joblib
import string
import time
import collections
from textblob import TextBlob
from spellchecker import SpellChecker
from autocorrect import Speller
from ipywidgets import widgets
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
spell=Speller(lang='en')
#from autocorrect import spell
check = Speller(lang='en')
#streamlit run analytics_engine.py
#spell = SpellChecker()
#from temp.temp_data import temp_data
from analytics.vibe_meter import vibe_plot
from analytics.sentiment_score import sentiment_par
from analytics.word_sentiment import word_senti
from analytics.emotion_score import emo_score
import plotly.graph_objects as go
import numpy as np

#del this
#from vibe_meter import vibe_plot
#from sentiment_score import sentiment_par
#from word_sentiment import word_senti
#


#del after checking
from textblob import TextBlob


def get_sentiment(text):
  blob = TextBlob(text)
  result = blob.sentiment.polarity
  return result


def delete_emoji(text):
  allchars = text
  emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
  clean_text = ' '.join([str for str in text.split() if not any(i in str for i in emoji_list)])
  return clean_text

#def delete_notEnglish(text):
  #english_words = []
  #d = enchant.Dict("en_US")
  #clean_text=' '.join([x for x in text.split() if d.check(x)==True])
  #return clean_text
def delete_punctuation(text):
  clean_text=''.join([p for p in text if p not in string.punctuation])
  return clean_text

#st.cache()
#def spelling_correction(text):
    #print(text)
    #if check(text):
        #print("correct")
        #return text
    #else:
        #print("incorrect")
        #clean_text =spell(text)
        #print(clean_text)
        #return clean_text

# definie function to delete stop words
def delete_stopwords(text):
  clean_text=' '.join([x for x in text.split() if x.lower() not in stopwords.words("english")])
  return clean_text


def stemming(text):
  text = text.split()
  words = ""
  for i in text:
    stemmer = PorterStemmer()
    words =words + (stemmer.stem(i))+" "
    return words

def spli_words(text):
  return text.split()

def word_list(counts_words):
  return counts_words

@st.cache(persist=True, allow_output_mutation=True)
def analyze_engine(Reviews):
  
   Reviews.dropna(subset=['Review_rating'], inplace=True)
   # review later *Review rating is removed*


   Reviews["text"] = Reviews[['Review_title','Review_body']].apply(lambda x: ' '.join(x), axis=1)
   Reviews['Review_date']= pd.to_datetime(Reviews['Review_date'])
   print("semoji,eng")
  #  Reviews["text"]=Reviews['text'].apply(delete_emoji)
   Reviews['text']=Reviews['text'].apply(delete_punctuation)
   Reviews['text'].replace('', np.nan, inplace=True)
   Reviews.dropna(subset=['text'], inplace=True)
   Reviews['text']=Reviews['text'].apply(stemming)
   Reviews['text'].replace('', np.nan, inplace=True)
   Reviews.dropna(subset=['text'], inplace=True)

  #  #Reviews['cl_t']=Reviews['em_t'].apply(delete_notEnglish)
  #  #Reviews['cl_b']=Reviews['em_b'].apply(delete_notEnglish)
  #  ## duplicates below delete later

  #  #remove emoji
  #  Reviews['em_t']=Reviews['Review_title'].apply(delete_emoji)
  #  Reviews['em_b']=Reviews['Review_body'].apply(delete_emoji)
  #  Reviews['cl_t']=Reviews['em_t']
  #  Reviews['cl_b']=Reviews['em_b']

  #  #preform punctuations delete
  #  Reviews['cl_t']=Reviews['cl_t'].apply(delete_punctuation)
  #  Reviews['cl_b']=Reviews['cl_b'].apply(delete_punctuation)
  #  print("punctuation")
  #  #to perform spelling check
  #  #Reviews['cl_t']=Reviews['cl_t'].apply(spelling_correction)
  #  #Reviews['cl_b']=Reviews['cl_b'].apply(spelling_correction)

  #  Reviews['cl_t'].replace('', np.nan, inplace=True)
  #  Reviews['cl_b'].replace('', np.nan, inplace=True)
  #  print("end emoji,eng")

  #  Reviews.dropna(subset=['cl_t'], inplace=True)
  #  Reviews.dropna(subset=['cl_b'], inplace=True)



  #  print("stopwords")
  #  Reviews['cl_t']=Reviews['cl_t'].apply(stemming)
  #  Reviews['cl_b']=Reviews['cl_b'].apply(stemming)
  #  print("stem")
  #  Reviews['cl_t'].replace('', np.nan, inplace=True)
  #  Reviews['cl_b'].replace('', np.nan, inplace=True)

  #  Reviews.dropna(subset=['cl_t'], inplace=True)
  #  Reviews.dropna(subset=['cl_b'], inplace=True)

   #all_words=list(Reviews['cl_t'])
   #all_words=list(Reviews['cl_b'])
   
   Reviews["words"]=Reviews["text"].apply(spli_words)
   rev_data=pd.DataFrame()
   rev_data["words"]=Reviews["words"]
   rev_data["Review_date"]=Reviews["Review_date"]
   rev_data["text"] = Reviews[['Review_title','Review_body']].apply(lambda x: ' '.join(x), axis=1)
   rev_data=sentiment_par(rev_data)
   print("emostart")
   rev_data=emo_score(rev_data)
   print("emodone")
   return rev_data

       


     
   #else :
     #st.text("Enter a valid word.")

   
#Reviews=pd.read_csv(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\reviews.csv")
#analyze_engine(Reviews)













   #return 1
   #count_vector = CountVectorizer()
   #count_t=count_vector.fit_transform(Reviews['cl_t'])
   #count_b=count_vector.fit_transform(Reviews['cl_b'])

   #words =' '.join(Reviews['cl_b'])
   #wordcloud = WordCloud().generate(words)
   #plt.imshow(wordcloud,interpolation='bilinear')
   #plt.axis("off")
   #plt.show()
   #st.pyplot(plt)
#d=pd.read_csv(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\reviews.csv")
#x=analyze_engine(d)
#print(x)
