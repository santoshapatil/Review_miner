import os, base64
import pandas as pd
import datetime
import string
import random
#from datetime import date
def id_generator():
    idd=''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    idd=str(idd)
    return idd

def session_id(go):

    #idd=''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    #idd=str(idd)
    #today = date.today()
    #today_time= date.today()
    #log_df=pd.DataFrame(columns={"session_id","session_time"},index=None)
    log_df=pd.read_csv(r"log_df.csv",index_col=False)
    idd=id_generator()
    print(idd)
    #idd not in log_df["session_id"]:
    noww = datetime.datetime.now()
    noww=str(noww)
    fg={'session_id': [idd], 'session_time': [noww]}
    log_df.loc[len(log_df["session_id"])]=fg

    #df=pd.DataFrame(fg)
    #log_df.merge(df)
        #log_df["session_id"]=log_df["session_id"].join(idd)
        #log_df["session_time"]=log_df["session_time"].join(noww)
    log_df.to_csv("log_df.csv",index=False)
    return idd,noww



    #print(idd.dty
    #log_df=pd.DataFrame(columns={"session_id","session_time"})
