import plotly.graph_objs as go
import plotly.express as px

def word_feelings(word,v):
    d=["Happy","Angry","Surprise","Sad","Fear"]
    pie_fig= go.Figure(data=[go.Pie(labels=d, values=v)])
                             
    pie_fig.update_traces(textposition='inside', textinfo='label+percent',insidetextorientation='radial')
    pie_fig.update_layout(paper_bgcolor = "#F2F2F0", font = {'color': "darkblue", 'family': "Arial"})
    pie_fig.update_layout(title="<b>Feelings surrounding the word:</b>")
    # pie_fig.add_annotation(
    #         x=1.2,
    #         y=1.25,
    #         text=word,
    #         showarrow=False,
    #         font=dict(
    #             family="Courier New, monospace",
    #             size=16,
    #             color="#ffffff"
    #             ),
    #         align="center",
    #         bordercolor="#c7c7c7",
    #         bgcolor="#ff7f0e",
    #         opacity=0.8
    #         )
    # pie_fig.show()
    return pie_fig