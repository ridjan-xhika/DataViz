import dash
from dash import dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.database import DatabaseConnection

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

COLORS = {
    'confirmed': '#FF6B6B',
    'deaths': '#4ECDC4',
    'recovered': '#95E1D3',
    'countries': '#FFD93D',
    'background': '#0F1419',
    'card_bg': '#1A1F2E',
    'text': '#FFFFFF',
    'text_secondary': '#B0B8C1'
}

def get_data():
    try:
        db = DatabaseConnection()
        if not db.connect():
            return pd.DataFrame()
        cursor = db.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM covid_data ORDER BY date DESC LIMIT 100000")
        results = cursor.fetchall()
        cursor.close()
        db.disconnect()
        return pd.DataFrame(results) if results else pd.DataFrame()
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def get_countries():
    try:
        df = get_data()
        return sorted(df['country'].unique().tolist()) if not df.empty else []
    except:
        return []

app.layout = dbc.Container([
    html.Div(id="page-content", style={
        "background": COLORS['background'],
        "color": COLORS['text'],
        "minHeight": "100vh",
        "padding": "40px 20px"
    }, children=[
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("COVID-19 Tracker", className="fw-bold", style={"fontSize": "3.5rem", "marginBottom": "0.5rem"}),
                    html.P("Real-time pandemic monitoring dashboard", style={"color": COLORS['text_secondary'], "fontSize": "1.1rem"})
                ])
            ], width=12)
        ], className="mb-5"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.P("Total Confirmed", style={"color": COLORS['text_secondary'], "marginBottom": "0.5rem", "fontSize": "0.9rem"}),
                            html.H2(id="confirmed-stat", children="0", style={"color": COLORS['confirmed'], "fontWeight": "bold"})
                        ])
                    ], style={"padding": "1.5rem"})
                ], style={"background": COLORS['card_bg'], "border": f"2px solid {COLORS['confirmed']}", "borderRadius": "12px"})
            ], md=3, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.P("Total Deaths", style={"color": COLORS['text_secondary'], "marginBottom": "0.5rem", "fontSize": "0.9rem"}),
                            html.H2(id="deaths-stat", children="0", style={"color": COLORS['deaths'], "fontWeight": "bold"})
                        ])
                    ], style={"padding": "1.5rem"})
                ], style={"background": COLORS['card_bg'], "border": f"2px solid {COLORS['deaths']}", "borderRadius": "12px"})
            ], md=3, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.P("Total Recovered", style={"color": COLORS['text_secondary'], "marginBottom": "0.5rem", "fontSize": "0.9rem"}),
                            html.H2(id="recovered-stat", children="0", style={"color": COLORS['recovered'], "fontWeight": "bold"})
                        ])
                    ], style={"padding": "1.5rem"})
                ], style={"background": COLORS['card_bg'], "border": f"2px solid {COLORS['recovered']}", "borderRadius": "12px"})
            ], md=3, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.P("Countries Affected", style={"color": COLORS['text_secondary'], "marginBottom": "0.5rem", "fontSize": "0.9rem"}),
                            html.H2(id="countries-stat", children="0", style={"color": COLORS['countries'], "fontWeight": "bold"})
                        ])
                    ], style={"padding": "1.5rem"})
                ], style={"background": COLORS['card_bg'], "border": f"2px solid {COLORS['countries']}", "borderRadius": "12px"})
            ], md=3, className="mb-4")
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Filters", style={"marginBottom": "1.5rem", "fontWeight": "bold"}),
                        html.Label("Country:", style={"marginBottom": "0.5rem", "fontWeight": "600"}),
                        dcc.Dropdown(
                            id="country-dropdown",
                            options=[],
                            placeholder="Select a country (optional)...",
                            style={"color": "#000", "borderRadius": "8px"}
                        ),
                        html.Br(),
                        html.Label("Metric:", style={"marginBottom": "0.5rem", "fontWeight": "600"}),
                        dcc.Dropdown(
                            id="chart-type",
                            options=[
                                {"label": "📊 Confirmed Cases", "value": "confirmed"},
                                {"label": "💀 Deaths", "value": "deaths"},
                                {"label": "✅ Recovered", "value": "recovered"}
                            ],
                            value="confirmed",
                            style={"color": "#000", "borderRadius": "8px"}
                        )
                    ], style={"background": COLORS['card_bg']})
                ], style={"background": COLORS['card_bg'], "border": "none", "borderRadius": "12px"})
            ], md=3, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id="trend-chart", style={"height": "400px", "marginBottom": "0"})
                    ], style={"padding": "1rem", "background": COLORS['card_bg']})
                ], style={"background": COLORS['card_bg'], "border": "none", "borderRadius": "12px"})
            ], md=9, className="mb-4")
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(id="global-chart", style={"height": "500px", "marginBottom": "0"})
                    ], style={"padding": "1rem", "background": COLORS['card_bg']})
                ], style={"background": COLORS['card_bg'], "border": "none", "borderRadius": "12px"})
            ], width=12)
        ]),
        
        dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
    ])
], fluid=True, style={"padding": "0", "maxWidth": "100%"})

