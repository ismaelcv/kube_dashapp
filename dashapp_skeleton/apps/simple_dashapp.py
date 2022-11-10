import os
from typing import Tuple

import boto3
import dash
import plotly.graph_objects as go
from dash import dcc, html

s3_resource = boto3.resource("s3")
BUCKET_NAME = "lambda-github-actions-test-bucket"


bucket = s3_resource.Bucket(BUCKET_NAME)

files = [file.key for file in bucket.objects.filter(Prefix="dummy_files/") if file.key.endswith(".parquet")]


es = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=es)
xs = list(range(30))
ys = [10000 * 1.07**i for i in xs]
fig = go.Figure(data=go.Scatter(x=xs, y=ys))
fig.update_layout(xaxis_title="Years", yaxis_title="$")
app.layout = html.Div(
    children=[
        html.H1(children=f"How many files are in {BUCKET_NAME}"),
        html.H2(children=f"There are {len(files)} files in your s3 bucket"),
        html.H3(children=str(files)),
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
