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
#from analytics.analytics_engine import analyze_engine
#https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/09_timeseries.html?highlight=datetime
def show(d):
    d['Review_date']= pd.to_datetime(d['Review_date'])

    cnt_rev=len(d)
    st.write("We Extracted a total of ",cnt_rev)
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


    
    #color_mapper = CategoricalColorMapper(palette=Spectral6, factors=regions_list)



    st.subheader("Rating over Time")
    st.info("Use the below graphs to know weather the rating of the product has been consistent with time. The average of the ratings is calculated based on month or year for the product selected.")

    date_data=d[["Review_date","Review_rating"]]
    grp_month=date_data.groupby(pd.Grouper(key='Review_date',freq='M')).mean()
    grp_year=d.groupby(d['Review_date'].dt.year)["Review_rating"].mean()
    #date_data=date_data.groupby(pd.Grouper(key='Review_date',freq='M')).mean()
    with st.beta_expander('Click to minimize-->',expanded=True):
        with st.beta_container():
            gtype=["Month","Year"]
            group_typ = st.selectbox("Group Date by",gtype,key="gtype")

            if group_typ=="Month":
                st.line_chart(grp_month)
            else:
                st.line_chart(grp_year)

    #d.plt(Review_date,Review_rating)
    #plt.show()
    #st.pyplot(plt)



#Reviews=pd.read_csv(r"C:\Users\SANTOSH A PATIL\Documents\GitHub\Review_miner\reviews.csv")
#show(Reviews)
