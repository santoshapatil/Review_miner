#display Result
import pandas as pd
import streamlit as st
import numpy as np
from datetime import date
def show(data):
    d=data
    cnt_rev=len(d)
    st.write("Extracted a total of ",cnt_rev)
    startd=d['Review_date'].iloc[0]
    lastd=d['Review_date'].iloc[-1]
    sd=date(day=startd.day, month=startd.month, year=startd.year).strftime('%d %B %Y')
    ld=date(day=lastd.day, month=lastd.month, year=lastd.year).strftime('%d %B %Y')
    st.write("Extracted Reviews from "+sd+" to "+ld)
    return
    
