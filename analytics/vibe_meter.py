import matplotlib.pyplot as plt

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import calendar
import datetime
import numpy as np
#del after checking
from textblob import TextBlob

from plots.mood_plot import mood_meter
from plots.emotion_plot import plot_emo
def get_sentiment(text):
  blob = TextBlob(text)
  result = blob.sentiment.polarity
  return result

# @st.cache
# def load_df(yind,mind,quind):
#   return yind,mind,quind

# delete this feature
# def moji(pol):
#   if pol > 0.5 :
#     custom_emoji = ':smile:'
#     p=emoji.emojize(custom_emoji,use_aliases=True)

#   elif pol <0.5 and pol>0:
#     custom_emoji = ':unamused:'
#     p=emoji.emojize(custom_emoji,use_aliases=True)

#   elif pol >-0.5 and pol<0:
#     custom_emoji = ':flushed:'
#     p=emoji.emojize(custom_emoji,use_aliases=True)

#   else:
#     custom_emoji = ':disappointed:'
#     p=emoji.emojize(custom_emoji,use_aliases=True)
#   return p
def vibe_plot(rev_data):

    rev_data['Review_date']= pd.to_datetime(rev_data['Review_date'])
    rev_data["year"]=rev_data['Review_date'].dt.year
    rev_data["quarter"]=rev_data['Review_date'].dt.quarter
    rev_data["month"]=rev_data['Review_date'].dt.month

    # del this line
    #rev_data["text"] = rev_data[['Review_title','Review_body']].apply(lambda x: ' '.join(x), axis=1)
    #rev_data["Polarity"]=rev_data["text"].apply(get_sentiment)


    yind=rev_data.pivot_table(index="year",values="Polarity",aggfunc='mean')
    mind=rev_data.pivot_table(index=["year","month"],values="Polarity",aggfunc='mean')
    quind=rev_data.pivot_table(index=["year","quarter"],values="Polarity",aggfunc='mean')
    yind["No. of Reviews"]=rev_data.groupby("year",sort=False)["text"].count()
    mind["No. of Reviews"]=rev_data.groupby([rev_data["year"],rev_data["month"]],sort=False)["text"].count()
    quind["No. of Reviews"]=rev_data.groupby([rev_data["year"],rev_data["quarter"]],sort=False)["text"].count()
    yind=yind.reset_index()
    quind=quind.reset_index()
    mind=mind.reset_index()
    quind['DATE'] =quind['year'].astype(str) + ' Q' + quind['quarter'].astype(str)
    mind["DATE"]=pd.to_datetime(mind[['year', 'month']].assign(DAY=1))
    av_pol=mind["Polarity"].mean()

    
    
    eyind=rev_data.pivot_table(index="year",values=["Happy","Angry","Surprise","Sad","Fear"],aggfunc=np.sum)
    # emind=rev_data.pivot_table(index=["year","month"],values=["Happy","Angry","Surprise","Sad","Fear"],aggfunc=np.sum)
    equind=rev_data.pivot_table(index=["year","quarter"],values=["Happy","Angry","Surprise","Sad","Fear"],aggfunc=np.sum)
    eyind=eyind.round(decimals=0)  #counting the number of values for time being which is a Probablity sum hence rounding ot off needs development
    equind=equind.round(decimals=0)

    eyind=eyind.reset_index()
    equind=equind.reset_index()
    equind['DATE'] =equind['year'].astype(str) + ' Q' + equind['quarter'].astype(str)
    # emind=emind.reset_index()


    return yind,quind,eyind,equind,av_pol
    




    # yind,mind,quind=load_df(yind,mind,quind)
    
    # st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    # by_Val=["By Year","By Quarter"]
    # mode=st.radio("Select :",by_Val)
    # st.subheader("")
    # with st.beta_container():
      
    #   if mode =="By Year":
    #     year_sel=yind["year"]
    #     year=st.radio("Select Year",year_sel)
    #     for index,row in yind.iterrows():
    #         if row["year"]==year:
    #             vibe_m=mood_meter(row["Polarity"])
    #             st.plotly_chart(vibe_m,use_container_width=True)

    #   elif mode == "By Quarter":
    #     qa_sel=quind["DATE"]
    #     qs=st.radio("Select Quarter",qa_sel)
    #     for index,row in quind.iterrows():
    #         if row["DATE"]==qs:
    #             vibe_m=mood_meter(row["Polarity"])
    #             st.plotly_chart(vibe_m,use_container_width=True)
      
      
    # fig = go.Figure(px.scatter(quind, x="DATE", y="Polarity",
    #              size='No. of Reviews', hover_data=['No. of Reviews',"Polarity"]
    #         ))
    # fig.add_shape(
    #         type='line',
    #         x0=0,
    #         y0=av_pol,
    #         x1=quind["DATE"].iloc[-1],
    #         y1=av_pol,
    #         )
    # fig.add_shape( # add a horizontal "target" line
    #              type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
    #               x0=0, x1=1, xref="paper", y0=av_pol, y1=av_pol, yref="y"
    #                )
    # fig.add_annotation(
    #         x=quind["DATE"].iloc[-1],
    #         y=av_pol,
    #         xref="x",
    #         yref="y",
    #         text="What most people felt",
    #         showarrow=True,
    #         font=dict(
    #             family="Courier New, monospace",
    #             size=16,
    #             color="#ffffff"
    #             ),
    #         align="center",
    #         arrowhead=2,
    #         arrowsize=1,
    #         arrowwidth=2,
    #         arrowcolor="red",
    #         ax=20,
    #         ay=-30,
    #         bordercolor="#c7c7c7",
    #         borderwidth=2,
    #         borderpad=4,
    #         bgcolor="#ff7f0e",
    #         opacity=0.8
    #         )

    # fig.update_xaxes(showgrid=False,showline=True, linewidth=2, linecolor='black')
    # fig.update_yaxes(showgrid=False,showline=True, linewidth=2, linecolor='black')

    # fig.update_layout(plot_bgcolor="#F2F2F0",paper_bgcolor = "#F2F2F0", font = {'color': "#F1828D", 'family': "Arial"})
    # #fig.update_layout(plot_bgcolor=<VALUE>)
    # st.subheader("Vibe Score in the Past:")
    # st.info("After reading the reviews,we gave a score for each one of them and here is what people have vibed across.")

    # for future developments use main app dashboard
    # with st.beta_container():
    #   st.plotly_chart(fig,use_container_width=True)

      
    
    
    # if quind["Polarity"].iloc[-1]<av_pol and quind["Polarity"].iloc[-2]<av_pol:
    #     st.info("Watch out!! look for an alternative as the people who bought the product in the last quarter felt the product is not upto the mark")
    # else:
    #     st.info("In the last two quarters we see that the Vibe score is greater than what most people felt, so the seller has not compramised on his product expectations.")
    

    


#Reviews=pd.read_csv(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\reviews.csv")
#print("read")
#vibe_plot(Reviews)
