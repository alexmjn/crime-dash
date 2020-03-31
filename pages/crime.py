import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
#from joblib import load
#pipeline = load('assets/logistic.joblib')

from app import app

column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Predicting Crime Clearance


            """
        ),
    ],
    md=4,
)

column1 = dbc.Col(
    [
        dcc.Markdown('## Predictions', className='mb-5'),
        dcc.Markdown('#### Year'),
        dcc.Slider(
            id='year',
            min=1955,
            max=2055,
            step=5,
            value=2020,
            marks={n: str(n) for n in range(1960,2060,20)},
            className='mb-5',
        ),
        dcc.Markdown('#### Continent'),
        dcc.Dropdown(
            id='continent',
            options = [
                {'label': 'Africa', 'value': 'Africa'},
                {'label': 'Americas', 'value': 'Americas'},
                {'label': 'Asia', 'value': 'Asia'},
                {'label': 'Europe', 'value': 'Europe'},
                {'label': 'Oceania', 'value': 'Oceania'},
            ],
            value = 'Africa',
            className='mb-5',
        ),
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.H2('Expected Lifespan', className='mb-5'),
        html.Div(id='prediction-content', className='lead')
    ]
)
layout = dbc.Row([column1, column2])
