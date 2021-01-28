import plotly.graph_objs as go
import plotly.express as px

def plot_emo(v):
    d=["Happy","Angry","Surprise","Sad","Fear"]
    pie_fig= go.Figure(data=[go.Pie(labels=d, values=v)])
                             
    pie_fig.update_traces(textposition='inside', textinfo='label+percent',insidetextorientation='radial')
    pie_fig.update_layout(paper_bgcolor = "#F2F2F0", font = {'color': "darkblue", 'family': "Arial"})
    pie_fig.update_layout(title = "<b>Critical Emotions or feelings during this period</b>")
    # pie_fig.show()
    return pie_fig