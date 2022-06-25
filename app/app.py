import os
import json
from this import d

import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go
from flask import Flask, request, render_template, jsonify, redirect
from sqlalchemy.ext.declarative import declarative_base

from lib import utils

logger = utils.get_logger(__name__)

logger.info("starting app")
app = Flask(__name__, static_folder='static')
app.config["TEMPLATES_AUTO_RELOAD"] = True
logger.info("app started")


@app.route('/', methods=["GET"])
def transition():
    df = utils.load_data()
    df = df.sort_values(by="date").reset_index(drop=True)
    fig = go.Figure(data=[
        go.Scatter(x=df["date"], y=df["value"], name="sin"),
    ])
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "transition.html",
        graph_json=graph_json,
        df=df
    )

@app.route('/update', methods=["GET"])
def update():
    date_ = request.args.get("date")
    value = request.args.get("value")

    utils.update_data(date_, value)
    return redirect("/")

@app.route('/delete/<id>', methods=["GET"])
def delete(id):
    utils.delete_data(id)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
