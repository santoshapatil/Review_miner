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
#from analytics.analytics_engine import analyze_engine
#https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/09_timeseries.html?highlight=datetime
def show(d):
    d['Review_date']= pd.to_datetime(d['Review_date'])

    cnt_rev=len(d)
    st.write("Extracted a total of ",cnt_rev)
    startd=d['Review_date'].iloc[0]
    lastd=d['Review_date'].iloc[-1]
    sd=date(day=startd.day, month=startd.month, year=startd.year).strftime('%d %B %Y')
    ld=date(day=lastd.day, month=lastd.month, year=lastd.year).strftime('%d %B %Y')
    st.write("Extracted Reviews from "+sd+" to "+ld)
    avg_rating=d["Review_rating"].mean()
    st.write("Average Rating for the product ",round(avg_rating, 2))

    r_df = d['Review_rating'].value_counts().reset_index()
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


    graph = figure(x_axis_type = "datetime", title = "Rating Over Time")
    graph.xaxis.axis_label = 'Date'
    graph.yaxis.axis_label = 'Rating'
    color = "lightblue"
    legend_label = 'Rating-line'
    graph.line(d['Review_date'],
        d["Review_rating"],
        color = color,
        legend_label = legend_label)

    st.bokeh_chart(graph)





    #d.plt(Review_date,Review_rating)
    #plt.show()
    #st.pyplot(plt)
    return


#f=pd.read_csv(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\reviews.csv")
#show(df)
