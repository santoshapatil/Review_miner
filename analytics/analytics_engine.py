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

def delete_emoji(text):
  allchars = text
  emoji_list = [c for c in allchars if c in emoji.UNICODE_EMOJI]
  clean_text = ' '.join([st for st in text.split() if not any(i in st for i in emoji_list)])
  return clean_text

#def delete_notEnglish(text):
  #english_words = []
  #d = enchant.Dict("en_US")
  #clean_text=' '.join([x for x in text.split() if d.check(x)==True])
  #return clean_text
def delete_punctuation(text):
  clean_text=''.join([p for p in text if p not in string.punctuation])
  return clean_text


# definie function to delete stop words
def delete_stopwords(text):
  clean_text=' '.join([x for x in text.split() if x.lower() not in stopwords.words("english")])
  return clean_text


def stemming(text):
  text = text.split()
  words = ""
  for i in text:
    stemmer = SnowballStemmer("english")
    words =words + (stemmer.stem(i))+" "
  return words
def analyze_engine(Reviews):
   Reviews.dropna(subset=['Review_rating'], inplace=True)

   print("semoji,eng")
   Reviews['em_t']=Reviews['Review_title'].apply(delete_emoji)
   Reviews['em_b']=Reviews['Review_body'].apply(delete_emoji)


   print("end emoji,eng")
   #Reviews['cl_t']=Reviews['em_t'].apply(delete_notEnglish)
   #Reviews['cl_b']=Reviews['em_b'].apply(delete_notEnglish)

   ## duplicates below delete later
   Reviews['cl_t']=Reviews['em_t']
   Reviews['cl_b']=Reviews['em_b']



   print("seng")
   Reviews['cl_t'].replace('', np.nan, inplace=True)
   Reviews['cl_b'].replace('', np.nan, inplace=True)
   print("end emoji,eng")

   Reviews.dropna(subset=['cl_t'], inplace=True)
   Reviews.dropna(subset=['cl_b'], inplace=True)

   Reviews['cl_t']=Reviews['cl_t'].apply(delete_punctuation)
   Reviews['cl_b']=Reviews['cl_b'].apply(delete_punctuation)
   print("punctuation")
   Reviews['cl_t']=Reviews['cl_t'].apply(delete_stopwords)
   Reviews['cl_b']=Reviews['cl_b'].apply(delete_stopwords)
   print("stopwords")
   Reviews['cl_t']=Reviews['cl_t'].apply(stemming)
   Reviews['cl_b']=Reviews['cl_b'].apply(stemming)
   print("stem")
   Reviews['cl_t'].replace('', np.nan, inplace=True)
   Reviews['cl_b'].replace('', np.nan, inplace=True)

   Reviews.dropna(subset=['cl_t'], inplace=True)
   Reviews.dropna(subset=['cl_b'], inplace=True)

   all_words=list(Reviews['cl_t'])
   all_words=list(Reviews['cl_b'])

   counts_words = collections.Counter(all_words)

   st.subheader("Most Common Words")
   with st.beta_expander('Click to maximize-->'):
       st.beta_container():
       
       num=st.slider("No. of Frequent Words",min_value=5, max_value=20, value=5)

       words_df = pd.DataFrame(counts_words.most_common(num),
                             columns=['words', 'count'])
       st.dataframe(words_df)

   #st.subheader("Most Common Words by Year/Month")
   #with st.beta_expander('Click to maximize-->'):
       #options={'Year', 'Month'}
       #opt=streamlit.radio(label, options)



   #w=[]
   #def print_col(w,i):














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
