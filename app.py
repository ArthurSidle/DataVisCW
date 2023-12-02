from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from zipfile import ZipFile
import get_data

def get_df_from_zip(file, csv, index_col=False):
    with ZipFile(f"data/{file}.zip") as archive:
        file = archive.open(f"{csv}.csv")
        df = pd.read_csv(file, index_col=index_col)
        file.close()
    return df

#df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")
df = get_df_from_zip("steam", "steam", index_col=0)
df = df.sample(10000)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.Div([
        html.H1("Missing Software", className="text-center"),
        html.P(
            "Over the couple of decades that digital media has existed, there have already been many cases of media going missing. By comparing databases of software collected at different times, or using data collected by fans, we can gain insights into the full extent of the phenomenon and infer trends among lost media.",
            className="text-center"
        )], className="container-lg mx-auto"
    ),
    html.Div([
        html.Div([
            html.Div(html.Div("Hello world", className="p-3 bg-primary"), className="col"),
            html.Div(html.Div("Hello world", className="p-3 bg-primary"), className="col"),
            html.Div(html.Div("Hello world", className="p-3 bg-primary"), className="col")
        ], className='row p-3 gx-5 text-center bg-light')
    ],
        className="container-fluid px-xxl-5"
    )
], className="bg-light")

if __name__ == "__main__":
    app.run(debug=True)