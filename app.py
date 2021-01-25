
from bs4 import BeautifulSoup
import requests
import streamlit as st
import os, base64
from PIL import Image
import numpy as np
from datetime import date
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
#from flask import Flask, render_template, url_for, request

#nltk.download('stopwords')

import os
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import collections


from pages.how_to import About
from ext.mkt_bridge import build_bridge
from disp.showdisp import show as DB
from analytics.analytics_engine import analyze_engine
from analytics.vibe_meter import vibe_plot
from analytics.word_sentiment import word_senti
from sessions.session import session_id
from sessions.action import action_log
from sessions.Review_db import rev_warehouse
from time_log.time_pull import start_time
from time_log.time_pull import log_time
from PIL import Image
from streamlit.report_thread import get_report_ctx
import time
import streamlit.components.v1 as components
from skimage import io

from plots.mood_plot import mood_meter
from plots.emotion_plot import plot_emo
#feedback form url
#fedback form iframe <iframe src="https://docs.google.com/forms/d/e/1FAIpQLSfEkP5xHG9hIEM1iXXmdHnHSaFkqbuhuXeT8EDP4BsI33joaA/viewform?embedded=true" width="640" height="1051" frameborder="0" marginheight="0" marginwidth="0">Loading…</iframe>
# width 640px,height 1051px
#  https://forms.gle/FhasqkRhHiAG5Put5
def start_time():
    start=time.time()
    return start 

def log_time(start):
    diff=time.time()-start
    return diff
#from pages.home import home_page
 

def temp_log(lid,l_date_time,mkt,product_url,ext_time,Reviews,entered_words,u_email,u_feedback):
    # temp_db=pd.DataFrame(index=None)
    temp_db=pd.read_csv(r"temp_db.csv",index_col=False)
    Reviews["session_id"]=lid
    Reviews["l_date_time"]=l_date_time
    Reviews["mkt"]=mkt
    Reviews["Product_url"]=product_url
    Reviews["ext_time"]=ext_time
    entered_words = ','.join(map(str, entered_words))
    Reviews["entered_words"]=entered_words
    if entered_words is None:
        entered_words="no_there"
        Reviews["entered_words"]=entered_words
    else:
        entered_words = ','.join(map(str, entered_words))
        Reviews["entered_words"]=entered_words
    Reviews["u_email"]=u_email
    Reviews["u_feedback"]=u_feedback


    
    #new_db={"product_url":[product_url],"log_id":[log_id],"l_date_time":[l_date_time]}
    

    temp_db=temp_db.append(Reviews,ignore_index=True)
    temp_db.to_csv("temp_db.csv",index=False)   
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded
@st.cache(persist=True, allow_output_mutation=True)
def data_bridge(mkt,product_url):
       t=start_time()
       data,p_name,pimg,error=build_bridge(mkt,product_url)
       diff=log_time(t)
       return data,p_name,pimg,error,diff

