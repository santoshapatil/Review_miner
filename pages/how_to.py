import streamlit as st
import codecs
import streamlit.components.v1 as components
import os
def About():
    

    # f=codecs.open(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\pages\test.html")
    # bod= f.read()
    # st.beta_container():

    f=codecs.open(r"C:\Users\Linus\Documents\GitHub\Review_miner\pages\chetube.html")
    bod= f.read()


    st.subheader("")
    with st.beta_container():
          components.html(bod,height=1000,scrolling=True)
         
    st.write()

# About()