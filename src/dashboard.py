import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from database import DatabaseConnection, init_database

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("COVID-19 Dashboard")
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([], width=12)
    ])
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=True)