def dashboard(lid,mkt,product_url):
     data,p_name,pimg,error,diff=data_bridge(mkt,product_url)
    #  data= pd.read_csv(r"rev_warehouse.csv",index_col=False)
    #  data=data[data["session_id"]==lid]
     img = io.imread(pimg)
     p_img = px.imshow(img)
     p_img.update_xaxes(showticklabels=False) # hide all the xticks
     p_img.update_yaxes(showticklabels=False)
    #  p_img.update_layout(plot_bgcolor="#F2F2F0",paper_bgcolor = "#cd ", font = {'color': "#F1828D", 'family': "Arial"})
    #  https://www.amazon.in/Lenovo-81NG002BIN-15-6-inch-I5-10210U-Microsoft/dp/B083PFG5HH/ref=cm_cr_arp_d_product_top?ie=UTF8
     st.subheader("Product Image")
     with st.beta_container():
          st.plotly_chart(p_img,use_container_width=True)
     cnt_rev, sd,ld, avg_rating, pie_fig,hist_fig,fig=DB(data)
     st.write("We Extracted a total of ",cnt_rev)
     st.write("Extracted Reviews from "+sd+" to "+ld)
     st.write("Average Rating for the product ",round(avg_rating, 2))

    
     st.subheader("Review ratings given by people who have written reviews about this product.")
     c1,c2 = st.beta_columns(2)
     c1.plotly_chart(pie_fig,use_container_width=True)
     c2.plotly_chart(hist_fig,use_container_width=True)
     st.subheader("Average review rating for every four months[Quarterly].")
     with st.beta_expander('Click to minimize-->',expanded=True):
        with st.beta_container():
            st.plotly_chart(fig,use_container_width=True)
     
     st.subheader("Most Common Words")
     
     rev_data=analyze_engine(data)
     
     all_words=rev_data["words"].tolist()

     new_list = []
     for words in all_words:
        new_list += words
     
     def word_table(i,new_list):
         counts_words = collections.Counter(new_list)
         words_df = pd.DataFrame(counts_words.most_common(i),columns=['words', 'count'])
         return words_df

     
     

    
    #  word_list(counts_words)
   #temp_data(Reviews)
     #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
     
     
     Val=["5","10","15"]
     num=st.radio(label="No. of Frequent Words",options=Val,key=1)
     if num=="5":
               st.table(word_table(5,new_list))
     elif num=="10":
            #    words_df = pd.DataFrame(counts_words.most_common(10),columns=['words', 'count'])
               st.table(word_table(10,new_list))
     elif num=="15":
            #    words_df = pd.DataFrame(counts_words.most_common(15),columns=['words', 'count'])
               st.table(word_table(15,new_list))
   
     st.subheader("Mood Meter")    
     st.info("We read the reviews for you and learnt what people vibed in it.")

     yind,quind,eyind,equind=vibe_plot(rev_data)

     st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
     by_Val=["By Year","By Quarter"]
     mode=st.radio("Select :",by_Val)
     st.subheader("")
     with st.beta_container():
      
      if mode =="By Year":
        year_sel=yind["year"]
        year=st.radio("Select Year",year_sel)
        for i1,r1,i2,r2 in zip(yind.iterrows(),eyind.iterrows()):
            if row["year"]==year:
                vibe_m=mood_meter(row["Polarity"])
                emo_fig=plot_emo(row["Happy","Angry","Surprise","Sad","Fear"])
                e1,e2=st.beta_columns(2)
                e1.plotly_chart(vibe_m,use_container_width=True)
                e2.plotly_chart(emo_fig,use_container_width=True)

      elif mode == "By Quarter":
        qa_sel=quind["DATE"]
        qs=st.radio("Select Quarter",qa_sel)
        for i1,r1,i2,r2 in zip(yind.iterrows(),equind.iterrows()):
            if row["DATE"]==qs:
                vibe_m=mood_meter(row["Polarity"])
                emo_fig=plot_emo(row["Happy","Angry","Surprise","Sad","Fear"])
                e1,e2=st.beta_columns(2)
                e1.plotly_chart(vibe_m,use_container_width=True)
                e2.plotly_chart(emo_fig,use_container_width=True)
     
     
     fig = go.Figure(px.scatter(quind, x="DATE", y="Polarity",
                 size='No. of Reviews', hover_data=['No. of Reviews',"Polarity"]
            ))
     fig.add_shape( # add a horizontal "target" line
                 type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                  x0=0, x1=1, xref="paper", y0=av_pol, y1=av_pol, yref="y"
                   )
     fig.add_annotation(
            x=quind["DATE"].iloc[-1],
            y=av_pol,
            xref="x",
            yref="y",
            text="What most people felt",
            showarrow=True,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
                ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="red",
            ax=20,
            ay=-30,
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
            )

     fig.update_xaxes(showgrid=False,showline=True, linewidth=2, linecolor='black')
     fig.update_yaxes(showgrid=False,showline=True, linewidth=2, linecolor='black')

     fig.update_layout(plot_bgcolor="#F2F2F0",paper_bgcolor = "#F2F2F0", font = {'color': "#F1828D", 'family': "Arial"})
    #fig.update_layout(plot_bgcolor=<VALUE>)
     st.subheader("Vibe Score in the Past:")
     st.info("After reading the reviews,we gave a score for each one of them and here is what people have vibed across all those reviews.")
     with st.beta_container():
      st.plotly_chart(fig,use_container_width=True)

      
    
    
     if quind["Polarity"].iloc[-1]<av_pol and quind["Polarity"].iloc[-2]<av_pol:
        st.info("Watch out!! look for an alternative as the people who bought the product in the last quarter felt the product is not upto the mark")
     else:
        st.info("In the last two quarters we see that the Vibe score is greater than what most people felt, so the seller has not compramised on his product expectations.")

     st.subheader("Vibe Score of a word")
     word_sent = st.text_input("Enter a word and we'll get the sentiment about that word in the reviews.",value="quality")
     word_sent=word_sent.lower()
     print(word_sent)
    #  rev_data=d_bank(rev_data)
   
   #if rev_data["text"].str.contains(word_sent, regex=True) is True:
   #print("word inside")
   #print(rev_data["text"])
     
     rev_data['text']=rev_data['text'].str.lower()
     entered_words=[]
     d=rev_data[rev_data['text'].str.contains(word_sent)]
     print(d)
     if d.empty:
         st.write("Word not present") 
     else:
         entered_words.append(word_sent)
         word_senti(word_sent,d)
     return entered_words

