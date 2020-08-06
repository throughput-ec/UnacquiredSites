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
data = pd.read_csv('src/output/predictions/comparison_file.tsv', sep='\t')

# GDDID dropdown
gddid_list = list(data['_gddid'].unique())
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
    data=data[['_gddid', 'sentence', 'sentid', 'prediction_proba', 'predicted_label', 'found_lat', 'found_long']]
    return(data)

# Figure generator for first graph
def fig_generator(sample_data):
    sample_data.reset_index(drop=True)
    sample_data=sample_data.sort_values(by='sentid')

    plot_data=go.Scatter(x=sample_data['sentid'], y=sample_data['prediction_proba'])
    plot_layout=go.Layout(title="Probability that a sentence has coordinates")

    fig = go.Figure(data = plot_data, layout=plot_layout)
    return(fig.data, fig.layout)



def table_generator(data):
    data.reset_index(drop=True)
    data=sample_data.sort_values(by='sentid')
    #data=data[data['_gddid'] == gddid]
    data=data[['sentence', 'sentid', 'prediction_proba', 'predicted_label', 'found_lat', 'found_long']]
    #a=data[data['sentid'] == int(sentence_id)-1]
    #b=data[data['sentid'] == int(sentence_id)]
    #c=data[data['sentid'] == int(sentence_id)+1]
    #data = pd.concat([a,b,c])
    return data.to_json()


# Dash application
app = dash.Dash()

app.layout = html.Div(children = [
                                  html.H1('Record Mining Dashboard'),
                                  #Graph
                                  html.Div(children=[
                                                     html.P('Choose a GDDID:'),
                                                     dcc.Dropdown(
                                                                  id="gddid_dropdown",
                                                                  options=options_list,
                                                                  value='54b43249e138239d8684a1b2')]),
                                  dcc.Graph(id='proba_graph'),
                                  # Table
                                  html.Div([
                                            html.P('Choose a sentence number:'),
                                            dcc.Dropdown(
                                                         id="sentid_dropdown",
                                                         options=sent_opt_list,
                                                         value='5')]),
                                # Div to store json serialized dataframe
                                html.Div(id='json_df_store', style={'display':'none'}),
                                html.Div(id='table_output')
                                                          ])
# Graph
@app.callback(Output('proba_graph', 'figure'),
              [Input('gddid_dropdown', 'value')])

def update_plot(input_gddid):
    df= datagen()
    sample_data = df[df["_gddid"] == input_gddid]
    trace,layout = fig_generator(sample_data)
    return {
           'data': trace,
           'layout':layout
           }

# Table

@app.callback(Output('json_df_store', 'children'),
              [Input('gddid_dropdown', 'value'),
               Input('sentid_dropdown', 'value')])
def load_table(input_gddid, input_sentid):
    try:
        data= datagen()
        data=data[data['_gddid'] == input_gddid]
        data=data[['sentence', 'sentid', 'prediction_proba', 'predicted_label', 'found_lat', 'found_long']]
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
                                 style_cell={'width': '50px',
                                            'height': '30px',
                                            'textAlign': 'left'}
                                            )
                       ])
    return child





if __name__ == '__main__':
    app.run_server(debug=True)
