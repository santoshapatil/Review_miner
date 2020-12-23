import matplotlib.pyplot as plt

import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import calendar
import datetime
#del after checking
from textblob import TextBlob
import pandas as pd

def get_sentiment(text):
  blob = TextBlob(text)
  result = blob.sentiment.polarity
  return result


def vide_meter(polarity):
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = polarity,
    mode = "gauge+number",
    #title={'text': "<h1>Vibe Meter</h1><p>Red -&gt; Poor Vibe</p><p>White -&gt; Neutral Vibe</p><p>Green -&gt; Good Vibe</p>"},
    title = {'text':"<b>Vibe Score</b><br><span style='color: orange; font-size:5'>RED is not okay, WHITE is Neutral,GREY is Good </span>",'font': {"size": 14}
             },
    gauge = {'axis': {'range': [-1, 1]},
             'steps' : [
                  {'range': [-1,-0.2], 'color': "red",'name':"Not Okay"},
                  {'range': [-0.2,0.2], 'color': "white",'name':"Not Okay"},
                  {'range': [0.2, 1], 'color': "lightgray",'name':"Not Okay"}]
             }))
    fig.update_layout(paper_bgcolor = "beige", font = {'color': "darkblue", 'family': "Arial"})

    return fig
def moji(pol):
  if pol > 0.5 :
    custom_emoji = ':smile:'
    p=emoji.emojize(custom_emoji,use_aliases=True)

  elif pol <0.5 and pol>0:
    custom_emoji = ':unamused:'
    p=emoji.emojize(custom_emoji,use_aliases=True)

  elif pol >-0.5 and pol<0:
    custom_emoji = ':flushed:'
    p=emoji.emojize(custom_emoji,use_aliases=True)

  else:
    custom_emoji = ':disappointed:'
    p=emoji.emojize(custom_emoji,use_aliases=True)
  return p
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






    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)
    by_Val=["By Year","By Quarter"]
    mode=st.radio("Select :",by_Val)
    if mode =="By Year":
        year_sel=yind["year"]
        year=st.radio("Select Year",year_sel)
        for index,row in yind.iterrows():
            if row["year"]==year:
                vibe_m=vide_meter(row["Polarity"])
                st.plotly_chart(vibe_m)

    elif mode == "By Quarter":
        qa_sel=quind["DATE"]
        qs=st.radio("Select Year",qa_sel)
        for index,row in quind.iterrows():
            if row["DATE"]==qs:
                vibe_m=vide_meter(row["Polarity"])
                st.plotly_chart(vibe_m)

    st.subheader("Vibe Score in the Past:")
    st.info("After reading the reviews,we gave a score for each one of them and here is what people have vibed across.")
    fig = go.Figure(px.scatter(quind, x="DATE", y="Polarity",
                 size='No. of Reviews', hover_data=['No. of Reviews',"Polarity"]
            ))
    fig.add_shape(
            type='line',
            x0=0,
            y0=av_pol,
            x1=quind["DATE"].iloc[-1],
            y1=av_pol,
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
    fig.show()
    st.plotly_chart(fig)
    if quind["Polarity"].iloc[-1]<av_pol and quind["Polarity"].iloc[-2]<av_pol:
        st.info("Watch out!! look for an alternative as the people who bought the product in the last quarter felt the product in not upto the mark")
    else:
        st.info("In the last two quarters we see that the Vibe score is greater than what most people felt, so the seller has not compramised on his product expectations.")

#Reviews=pd.read_csv(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\reviews.csv")
#print("read")
#vibe_plot(Reviews)