def main():
    
    


    
    ctx = get_report_ctx()
    print(ctx.session_id)
    st.set_page_config(
    page_title="intmood",
    page_icon="🧊",
    layout="wide")
    # initial_sidebar_state="expanded")
    
    go=1
    lid,l_date_time=session_id(go)
    
    #st.text("By Santosh A Patil")
    pages = ["Home","About"]
    page = st.sidebar.radio("Select Page",pages,key="page")

    st.sidebar.title("Key Idea")
    st.sidebar.info(
    """
        Know what people felt about what you are about to buy

    """
    )
    st.sidebar.title("About")
    st.sidebar.info(
        """
        This is a Web ML App to help you make a data driven decision before you
        click purchase button while shopping online.
        We sincerely thank Amazon,Flipkart and other digital market places
        to let this app get reviews from their website."

        """
        )
    
    
    
    
    
 
    #st.sidebar.title("Connect with us on")
    #inst = Image.open("./img/instagram.svg")
    #tweet=Image.open("./img/twitter.svg")
    #linkedin=Image.open("./img/linkedin.svg")
    #youtube=Image.open("./img/youtube.svg")
    

    st.sidebar.subheader("Follow us on:")
    with st.sidebar.beta_container():
                c1,c2,c3,c4= st.beta_columns(4)
                with c1:
                    #insta=f"<a href='https://github.com/MarcSkovMadsen/awesome-streamlit'><img src='data:./img/instagram.svg;base64,{image_base64}'></a>"
                    insta=f"[![instagram](https://cdn.exclaimer.com/Handbook%20Images/instagram-icon_32x32.png)](https://instagram.com/intmood_)"
                    st.markdown(insta,unsafe_allow_html=False)
                with c2:
                    twit=f"[![twitter](https://cdn.exclaimer.com/Handbook%20Images/twitter-icon_32x32.png)](https://twitter.com/intmood)"
                    st.markdown(twit,unsafe_allow_html=False)
                with c3:
                    linkedin=f"[![linkedin](https://cdn.exclaimer.com/Handbook%20Images/linkedin-icon_32x32.png)](https://www.linkedin.com/company/intmood)"
                    st.markdown(linkedin,unsafe_allow_html=False)
                with c4:
                    youtube=f"[![youtube](https://cdn.exclaimer.com/Handbook%20Images/youtube-icon_32x32.png)](https://www.youtube.com/channel/UCZ84Qr78IKdMKtYLymu1TFw)"
                    st.markdown(youtube,unsafe_allow_html=False)
    st.sidebar.subheader("Feedback/Report broken link")
    with st.sidebar.beta_container():
            feedback=f"[![feedback](https://raw.githubusercontent.com/loadcontent/imagebox/main/3933037771600677167-48.png)](https://docs.google.com/forms/d/e/1FAIpQLSfEkP5xHG9hIEM1iXXmdHnHSaFkqbuhuXeT8EDP4BsI33joaA/viewform?usp=sf_link)"
            st.markdown(feedback,unsafe_allow_html=False)       
    u_email=st.sidebar.text_input("Email ID",value="")
    u_feedback=st.sidebar.text_input("Enter Feedback here",value="")    
    
    


    
    


    
    if page == "Home":
        
        
     st.title("intmood")
        #st.text("https://www.amazon.in/Brayden-Portable-Blender-Rechargeable-Transparent/dp/B07NS898HJ/ref=cm_cr_arp_d_product_top?ie=UTF8")
     marketplace = ["amazon.in","flipkart.com","swiggy.com","zomato.com","oyorooms.com","rottentomatoes.com","mynrta.com"]
     c1,c2 = st.beta_columns((1,4))
     with c1:

            mkt = st.selectbox(label="Select Marketplace",options= marketplace,key="marketplace")
     with c2:
            product_url = st.text_input("Enter The Product url [Eg:https://www.amazon.in/dp/B07JWV47JW]")    
    
     if mkt == "amazon.in":
        st.subheader("Amazon.in")
        # if st.button("Analyze Reviews",key=2):
        if "amazon.in" in product_url:
                with st.spinner('Crawling Amazon to get reviews'):
                    data,p_name,pimg,error,ext_time=data_bridge(mkt,product_url)
                    # data=reservoir(data)
                    if error=="stop":
                        st.info("Unable to connect!! Amazon is Not available right now")
                        st.stop()
                    else:
                        st.success('Extrction Complete!')
                        st.title("Lets dig in to the product:")
                        st.info(p_name)
                        rev_warehouse(lid,product_url,l_date_time,data)
                        action_log(lid,mkt,product_url,ext_time)
                        #(lid,product_url,l_date_time,data)
                        entered_words=dashboard(lid,mkt,product_url)
                        temp_log(lid,l_date_time,mkt,product_url,ext_time,data,entered_words,u_email,u_feedback)
                        #rev_warehouse(product_url,l_date_time,data)
                        
                        st.info("that's all for now")
        else:
                st.text("Enter a amazon.in starting product URL")
     elif mkt == "flipkart.com":
        st.subheader("flipkart.com")
        if st.button("Analyze Reviews",key=3):
            if "flipkart.com" in product_url:
                with st.spinner('Crawling Flipkart to get reviews'):
                    
                    data,p_name,error=build_bridge(mkt,product_url)
                    # data=reservoir(data)
                    if error=="stop":
                        st.info("Unable to connect!! Flipkart is Not available right now")
                        st.stop()
                    else:
                        st.success('Extrction Complete!')
                        st.title("Lets dig in to the product:")
                        st.info(p_name)
                        action_log(lid,mkt,product_url)
                        #(lid,product_url,l_date_time,data)
                        rev_warehouse(product_url,l_date_time,data)
                        st.info("that's all for now")
            else:
                st.text("Enter a flipkart.com starting product URL")








        else:
            st.write("Press the above button..")
    elif page == "About":
        About()

    return None

if __name__ == '__main__':
       main()
