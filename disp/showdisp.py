#display Result
import pandas as pd
import streamlit as st
import numpy as np
from datetime import date

import bokeh
from bokeh.plotting import figure, output_file, show

from PIL import Image
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource,
                          HoverTool, Label, SingleIntervalTicker, Slider,)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
import plotly.graph_objects as go
import plotly.express as px
#from analytics.analytics_engine import analyze_engine
#https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/09_timeseries.html?highlight=datetime
def show(rev_data):
    rev_data['Review_date']= pd.to_datetime(rev_data['Review_date'])

    cnt_rev=len(rev_data)
    st.write("We Extracted a total of ",cnt_rev)
    startd=rev_data['Review_date'].iloc[0]
    lastd=rev_data['Review_date'].iloc[-1]
    sd=date(day=startd.day, month=startd.month, year=startd.year).strftime('%d %B %Y')
    ld=date(day=lastd.day, month=lastd.month, year=lastd.year).strftime('%d %B %Y')
    st.write("Extracted Reviews from "+sd+" to "+ld)
    avg_rating=rev_data["Review_rating"].mean()
    st.write("Average Rating for the product ",round(avg_rating, 2))

    r_df = rev_data['Review_rating'].value_counts().reset_index()
    r_df.columns = ['Rate', 'rate_count']

    cmap = plt.get_cmap('Spectral')
    colors = [cmap(i) for i in np.linspace(0, 1, 8)]

    r_df['emo_r']=["1 star","2 star","3 star","4 star","5 star"]
    c1,c2 = st.beta_columns(2)

    with c1:
         plt.subplot(aspect=1, title='Review rating')
         type_show_ids = plt.pie(r_df.rate_count, labels=r_df.emo_r, autopct='%1.1f%%', colors=colors)
         plt.show()
         st.pyplot(plt)
    with c2:

        plt.subplot(title='Review rating')
        plt.bar(r_df.emo_r,r_df.rate_count)
        plt.show()
        st.pyplot(plt)



    #color_mapper = CategoricalColorMapper(palette=Spectral6, factors=regions_list)



    st.subheader("Rating over Time")
    st.info("Use the below graphs to know weather the rating of the product has been consistent with time. The average of the ratings is calculated based on month or year for the product selected.")


    rev_data["year"]=rev_data['Review_date'].dt.year
    rev_data["quarter"]=rev_data['Review_date'].dt.quarter
    rev_data["month"]=rev_data['Review_date'].dt.month

    yind=rev_data.pivot_table(index="year",values="Review_rating",aggfunc='mean')
    mind=rev_data.pivot_table(index=["year","month"],values="Review_rating",aggfunc='mean')
    quind=rev_data.pivot_table(index=["year","quarter"],values="Review_rating",aggfunc='mean')
    yind["No. of Ratings"]=rev_data.groupby("year",sort=False)["Review_rating"].count()
    mind["No. of Ratings"]=rev_data.groupby([rev_data["year"],rev_data["month"]],sort=False)["Review_rating"].count()
    quind["No. of Ratings"]=rev_data.groupby([rev_data["year"],rev_data["quarter"]],sort=False)["Review_rating"].count()
    yind=yind.reset_index()
    quind=quind.reset_index()
    mind=mind.reset_index()
    quind['DATE'] =quind['year'].astype(str) + ' Q' + quind['quarter'].astype(str)
    mind["DATE"]=pd.to_datetime(mind[['year', 'month']].assign(DAY=1))
    av_rate=rev_data["Review_rating"].mean()
    fig = go.Figure(px.scatter(quind, x="DATE", y="Review_rating",
                 size='No. of Ratings', hover_data=['No. of Ratings',"Review_rating"]
            ))
    fig.add_shape(
            type='line',
            x0=0,
            y0=av_rate,
            x1=quind["DATE"].iloc[-1],
            y1=av_rate,
            )

    fig.add_annotation(
            x=quind["DATE"].iloc[-1],
            y=av_rate,
            xref="x",
            yref="y",
            text="What most people rated this product",
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

    #date_data=date_data.groupby(pd.Grouper(key='Review_date',freq='M')).mean()
    with st.beta_expander('Click to minimize-->',expanded=True):
        with st.beta_container():
            st.plotly_chart(fig)

    #d.plt(Review_date,Review_rating)
    #plt.show()
    #st.pyplot(plt)



#Reviews=pd.read_csv(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\reviews_fkart.csv")
#show(Reviews)
