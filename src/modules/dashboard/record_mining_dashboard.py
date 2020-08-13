import plotly.graph_objects as go
import dash
import numpy as np
import pandas as pd

import plotly.offline as pyo
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import State, Input, Output



#Loading Data
data_test = pd.read_csv('src/output/predictions/comparison_file.tsv', sep='\t')
data_train = pd.read_csv('src/output/predictions/dashboard_file.tsv', sep='\t')
data = pd.concat([data_train, data_test])

# GDDID dropdown
gddid_list = list(data['title'].unique())
options_list = []
for i in gddid_list:
    options_list.append({'label':i, 'value':i})

# Sentence ID dropdown
sentid_list = list(data['sentid'].unique())
list.sort(sentid_list)
sent_opt_list = []
for i in sentid_list:
    sent_opt_list.append({'label':i, 'value':i})

# Data Generator
def datagen(data = data):
    data=data[['title', '_gddid', 'sentence', 'sentid', 'prediction_proba', 'original_label', 'predicted_label', 'found_lat', 'found_long', 'train/test']]
    return(data)

# Figure generator for first graph
def fig_generator(sample_data):
    sample_data.reset_index(drop=True)
    sample_data=sample_data.sort_values(by='sentid')
    plot_data=[]
    plot_data.append(go.Scatter(x=sample_data['sentid'], y=sample_data['prediction_proba']))

    plot_layout=go.Layout(title="Probability that a sentence has coordinates")
    fig = go.Figure(data = plot_data, layout=plot_layout)
    return(fig.data, fig.layout)



def table_generator(data):
    data.reset_index(drop=True)
    data=sample_data.sort_values(by='sentid')
    data=data[['sentence', 'sentid', 'prediction_proba', 'original_label', 'predicted_label', 'found_lat', 'found_long']]
    return data.to_json()


# Dash application
app = dash.Dash()
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div(children=[html.H1('Record Mining Dashboard'),
                                dcc.Tabs(id='tabs-example', value='tab-1', children=[
                                                                                     dcc.Tab(label='Tab one', value='tab-1'),
                                                                                     dcc.Tab(label='Tab two', value='tab-2'),
                                                                                     ]),
                                html.Div(id='tabs-example-content')
                                ])


# Graph
@app.callback(Output('proba_graph', 'figure'),
              [Input('title_dropdown', 'value')])

def update_plot(input_title):
    df= datagen()
    sample_data = df[df["title"] == input_title]
    trace,layout = fig_generator(sample_data)
    return {
           'data': trace,
           'layout':layout
           }

# GDD output
@app.callback(Output('gddid_output', 'children'),
              [Input('title_dropdown', 'value')])

def update_output(input_title):
    df= datagen()
    sample_data = df[df["title"] == input_title]
    title = sample_data['_gddid'].unique()
    return 'The GDDID for that title is: \n{}'.format(title)

# Table

@app.callback(Output('json_df_store', 'children'),
              [Input('title_dropdown', 'value'),
               Input('sentid_dropdown', 'value')])
def load_table(input_title, input_sentid):
    try:
        data= datagen()
        data=data[data['title'] == input_title]
        data=data[['sentence', 'sentid', 'prediction_proba', 'original_label', 'predicted_label', 'found_lat', 'found_long', 'train/test']]
        a=data[data['sentid'] == int(input_sentid)-1]
        b=data[data['sentid'] == int(input_sentid)]
        c=data[data['sentid'] == int(input_sentid)+1]
        data = pd.concat([a,b,c])
        data=data.to_json()
        return data

    except:
        print('Can\'t find that index')



@app.callback(Output('table_output', 'children'),
              [Input('json_df_store', 'children')])

def update_output(json_df):
    info_dataframe = pd.read_json(json_df)
    data = info_dataframe .to_dict("rows")
    cols = [{"name": i, "id": i} for i in info_dataframe.columns]

    child = html.Div([
            dt.DataTable(style_data={
                                     'whiteSpace': 'normal',
                                     'height': 'auto',
                                     'lineHeight': '15px'
                                     },
                          id='table',
                          data=data,
                          columns=cols,
                          sort_action='native',
                          filter_action='native',
                          style_cell={'width': '50px',
                                      'height': '30px',
                                      'textAlign': 'left'}
                          )])
    return child

# Tabs
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div(children=[
                                  #Graph
                                  html.Div(children=[html.P('Choose a paper:'),
                                                     dcc.Dropdown(id="title_dropdown",
                                                                  options=options_list,
                                                                  value='Paradigms and proboscideans in the southern Great Lakes region, USA')]),
                                                     dcc.Graph(id='proba_graph'),
                                                     html.Div(id='gddid_output', style={'whiteSpace': 'pre-line'}),
                                  #Table
                                  html.Div(children=[html.P('Choose a sentence number:'),
                                                     dcc.Dropdown(id="sentid_dropdown",
                                                                  options=sent_opt_list,
                                                                  value='5')]),
                                  #Div to store json serialized dataframe
                                  html.Div(id='json_df_store', style={'display':'none'}),
                                  html.Div(id='table_output')

                                  ])

    elif tab == 'tab-2':
        return html.Div(children=[
                                  html.Div(children=[html.P('Choose a paper:'),
                                                     dcc.Dropdown(id="title_dropdown",
                                                                  options=options_list,
                                                                  value='Paradigms and proboscideans in the southern Great Lakes region, USA')]),
                                                     html.Div(id='gddid_output', style={'whiteSpace': 'pre-line'})
                                  #Table
                                  ])



if __name__ == '__main__':
    app.run_server(debug=True)
