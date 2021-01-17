import streamlit as st
import codecs
import streamlit.components.v1 as components
import os
def About():
    

    f=codecs.open(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\pages\test.html")
    bod= f.read()
    # st.beta_container():
    st.subheader("")
    with st.beta_container():
          components.html(bod,width=100,height=1000,scrolling=True)
         
    

About()