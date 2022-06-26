import logging
import json
from pathlib import Path

from dotenv import load_dotenv
import plotly
import plotly.express as px
import plotly.graph_objects as go


BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    return logger

def data2plotly_json(x, y, name=None):
    if name is None:
        fig = go.Figure(data=[
            go.Scatter(x=x, y=y)
        ])
    else:
        fig = go.Figure(data=[
            go.Scatter(x=x, y=y, name=name)
        ])
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json

def img2plotly_json(img):
    fig = px.imshow(img)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0))
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json
