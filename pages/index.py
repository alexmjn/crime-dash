# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from functions.load_data import load_data, create_binary_target, define_target
from functions.load_data import extract_time_and_date, clean_age_category
from functions.load_data import separate_black_hispanic, wrangle, wrangle_data
from functions.load_data import generate_most_common
# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
           """
           App lets users interactively examine what factors lead to crimes
           being solved or not.
           """
        ),
        dcc.Link(dbc.Button('Your Call To Action', color='primary'), href='/predictions')
    ],
    md=4,
)

# pass a data frame here -- how best way?
train, val, test = load_data()
train, val, test = define_target(train, val, test)
train, val, test = wrangle_data(train, val, test)
df = generate_most_common("agency_name", 8, train)

fig = px.bar(df, x="agency_name", y="cleared", color="firearm_ind",
           )

column2 = dbc.Col(
    [
        dcc.Graph(figure=fig),
    ]
)

layout = dbc.Row([column1, column2])
