
from bs4 import BeautifulSoup
import requests
import streamlit as st

#from flask import Flask, render_template, url_for, request

#nltk.download('stopwords')



from ext.amzengine import Review_extract as amz
from disp.showdisp import show as DB
from analytics.analytics_engine import analyze_engine
def main():
    st.title("Review Miner  ")
    st.text("By Santosh A Patil")
    marketplace = ["amazon.in","flipkart.in","swiggy.com","zomato.com","oyorooms.com","rottentomatoes.com","mynrta.com"]
    choice = st.sidebar.selectbox("Select Marketplace",marketplace)
    if choice == "amazon.in":
        st.subheader("Amazon.in")
        st.text("https://www.amazon.in/Brayden-Portable-Blender-Rechargeable-Transparent/dp/B07NS898HJ/ref=cm_cr_arp_d_product_top?ie=UTF8")
        product_url = st.text_input("Enter The Product url [Eg:https://www.amazon.in/dp/B07JWV47JW]")

        if st.button('Analyze Reviews'):
            if "amazon.in" in product_url:
                data=amz(product_url)
                DB(data)
                analyze_engine(data)


            else:
                st.text("Enter a amazon.in starting product URL")
        else:
            st.write("Press the above button..")
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
        "[issues](https://github.com/MarcSkovMadsen/awesome-streamlit/issues) of or"
        "[pull requests](https://github.com/MarcSkovMadsen/awesome-streamlit/pulls) "
        "to the [source code](https://github.com/MarcSkovMadsen/awesome-streamlit). "
        """
    )
    st.sidebar.title("Key Idea")
    st.sidebar.info(
        """
        Know what people felt about what you are about to buy

        """
    )

if __name__ == '__main__':
	main()
