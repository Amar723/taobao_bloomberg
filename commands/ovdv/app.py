import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from commands.ovdv.fetch import get_vol_surface
from commands.ovdv.surface import build_surface
from shared.style import BLOOMBERG_LAYOUT

app = dash.Dash(__name__)

app.layout = html.Div(
    style={"background": "#0a0a0a", "minHeight": "100vh", "fontFamily": "monospace"},
    children=[
        html.Div(
            style={"padding": "12px 20px", "borderBottom": "1px solid #333",
                   "display": "flex", "gap": "20px", "alignItems": "center"},
            children=[
                html.Span("OVDV", style={"color": "#ff8c00", "fontWeight": "bold", "fontSize": "18px"}),
                html.Span("Volatility Surface", style={"color": "#aaa", "fontSize": "14px"}),
                dcc.Input(
                    id="ticker-input", value="AAPL", debounce=True,
                    style={"background": "#1a1a1a", "color": "white",
                           "border": "1px solid #444", "padding": "4px 10px",
                           "fontFamily": "monospace"}
                ),
                html.Button(
                    "GO", id="go-btn",
                    style={"background": "#ff8c00", "color": "black", "border": "none",
                           "padding": "4px 12px", "fontWeight": "bold", "cursor": "pointer"}
                ),
            ]
        ),
        dcc.Loading(
            id="loading",
            type="circle",
            color="#ff8c00",
            children=dcc.Graph(id="vol-surface", style={"height": "88vh"}),
        ),
    ]
)

@app.callback(Output("vol-surface", "figure"), Input("ticker-input", "value"))
def update_surface(ticker_sym: str):
    if not ticker_sym:
        return go.Figure()
    try:
        df, spot = get_vol_surface(ticker_sym.upper())
        moneyness_grid, dte_grid, IV_grid = build_surface(df)

        layout = dict(BLOOMBERG_LAYOUT)
        layout["title"] = dict(
            text=f"{ticker_sym.upper()} — Implied Volatility Surface  |  Spot: {spot:.2f}",
            font=dict(color="#ff8c00", size=14)
        )

        fig = go.Figure(
            data=[go.Surface(
                x=moneyness_grid,
                y=dte_grid,
                z=IV_grid * 100,
                colorscale="RdYlGn_r",
                colorbar=dict(
                    title="IV %",
                    tickfont=dict(color="white"),
                    ticksuffix="%",
                    bgcolor="#1a1a1a",
                    bordercolor="#333",
                ),
                contours=dict(
                    z=dict(show=True, usecolormap=True, highlightcolor="white", project_z=True)
                ),
                lighting=dict(ambient=0.6, diffuse=0.8, roughness=0.5, fresnel=0.2),
            )],
            layout=layout,
        )
        return fig
    except Exception as e:
        # return empty figure with error message if data fetch fails
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="#0a0a0a",
            font=dict(color="white"),
            annotations=[dict(text=f"Error: {str(e)}", x=0.5, y=0.5, showarrow=False)]
        )
        return fig

if __name__ == "__main__":
    app.run(debug=True)