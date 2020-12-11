
from bs4 import BeautifulSoup
import requests
import streamlit as st
import os, base64


#from flask import Flask, render_template, url_for, request

#nltk.download('stopwords')



from ext.amzengine import Review_extract as amz
from disp.showdisp import show as DB
from analytics.analytics_engine import analyze_engine
from sessions.session import session_id
from sessions.action import action_log
from sessions.Review_db import rev_warehouse
#from pages.home import home_page
def main():
    go=1
    lid,l_date_time=session_id(go)
    st.title("Review Miner  ")
    #st.text("By Santosh A Patil")
    pages = ["Home","How to"]
    page = st.sidebar.selectbox("Select Page",pages,key="page")

    st.sidebar.title("Key Idea")
    st.sidebar.info(
    """
        Know what people felt about what you are about to buy

    """
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This a Web ML App to help you make a data driven decision before you
        click purchase button while shopping online.
        We sincerely thank Amazon,Flipkart and other digital market places
        to let this app get reviews from their website."

        """
        )
    st.sidebar.title("Key Idea")
    st.sidebar.info(
        """
        Know what people felt about what you are about to buy

        """
        )



    if page == "Home":
        #st.text("https://www.amazon.in/Brayden-Portable-Blender-Rechargeable-Transparent/dp/B07NS898HJ/ref=cm_cr_arp_d_product_top?ie=UTF8")
        marketplace = ["amazon.in","flipkart.in","swiggy.com","zomato.com","oyorooms.com","rottentomatoes.com","mynrta.com"]
        c1,c2,c3 = st.beta_columns((1,3,1))
        with c1:
            choice = st.selectbox("Select Marketplace",marketplace,key="marketplace")
        with c2:
            product_url = st.text_input("Enter The Product url [Eg:https://www.amazon.in/dp/B07JWV47JW]")
        with c3:
            st.button('Analyze Reviews',key="go")



    if choice == "amazon.in":
        st.subheader("Amazon.in")
        if st.button('Analyze Reviews') == "go":
            if "amazon.in" in product_url:
                with st.spinner('Crawling Amazon to get reviews'):
                    data=amz(product_url)
                    st.success('Extrction Complete!')
                    action_log(lid,choice,product_url)
                    #(lid,product_url,l_date_time,data)
                    DB(data)
                    analyze_engine(data)
                    rev_warehouse(product_url,l_date_time,data)



            else:
                st.text("Enter a amazon.in starting product URL")
        else:
            st.write("Press the above button..")


if __name__ == '__main__':
	main()
