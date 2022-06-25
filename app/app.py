import os
import json
import re
from this import d

import numpy as np
import pandas as pd
from PIL import Image
import plotly
import plotly.graph_objects as go
from flask import Flask, request, render_template, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

from lib import utils
from lib.error import DataExistError, DataNotFoundError

logger = utils.get_logger(__name__)

logger.info("")
logger.info("starting app")
app = Flask(__name__, static_folder='static')
app.config["TEMPLATES_AUTO_RELOAD"] = True
logger.info("app started")

@app.before_request
def app_before_request1():
    logger.info("")
    logger.info(("request.path", request.path))
    logger.info(("request.method", request.method))
    if request.args:
        logger.info(("request.args", request.args))
    if request.form:
        logger.info(("request.form", request.form))
    if request.files:
        logger.info(("request.files", request.files))


@app.route('/', methods=["GET"])
@app.route('/transition', methods=["GET"])
def transition():
    message = request.args.get("message", None)
    logger.info(("message", message))

    df = utils.load_data()
    df = df.sort_values(by="date").reset_index(drop=True)
    fig = go.Figure(data=[
        go.Scatter(x=df["date"], y=df["value"], name="sin"),
    ])
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template(
        "transition.html",
        graph_json=graph_json,
        df=df,
        message=message
    )

@app.route('/create', methods=["POST"])
def create():
    date_ = request.form.get("date")
    value = request.form.get("value")

    try:
        utils.create_data(date_, value)
        return redirect("/")

    except DataExistError as e:
        logger.error(e)
        return redirect(
            url_for(
                "transition",
                message="すでにデータが存在しているため作成できませんでした"
            )
        )

@app.route('/detail/<date_>', methods=["GET"])
def detail(date_):
    df = utils.load_data(date_)
    if len(df) == 0:
        logger.info(("df", df))
        return redirect(
            url_for(
                "transition",
                message="データが存在しません"
            )
        )
    elif len(df) > 1:
        logger.info(("df", df))
        return redirect(
            url_for(
                "transition",
                message="データが複数存在しているため詳細ページを表示できません"
            )
        )

    # imgs = utils.load_imgs(date_)
    figs = [
        go.Figure(data=[
            go.Scatter(x=df["date"], y=df["value"], name="sin"),
        ]) for i in range(3)
    ]
    imgs = [
        json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        for fig in figs
    ]

    return render_template(
        "detail.html",
        row=df.iloc[0],
        imgs=imgs
    )

@app.route('/update/<date_>', methods=["GET"])
def update(date_):
    value = request.args.get("value")

    try:
        utils.update_data(date_, value)
        return redirect("/")
    except DataNotFoundError as e:
        logger.error(e)
        return redirect(
            url_for(
                "transition",
                message="データが存在しないため更新できませんでした"
            )
        )

@app.route('/delete/<date_>', methods=["GET"])
def delete(date_):
    utils.delete_data(date_)
    return redirect("/")

def save(*args):
    pass

@app.route('/upload', methods=["POST"])
def upload():
    files = request.files.getlist('imgs')
    for file in files:
        file_name = secure_filename(file.filename)
        stream = file.stream
        img = np.frombuffer(stream.read(), dtype=np.uint8)
        logger.info(("file_name", file_name))
        logger.info(("img", type(img)))
        img_pil = Image.fromarray(img)
        save(img_pil, file_name)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