@callback(
    [Output("confirmed-stat", "children"),
     Output("deaths-stat", "children"),
     Output("recovered-stat", "children"),
     Output("countries-stat", "children"),
     Output("country-dropdown", "options")],
    Input("interval-component", "n_intervals")
)
def update_stats(_):
    try:
        df = get_data()
        if df.empty:
            return "0", "0", "0", "0", []
        
        latest_date = df['date'].max()
        latest_data = df[df['date'] == latest_date]
        
        total_confirmed = int(latest_data['confirmed'].sum())
        total_deaths = int(latest_data['deaths'].sum())
        total_recovered = int(latest_data['recovered'].sum())
        countries = get_countries()
        
        return (
            f"{total_confirmed:,}",
            f"{total_deaths:,}",
            f"{total_recovered:,}",
            f"{len(countries)}",
            [{"label": c, "value": c} for c in countries]
        )
    except Exception as e:
        print(f"Error updating stats: {e}")
        return "0", "0", "0", "0", []

@callback(
    Output("trend-chart", "figure"),
    [Input("country-dropdown", "value"),
     Input("chart-type", "value"),
     Input("interval-component", "n_intervals")]
)
def update_trend(country, chart_type, _):
    try:
        df = get_data()
        
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No data available")
            return fig
        
        if country:
            df = df[df['country'] == country]
        
        df = df.groupby('date').agg({
            'confirmed': 'sum',
            'deaths': 'sum',
            'recovered': 'sum'
        }).reset_index().sort_values('date')
        
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No data for selected country")
            return fig
        
        fig = px.line(
            df,
            x="date",
            y=chart_type,
            title=f"<b>{chart_type.upper()} CASES TREND</b>" + (f"<br><sub>{country}</sub>" if country else "<br><sub>Global</sub>"),
            labels={"date": "Date", chart_type: "Count"}
        )
        
        color_map = {'confirmed': COLORS['confirmed'], 'deaths': COLORS['deaths'], 'recovered': COLORS['recovered']}
        
        fig.update_traces(line=dict(color=color_map[chart_type], width=3))
        fig.update_layout(
            hovermode="x unified",
            template="plotly_dark",
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text'], size=12),
            title_font_size=16,
            margin=dict(l=50, r=50, t=60, b=50),
            xaxis=dict(gridcolor='#2A3543'),
            yaxis=dict(gridcolor='#2A3543')
        )
        return fig
    except Exception as e:
        print(f"Error updating trend: {e}")
        fig = go.Figure()
        fig.add_annotation(text=f"Error loading chart")
        return fig

@callback(
    Output("global-chart", "figure"),
    [Input("chart-type", "value"),
     Input("interval-component", "n_intervals")]
)
def update_global(chart_type, _):
    try:
        df = get_data()
        
        if df.empty:
            fig = go.Figure()
            fig.add_annotation(text="No data available")
            return fig
        
        latest_date = df['date'].max()
        df = df[df['date'] == latest_date].groupby('country').agg({
            'confirmed': 'sum',
            'deaths': 'sum',
            'recovered': 'sum'
        }).reset_index().sort_values(chart_type, ascending=True).tail(15)
        
        color_map = {'confirmed': COLORS['confirmed'], 'deaths': COLORS['deaths'], 'recovered': COLORS['recovered']}
        
        fig = px.bar(
            df,
            x=chart_type,
            y="country",
            title=f"<b>TOP 15 COUNTRIES BY {chart_type.upper()}</b>",
            labels={chart_type: "Count", "country": "Country"},
            orientation="h"
        )
        
        fig.update_traces(marker=dict(color=color_map[chart_type]))
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['background'],
            font=dict(color=COLORS['text'], size=12),
            title_font_size=16,
            margin=dict(l=150, r=50, t=60, b=50),
            xaxis=dict(gridcolor='#2A3543'),
            yaxis=dict(gridcolor='#2A3543'),
            hovermode='closest'
        )
        
        return fig
    except Exception as e:
        print(f"Error updating global: {e}")
        fig = go.Figure()
        fig.add_annotation(text=f"Error loading chart")
        return fig

if __name__ == "__main__":
    app.run(debug=False)
