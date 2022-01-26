import pandas as pd
import plotly.express as px


aus_maxT = pd.read_csv('AustralianAverageMaxTemp.csv')
print(aus_maxT.head())
print(aus_maxT['Year'].unique())

# mapbox token from https://www.kaggle.com/shtrausslearning/geospatial-data-visualisation-australia/data
px.set_mapbox_access_token('pk.eyJ1Ijoic2h0cmF1c3NhcnQiLCJhIjoiY2t0eXhzdGFpMWlscTJ1cDg3ZGhocmptayJ9.7TepS9eN6iKXwYjPHu44Tg')

fig = px.scatter_mapbox(aus_maxT, lat='lat', lon='long', color='Temp', mapbox_style='light',
                        opacity=1.0, range_color=[15,28], size='Temp', size_max=10,
                        animation_frame='Year', zoom=2.8, center=dict(lat=-27, lon=140), height=650)

fig.update_layout(margin=dict(l=30, r=30, b=30))
fig.update_layout(template='plotly_white', title='<b>ALL STATION MAX TEMPERATURE</b>' + 
                  ' | TIME SERIES VARIATION', showlegend=True)
fig.update_layout(font=dict(family='sans-serif', size=12))
fig.show()