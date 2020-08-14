import plotly.graph_objects as go
import dash
import numpy as np
import pandas as pd
import os

import plotly.offline as pyo
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt
from dash.dependencies import State, Input, Output
from dash.exceptions import PreventUpdate



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
    #mask=(sample_data['prediction_proba'] > 0.2)
    sample_data=sample_data.loc[(sample_data['prediction_proba']>0.02) | (sample_data['original_label']>0.02)]
    sample_data=sample_data.sort_values(by='sentid')
    plot_data=[]
    #plot_data.append(go.Scatter(x=sample_data['sentid'], y=sample_data['prediction_proba']))

    plot_layout=go.Layout(title="Probability that a sentence has coordinates")
    #fig = go.Figure(data = plot_data, layout=plot_layout)
    fig = go.Figure(layout=plot_layout)
    fig.add_trace(go.Scatter(x=sample_data['sentid'], y=sample_data['prediction_proba'], mode='markers', name='proba'))
    fig.add_trace(go.Scatter(x=sample_data['sentid'], y=sample_data['original_label'], mode='markers', name='original label'))
    fig.update_layout(yaxis=dict(range=[0,1.02]))
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
                                html.Div(children=[html.P('Choose a paper:'),
                                                   dcc.Dropdown(id="title_dropdown",
                                                                options=options_list,
                                                                value='Paradigms and proboscideans in the southern Great Lakes region, USA')]),
                                                   html.Div(id='gddid_output', style={'whiteSpace': 'pre-line'}),

                                dcc.Tabs(id='tabs-example', value='tab-1', children=[
                                                                                     dcc.Tab(label='Graphics', value='tab-1'),
                                                                                     dcc.Tab(label='Complete article', value='tab-2'),
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
    gdd = sample_data['_gddid'].unique()
    return 'The GDDID for that title is: \n{}'.format(gdd)

# Table

@app.callback(Output('json_df_store', 'children'),
              [Input('title_dropdown', 'value'),
               Input('sentid_dropdown', 'value')])
def load_table(input_title, input_sentid):
    try:
        data=''
        data= datagen()
        data.reset_index(inplace=True)
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
    data = info_dataframe.to_dict("rows")
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
                          style_cell={'width': '50px',
                                      'height': '30px',
                                      'textAlign': 'left'}
                          )])
    return child


# Table2

@app.callback(Output('json_df_store_t2', 'children'),
              [Input('title_dropdown', 'value')])
def load_table_t2(input_title):
    data =''
    data= datagen()
    data.reset_index(inplace=True)
    data=data[data['title'] == input_title]
    data['coordinates(y/n)'] = ''
    data=data[['sentid','sentence', 'prediction_proba', 'predicted_label','coordinates(y/n)']]

    data=data.to_json()
    return data

@app.callback(Output('table_output_t2', 'children'),
              [Input('json_df_store_t2', 'children')])

def update_output_t2(json_df_t2):
    info_dataframe_t2 = pd.read_json(json_df_t2)
    info_dataframe_t2.reset_index(drop=True, inplace=True)
    data = info_dataframe_t2.to_dict("rows")
    cols = [{"name": i, "id": i} for i in info_dataframe_t2.columns]

    child2 = html.Div([
            html.Button(id="save-button",n_clicks=0,children="Save"),
            html.Div(id="output-1",children="Mark the last column if the sentence has a coordinate. Press button to save changes"),
            dt.DataTable(style_data={
                                     'whiteSpace': 'normal',
                                     'height': 'auto',
                                     'lineHeight': '15px'
                                     },
                          id='table',
                          data=data,
                          columns=[{'name': 'sentid', 'id': 'sentid', 'editable':False},
                                   {'name': 'sentence', 'id': 'sentence', 'editable':False},
                                   {'name': 'prediction_proba', 'id': 'prediction_proba', 'editable':False},
                                   {'name': 'predicted_label', 'id': 'predicted_label', 'editable':False},
                                   {'name': 'coordinates(y/n)','id': 'coordinates(y/n)', 'editable': True}],
                          sort_action='native',
                          filter_action='native',
                          style_cell={'width': '50px',
                                      'height': '30px',
                                      'textAlign': 'left'},

                          merge_duplicate_headers=True
                          )
            ])
    return child2

# Save Button
@app.callback(
        Output("output-1","children"),
        [Input("save-button","n_clicks")],
        [State("table","data")]
        )

def selected_data_to_csv(nclicks,table1):

    if nclicks == 0:
        raise PreventUpdate
    else:
        #gdd_name=''
        #gdd_name = gddid_output
        #print(gdd_name)

        #gdd_name = gdd_name.append('.tsv')
        gdd_name = 'file.tsv'
        path = r'/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output/from_dashboard'
        output_file = os.path.join(path,gdd_name)

        pd.DataFrame(table1).to_csv(output_file, sep='\t', index = False)
        return "Data Submitted"


# Tabs
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])

def render_content(tab):
    if tab == 'tab-1':
        return html.Div(children=[#Graph
                                  dcc.Graph(id='proba_graph'),

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
        return html.Div(children=[#Table
                                  #Div to store json serialized dataframe
                                  html.Div(id='json_df_store_t2', style={'display':'none'}),
                                  html.Div(id='table_output_t2')
                                  ])



if __name__ == '__main__':
    app.run_server(debug=True)
