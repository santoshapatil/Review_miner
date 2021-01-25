import plotly.graph_objs as go
import plotly.express as px

def plot_emo(row["Happy","Angry","Surprise","Sad","Fear"]):
    pie_fig = px.pie(r_df,names="Rate",values='rate_count',
               hover_data=['rate_count'], labels={'rate_count':'No. of Reviews'})
                             
    pie_fig.update_traces(textposition='inside', textinfo='label+percent',insidetextorientation='radial')
    pie_fig.update_layout(paper_bgcolor = "#F2F2F0", font = {'color': "darkblue", 'family': "Arial"})