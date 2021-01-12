def vide_meter(polarity):
    fig = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = polarity,
    mode = "gauge+number",
    #title={'text': "<h1>Vibe Meter</h1><p>Red -&gt; Poor Vibe</p><p>White -&gt; Neutral Vibe</p><p>Green -&gt; Good Vibe</p>"},
    title = {'text':"<b>Vibe Score</b><br><span style='color: orange; font-size:10'>RED is not okay, WHITE is Neutral,GREY is Good </span>",'font': {"size": 14}
             },
    gauge = {'axis': {'range': [-1, 1]},
             'steps' : [
                  {'range': [-1,-0.2], 'color': "red",'name':"Not Okay"},
                  {'range': [-0.2,0.2], 'color': "white",'name':"Not Okay"},
                  {'range': [0.2, 1], 'color': "lightgray",'name':"Not Okay"}]
             }))
    fig.update_layout(paper_bgcolor = "#F2F2F0", font = {'color': "darkblue", 'family': "Arial"})
    
    
    return fig