
from bs4 import BeautifulSoup
import requests
import streamlit as st
import os, base64


#from flask import Flask, render_template, url_for, request

#nltk.download('stopwords')



from ext.amzengine import Review_extract as amz
from ext.flipkartengine import Review_extract as flipkart
from disp.showdisp import show as DB
from analytics.analytics_engine import analyze_engine
from sessions.session import session_id
from sessions.action import action_log
from sessions.Review_db import rev_warehouse
#from pages.home import home_page

def main():
    go=1
    lid,l_date_time=session_id(go)
    st.title("intmood")
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
        marketplace = ["amazon.in","flipkart.com","swiggy.com","zomato.com","oyorooms.com","rottentomatoes.com","mynrta.com"]
        c1,c2 = st.beta_columns((1,4))
        with c1:
            choice = st.selectbox("Select Marketplace",marketplace,key="marketplace")
        with c2:
            product_url = st.text_input("Enter The Product url [Eg:https://www.amazon.in/dp/B07JWV47JW]")

    if choice == "amazon.in":
        st.subheader("Amazon.in")
        if st.button("Analyze Reviews",key="go"):
            if "amazon.in" in product_url:
                with st.spinner('Crawling Amazon to get reviews'):
                    data,p_name,error=amz(product_url)
                    if error=="stop":
                        st.info("Unable to connect!! Amazon is Not available right now")
                        st.stop()
                    else:
                        st.success('Extrction Complete!')
                        st.title("Lets dig in to the product:")
                        st.info(p_name)
                        action_log(lid,choice,product_url)
                        #(lid,product_url,l_date_time,data)
                        DB(data)
                        analyze_engine(data)
                        rev_warehouse(product_url,l_date_time,data)
                        st.info("that's all for now")
    elif choice == "flipkart.com":
        st.subheader("flipkart.com")
        if st.button("Analyze Reviews",key="go"):
            if "flipkart.com" in product_url:
                with st.spinner('Crawling Flipkart to get reviews'):
                    print("entered0")
                    data,p_name,error=flipkart(product_url)
                    if error=="stop":
                        st.info("Unable to connect!! Flipkart is Not available right now")
                        st.stop()
                    else:
                        st.success('Extrction Complete!')
                        st.title("Lets dig in to the product:")
                        st.info(p_name)
                        action_log(lid,choice,product_url)
                        #(lid,product_url,l_date_time,data)
                        DB(data)
                        analyze_engine(data)
                        rev_warehouse(product_url,l_date_time,data)
                        st.info("that's all for now")








            else:
                st.text("Enter a amazon.in starting product URL")
        else:
            st.write("Press the above button..")


if __name__ == '__main__':
	main()
