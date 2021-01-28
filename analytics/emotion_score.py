import text2emotion as te
import pandas as pd 

def get_emo(text):
  return te.get_emotion(text)

def emo_score(rev_data):
    rev_data["emotion"]= rev_data["clean_text"].apply(get_emo)
    rev_data=rev_data.join(pd.json_normalize(rev_data['emotion']))
    return rev_data
    
    
