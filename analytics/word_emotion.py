import pandas as pd


def word_emo(d):
    # h=d.Happy.sum()
    # a=d.Angry.sum()
    # s=d.Surprise.sum()
    # sad=d.Sad.sum()
    # f=d.Fear.sum()
    v=[d['Happy'].sum(),d['Angry'].sum(),d['Surprise'].sum(),d['Sad'].sum(),d['Fear'].sum()]
    v=[round(i) for i in v]
    v=[int(i) for i in v]
    return v
