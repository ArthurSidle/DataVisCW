from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from flask import Flask
import pandas as pd
import plotly.express as px
from plotly import graph_objects as go
from zipfile import ZipFile
from get_data import *

steam_data = get_steam_data()
delisters = get_delisters()
genres = get_genres() # genres for lost games
genres_other = get_genres_other() # genres for all games
ratings_lost = get_ratings_lost()
ratings = get_ratings()

missing_percent_fig = go.Figure(
    go.Funnel(x=steam_data["percent"]["x"], y=steam_data["percent"]["y"]))
delisters_fig = px.bar(delisters, x="company_name", y="count")
genres_fig = px.pie(genres, values="count", names="genre", title="Lost Games' Genres")
genres_other_fig = px.pie(genres_other, values="count", names="genre", title="Available Games' Genres")
ratings_lost_fig = px.bar(ratings_lost, x="rating_range", y="count", title="Lost Games' Rating")
ratings_fig = px.bar(ratings, x="rating_range", y="count", title="Available Games' Rating")

no_of_steam_games = steam_data["percent"]["x"][0]
no_of_lost_steam_games = steam_data["percent"]["x"][1]
lost_percent_steam = round(
    (no_of_lost_steam_games / (no_of_steam_games + no_of_lost_steam_games)) * 100, 2)

flask_server = Flask(__name__)
app = Dash(__name__, server=flask_server,
           external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

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
    ),
    html.Div([
        html.H2("Serial Delisters"),
        html.P(
            "Some companies have a habit of removing their games from digital storefronts."),
        dcc.Graph(figure=delisters_fig)
    ], className="container-fluid px-xxl-5"
    ),
    html.Div([
        html.H2("Does the genre make it more likely?"),
        html.P(
            "Some types of games are more likely to disappear than others."),
        dcc.Graph(figure=genres_fig),
        dcc.Graph(figure=genres_other_fig)
    ], className="container-fluid px-xxl-5"),
    html.Div([
        html.H2("Does rating influence delisting?"),
        html.P(
            "Delisted games often have lower ratings than their contemporaries"),
        dcc.Graph(figure=ratings_lost),
        dcc.Graph(figure=ratings)
    ], className="container-fluid px-xxl-5")
], className="bg-light")

if __name__ == "__main__":
    app.run(debug=True)
