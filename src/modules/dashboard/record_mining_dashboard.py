import plotly.graph_objects as go
import dash
import numpy as np
import pandas as pd

import plotly.offline as pyo
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from dash.dependencies import State, Input, Output

data = pd.read_csv('/Users/seiryu8808/Desktop/UWinsc/Github/UnacquiredSites/src/output/predictions/comparison_file.tsv', sep='\t')
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

# Options list for selecting GDDID
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
    Base_Data = data
    return(Base_Data)

# Figure generator for first graph
def fig_generator(sample_data):
    sample_data.reset_index(drop=True)
    sample_data=sample_data.sort_values(by='sentid')

    plot_data=go.Scatter(x=sample_data['sentid'], y=sample_data['prediction_proba'])
    plot_layout=go.Layout(title="This is a graph")

    fig = go.Figure(data = plot_data, layout=plot_layout)
    return(fig.data, fig.layout)

def table_generator(data, sentence_id):
    a=data[data['sentid'] == sentence_id-1]
    b=data[data['sentid'] == sentence_id]
    c=data[data['sentid'] == sentence_id+1]
    df = pd.concat([a,b,c])
    return df


# Dash application
app = dash.Dash()

app.layout = html.Div(children = [
    html.H1('Record Mining Dashboard'),
    html.Div([
                html.P('Choose a GDDID:'),
                dcc.Dropdown(
                            id="drop_down_1",
                            options=options_list,
                            value='54b43249e138239d8684a1b2')]),
    dcc.Graph(
              id='proba_graph'),
    html.Div([
                html.P('Choose a sentence number:'),
                dcc.Dropdown(
                 id="sentid_dropdown",
                 options=sent_opt_list,
                 value='5')]),

    html.Div(id = 'my-output', children = [
    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in data.columns],
                        data=data.to_dict('rows')
                        )])
    ])

@app.callback(Output('proba_graph', 'figure'),
              [Input('drop_down_1', 'value')])
def updateplot(input_gddid):
    df= datagen()
    sample_data = df[df["_gddid"] == input_gddid]
    trace,layout = fig_generator(sample_data)
    return {
           'data': trace,
           'layout':layout
           }

@app.callback(Output('my-output', 'children'),
             [Input('drop_down_1', 'value'),
              Input('sentid_dropdown', 'value')])

def table_generator(gddid, sentence_id):
    try:
        data= datagen()
        data=data[data['_gddid'] == gddid]
        a=data[data['sentid'] == int(sentence_id)-1]
        b=data[data['sentid'] == int(sentence_id)]
        c=data[data['sentid'] == int(sentence_id)+1]
        data = pd.concat([a,b,c])
        return data.to_json()
    except:
        print('Can\'t find that index')



if __name__ == '__main__':
    app.run_server(debug=True)
