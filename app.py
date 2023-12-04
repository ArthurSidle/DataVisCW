from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
from zipfile import ZipFile
import get_data


def get_df_from_zip(file, csv, index_col=False):
    with ZipFile(f"data/{file}.zip") as archive:
        file = archive.open(f"{csv}.csv")
        df = pd.read_csv(file, index_col=index_col)
        file.close()
    return df

steam_data = get_data.get_steam_data()
missing_percent_fig = go.Figure(go.Funnel(x=steam_data["percent"]["x"], y=steam_data["percent"]["y"]))

no_of_steam_games = steam_data["percent"]["x"][0]
no_of_lost_steam_games = steam_data["percent"]["x"][1]
lost_percent_steam = round((no_of_lost_steam_games / (no_of_steam_games + no_of_lost_steam_games)) * 100, 2)

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
        html.H2("The Full Scope"),
        html.P(f"There are {no_of_steam_games} games on steam. However, {no_of_lost_steam_games} are lost. That comprises {lost_percent_steam}% of all games ever released on the platform."),
        dcc.Graph(figure=missing_percent_fig)
        ], className="container-fluid px-xxl-5"
    )
], className="bg-light")

if __name__ == "__main__":
    app.run(debug=True)