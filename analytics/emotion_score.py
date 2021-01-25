import text2emotion as te
import pandas as pd 

def get_emo(text):
  return te.get_emotion(text)

def emo_score(rev_data):
    rev_data["emotion"]= rev_data["text"].apply(get_emo)
    return rev_data
    
    
