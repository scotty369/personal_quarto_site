# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
# | output: false
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import datetime
import plotly.express as px

# Load my Data
prob_data = pd.read_csv('https://raw.githubusercontent.com/acbass49/Election2024/main/data/state_probabilities.csv')
tracking_data = pd.read_csv("https://raw.githubusercontent.com/acbass49/Election2024/main/data/tracking_data.csv")
simulation_data = pd.read_csv("https://raw.githubusercontent.com/acbass49/Election2024/main/data/simulation_data.csv")

# Figure 1
fig = go.Figure(data=go.Choropleth(
    locations=prob_data['State'], # Spatial coordinates
    z = prob_data['Trump Win Prob.'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'rdylbu_r',
    marker_line_color='white',
    hovertemplate = "State: %{location}<br>Trump Win Probability: %{z}%<extra></extra>",
    showscale=False
))
config = {'displayModeBar': False, 'scrollZoom': False}
fig.update_layout(
    title_text = 'hover chart for more info',
    geo_scope='usa', # limite map scope to USA
    title_x=0.5
);

# Figure 2
win_perc = sum(simulation_data['points']>=270)/simulation_data.shape[0]

simulation_data = simulation_data.rename(columns={'winner':'Winner'})

fig2 = px.histogram(simulation_data, x="points", color="Winner",
color_discrete_map={"Trump":"#ec543c", "Biden":"#636bfa"})
fig2.update_layout(
    showlegend=True,
    plot_bgcolor='white',
    xaxis_title="EC Votes Trump Wins",
    yaxis_title="Simulation Wins",
#     legend=dict(
#         yanchor="top",
#         y=0.99,
#         xanchor="left",
#         x=0.01
# )
)

#Figure 3

from datetime import timedelta

tracking_data = tracking_data \
    .rename(columns = {'Win Percentage':'Win_Percentage'}) \
    .assign(
        Date = lambda x:pd.to_datetime(x.Date,format='%Y-%m-%d'),
        Win_Percentage = lambda x:round(x.Win_Percentage*100,1),
        LB = lambda x:round(x.LB*100,1),
        UB = lambda x:round(x.UB*100,1),
    )

fig3 = go.Figure()

fig3.add_trace(
    go.Scatter(
        x = tracking_data.query('Candidate == "Biden"')['Date'],
        y = tracking_data.query('Candidate == "Biden"')['Win_Percentage'],
        name = 'Biden',
        line_shape='spline'
    )
)

fig3.add_trace(
    go.Scatter(
        x = tracking_data.query('Candidate == "Trump"')['Date'],
        y = tracking_data.query('Candidate == "Trump"')['Win_Percentage'],
        name = 'Trump',
        line_shape='spline'
    )
)

fig3.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickcolor='rgb(204, 204, 204)',
        tickformat= '%b %d',
        type='date',
        #dtick= 86400000.0,
    ),
    showlegend=True,
    plot_bgcolor='white',
    title_x=0.5,
    xaxis_range=[tracking_data.Date.min()-timedelta(days=1),tracking_data.Date.max()+timedelta(days=1)],
    hovermode='x unified',
    legend_title_text = 'Candidate',
    margin={"l":100,"r":100,"t":130,"b":130},
    yaxis_range=[0,100],
    # annotations = [dict(xref='paper',
    #     yref='paper',
    #     x=1, y=-0.3,
    #     showarrow=False,
    #     text ='*confidence intervals contain 95% of sample means',
    #     font=dict(
    #         size=10,
    #         ),)]
)

fig3.update_yaxes(
    title_text = "Simulations Won(%)",
    ticksuffix="%"
)

fig3.add_traces([go.Scatter(
        x = tracking_data.query('Candidate == "Trump"')['Date'], 
        y = tracking_data.query('Candidate == "Trump"')['UB'],
        name = "",
        mode = 'lines', line_color = 'rgba(0,0,0,0)',
        hoverinfo = 'skip',
        showlegend = False),
    go.Scatter(
        x = tracking_data.query('Candidate == "Trump"')['Date'], 
        y = tracking_data.query('Candidate == "Trump"')['LB'],
        name = "",
        mode = 'lines', line_color = 'rgba(0,0,0,0)',
        fill='tonexty', fillcolor = 'rgba(255, 0, 0, 0.2)',
        hoverinfo = 'skip',
        showlegend = False)])

fig3.add_traces([go.Scatter(
        x = tracking_data.query('Candidate == "Biden"')['Date'], 
        y = tracking_data.query('Candidate == "Biden"')['UB'],
        name = "97.5 Win Perc",
        hovertext = None,
        showlegend = False,
        hoverinfo = 'skip',
        mode = 'lines', line_color = 'rgba(0,0,0,0)'),
    go.Scatter(
        x = tracking_data.query('Candidate == "Biden"')['Date'], 
        y = tracking_data.query('Candidate == "Biden"')['LB'],
        name = "2.5 Win Perc.",
        hovertext = None,
        mode = 'lines', line_color = 'rgba(0,0,0,0)',
        hovertemplate = '',
        showlegend = False,
        hoverinfo = 'skip',
        fill='tonexty', fillcolor = 'rgba(0, 0, 255, 0.2)')])

#
#
#
#
#
#
#| content: valuebox
#| title: "Today's Projected Winner"

win_perc = sum(simulation_data['points']>=270)/simulation_data.shape[0]
win_perc = round(win_perc*100,2)

if win_perc>50:
    color = 'red'
    value = 'Trump'
else:
    color = 'blue'
    value = 'Biden'

dict(
    icon = "trophy",
    color = color,
    value = value
)
#
#
#
#| content: valuebox
#| title: "Percentage of Simulations Won"

win_perc = sum(simulation_data['points']>=270)/simulation_data.shape[0]
win_perc = round(win_perc*100,2)

if win_perc < 50:
    win_perc = 100 - win_perc

dict(
    icon = "percent",
    color = "light",
    value = win_perc,
) 
#
#
#
#| content: valuebox
#| title: "Last Updated"

import datetime
x = datetime.datetime.now()

dict(
    icon = "calendar",
    color = "light",
    value = x.strftime("%d %b %Y"),
) 
#
#
#
#
#
#
#
#
#| title: Trump Win Probability By State
#| padding: 0
fig.show(config=config)
#
#
#
#
#
#
#
#| title: Simulations Won Today
#| padding: 0
fig2.show(config=config)
#
#
#
#| title: Simulations Won Over Time
#| padding: 0
fig3.show(config=config)
#
#
#
#
#
