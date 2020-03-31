# pylint: disable=import-error
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
from joblib import load
# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout

pipeline = load('assets/logistic.joblib')

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown('#### Police Agency Name'),
        dcc.Dropdown(
            id='agency_name',
            options = [
                {'label': 'Chicago PD', 'value': 'CHICAGO-PD'},
                {'label': 'Philadelphia PD', 'value': 'PHILADELPHIA-PD'},
                {'label': 'Los Angeles PD', 'value': 'LOS-ANGELES-PD'}
            ],
            value = 'CHICAGO-PD',
            className='mb-4',
        ),
        dcc.Markdown('#### Firearm Indicated'),
        dcc.Dropdown(
            id='firearm_ind',
            options = [
                {'label': 'No Firearm', 'value': 'N'},
                {'label': 'Firearm Present', 'value': 'Y'},
                {'label': 'Data Missing', 'value': 'MISSING'}
            ],
            value = 'Y',
            className='mb-4',
        ),
    ],
    md=4,
)
"""
column2 = dbc.Col(
    [
        #dcc.Markdown('## .', className='mb-5'),




        dcc.Markdown('#### Longitude (In Central Park)'),
        dcc.Slider(
            id='Longitude',
            min=-73.981159,
            max=-73.949722,
            step=0.0005,
            value=-73.967238,
            #marks={i: 'Label {}'.format(i) for i in range(10)},

        ),
        html.Div(id='slider-output-container1'),

        dcc.Markdown('#### Latitude (In Central Park)'),
        dcc.Slider(
            id='Latitude',
            min=40.764911,
            max=40.800119,
            step=0.0005,
            value=40.780775,
            #marks={n: str(n) for n in range(1960,2060,20)},

        ),
        html.Div(id='slider-output-container2'),


    ]
) """

column2 = dbc.Col(
    [

        html.H2('Clearance Prediction', className='mb-3'),
        html.Div(id='prediction-content', className='lead'),
 #       html.Div(id='prediction-image', className='lead'),

    #daq.Gauge(
    #d='my-daq-gauge',
    #min=0,
    #max=10,
    #value=6
    #),




    ]
)

layout = dbc.Row([column1, column2])


import pandas as pd

@app.callback(
    Output('prediction-content', 'children'),
    [Input('agency_name', 'value'), Input('firearm_ind', 'bool')],
)
def predict(agency_name, firearm_ind):
    df = pd.DataFrame(
        columns=['agency_name', 'firearm_ind'],
        data=[[agency_name, firearm_ind]]
    )
    y_pred = pipeline.predict(df)[0]
    if y_pred == True:
        return f'This case was likely cleared!'
    else:
        return f'This case was likely unsolved.'

"""
This uses the pipeline to call back an image - stylization.
@app.callback(
    Output('prediction-image', 'children'),
    [Input('Shift', 'value'), Input('Foraging', 'bool'), Input('Longitude', 'value'), Input('Latitude', 'value'),
    Input('Primary_Fur_Color', 'value'), Input('Eating', 'bool'), Input('Highlight_Fur_Color', 'value') ],
)

def predict(Shift, Foraging, X, Y, Primary_Fur_Color, Eating, Highlight_Fur_Color):
    df = pd.DataFrame(
        columns=['Shift', 'Foraging', 'Longitude', 'Latitude', 'Primary_Fur_Color', 'Eating', 'Highlight_Fur_Color'],
        data=[[Shift, Foraging, X, Y, Primary_Fur_Color, Eating, Highlight_Fur_Color]]
    )
    y_pred = pipeline.predict(df)[0]
    if y_pred == True:
        return html.Img(src='assets/squirrel_approach.png',className='img-fluid', style = {'height': '300px'})
    else:
        return html.Img(src='assets/squirrel_runs.png',className='img-fluid', style = {'height': '300px'}) """

@app.callback(
    dash.dependencies.Output('slider-output-container1', 'children'),
    [dash.dependencies.Input('Longitude', 'value')])
def update_output(value):
    return 'You have entered "{}"'.format(value)

@app.callback(
    dash.dependencies.Output('slider-output-container2', 'children'),
    [dash.dependencies.Input('Latitude', 'value')])
def update_output(value):
    return 'You have entered "{}"'.format(value)
