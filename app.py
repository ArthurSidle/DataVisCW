from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
from zipfile import ZipFile

def get_df_from_zip(file, csv, index_col=False):
    with ZipFile(f'data/{file}.zip') as archive:
        file = archive.open(f'{csv}.csv')
        df = pd.read_csv(file, index_col=index_col)
        file.close()
    return df

#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
df = get_df_from_zip('spotify', 'spotify_data', index_col=0)
df = df.sample(10000)

app = Dash(__name__)

app.layout = html.Div([
    html.Div(className='row',
             children='Music data app',
             style={'textAlign': 'center', 'color': 'blue', 'fontSize': 30}
    ),
    html.Div(className='row', children=[
        dcc.RadioItems(options=['popularity', 'danceability', 'speechiness'],
                       value='popularity',
                       id='controls-and-radio-item')
    ]),
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            dash_table.DataTable(data=df.to_dict('records'), page_size=11, style_table={'overflowX': 'auto'})
        ]),
        html.Div(className='six columns', children=[
            dcc.Graph(figure={}, id='controls-and-graph')
        ])
    ])
])

@callback(
    Output(component_id='controls-and-graph', component_property='figure'),
    Input(component_id='controls-and-radio-item', component_property='value')
)
def update_graph(col_chosen):
    fig = px.histogram(df, x='genre', y=col_chosen, histfunc='avg')
    return fig

if __name__ == '__main__':
    app.run(debug=True)