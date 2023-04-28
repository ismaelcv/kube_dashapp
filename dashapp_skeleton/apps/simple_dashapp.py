import os
from typing import Tuple

import dash
import plotly.graph_objects as go
from dash import dcc, html

es = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=es)
xs = list(range(30))
ys = [10000 * 1.07**i for i in xs]
fig = go.Figure(data=go.Scatter(x=xs, y=ys))
fig.update_layout(xaxis_title="Years", yaxis_title="$")
app.layout = html.Div(
    children=[
        html.Br(),
        html.H2(children="And now look...a random graph"),
        dcc.Graph(figure=fig),
    ]
)


@app.server.route("/health")
def health() -> Tuple[dict, int]:
    """
    Function call to check if the app is running
    """

    return ({"status": "ok"}, 200)


server = app.server

if __name__ == "__main__":
    debug = os.environ.get("DEBUG", "false") == "true"
    app.run_server(debug=debug, port="8094")
