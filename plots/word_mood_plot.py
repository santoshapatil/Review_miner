import plotly.graph_objs as go

def word_mood_meter(word,polarity):
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = polarity,
    mode = "gauge+number",
    #title={'text': "<h1>Vibe Meter</h1><p>Red -&gt; Poor Vibe</p><p>White -&gt; Neutral Vibe</p><p>Green -&gt; Good Vibe</p>"},
    title = {'text':"<b>General Mood surrounding the word:</b><br><span style='color: orange; font-size:10'>RED is not okay, WHITE is Neutral,GREY is Good </span>",'font': {"size": 14}
             },
    gauge = {'axis': {'range': [-1, 1]},
             'steps' : [
                  {'range': [-1,-0.2], 'color': "red",'name':"Not Okay"},
                  {'range': [-0.2,0.2], 'color': "white",'name':"Not Okay"},
                  {'range': [0.2, 1], 'color': "lightgray",'name':"Not Okay"}]
             }))
    if polarity >0.2:
        fig.add_layout_image(dict(
        source="https://raw.githubusercontent.com/loadcontent/imagebox/main/sml_pos.png",
        x=1,
        y=0.8,
        ))
    elif polarity <=0.2 and polarity >=-0.2 :
        fig.add_layout_image(dict(
        source="https://raw.githubusercontent.com/loadcontent/imagebox/main/sml_neu.png",
        x=1,
        y=0.8,
        ))
    else :
       fig.add_layout_image(
        dict(
        source="https://raw.githubusercontent.com/loadcontent/imagebox/main/sml_neg.png",
        x=1,
        y=0.8,
          ))
    fig.update_layout_images(dict(
        xref="paper",
        yref="paper",
        sizex=0.2,
        sizey=0.2,
        xanchor="right",
        yanchor="bottom"
     ))
    
    fig.update_layout(paper_bgcolor = "#F2F2F0", font = {'color': "darkblue", 'family': "Arial"})
    return fig