import os
import datetime
import traceback
from typing import Optional

import numpy as np
from PIL import Image
from flask import Flask, request, render_template, redirect, url_for, abort, jsonify, escape
from werkzeug.utils import secure_filename
from pydantic import validate_arguments

from lib import utils
from lib.storage import cloud_sql, gcs, gcs_wrapper
from lib.error import DataExistError, DataNotFoundError

logger = utils.get_logger(__name__)

logger.info("")
logger.info("starting app")
app = Flask(__name__, static_folder='static')
app.config["TEMPLATES_AUTO_RELOAD"] = True
logger = app.logger
logger.setLevel("DEBUG")
logger.info("app started")

@app.before_request
def app_before_request1():
    if request.args:
        logger.info(("request.args", request.args))
    if request.form:
        logger.info(("request.form", request.form))
    if request.files:
        logger.info(("request.files", request.files))


def redirect_top(message):
    return redirect(url_for("transition", message=message))

@app.errorhandler(Exception)
def error_except(e):
    logger.warning(("error", e))
    logger.warning(traceback.format_exc())
    abort(500, str(e))

@app.route('/', methods=["GET"])
@app.route('/transition', methods=["GET"])
def transition():
    message = request.args.get("message", "")
    message = escape(message)
    df = cloud_sql.read()
    df = df.sort_values(by="date").reset_index(drop=True)
    graph_json = utils.data2plotly_json(df["date"], df["value"])

    return render_template(
        "transition.html",
        graph_json=graph_json,
        df=df,
        message=message
    )

@app.route('/create', methods=["POST"])
def create():
    try:
        cloud_sql.create(request.form["date"], request.form["value"])
        return redirect("/")

    except DataExistError as e:
        logger.error(e)
        return redirect_top("すでにデータが存在しているため作成できませんでした")

@app.route('/detail/<date_>', methods=["GET"])
@validate_arguments
def detail(date_: datetime.date):
    df = cloud_sql.read(date_)
    if len(df) == 0:
        logger.info(("df", df))
        return redirect_top("データが存在しません")

    elif len(df) > 1:
        logger.info(("df", df))
        return redirect_top("データが複数存在しているため詳細ページを表示できません")

    file_names, imgs = gcs_wrapper.read_imgs(date_)
    graph_jsons = [
        utils.img2plotly_json(img) for img in imgs
    ]

    return render_template(
        "detail.html",
        row=df.iloc[0],
        file_names=file_names,
        graph_jsons=graph_jsons
    )

@app.route('/update/<date_>', methods=["GET"])
@validate_arguments
def update(date_: datetime.date):
    try:
        cloud_sql.update(date_, request.args["value"])
        return redirect(f"/detail/{date_}")
    except DataNotFoundError as e:
        logger.error(e)
        return redirect_top("データが存在しないため更新できませんでした")

@app.route('/delete/<date_>', methods=["GET"])
@validate_arguments
def delete(date_: datetime.date):
    cloud_sql.delete(date_)
    return redirect("/")

@app.route('/upload/<date_>', methods=["POST"])
@validate_arguments
def upload_img(date_: datetime.date):
    files = request.files.getlist('imgs')
    for file in files:
        file_name = secure_filename(file.filename)
        logger.info(("file_name", file_name))
        img_pil = Image.open(file)

        try:
            gcs_wrapper.save_img(img_pil, os.path.join(str(date_), file_name))
        except FileExistsError as e:
            logger.error(e)
            return redirect_top("すでにファイルが存在しているためアップロードできませんでした")

    return redirect(f"/detail/{date_}")

@app.route('/delete_img/<date_>/<file_name>', methods=["GET"])
@validate_arguments
def delete_img(date_: datetime.date, file_name: str):
    gcs.delete(f"{date_}/{file_name}")
    return redirect(f"/detail/{date_}")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
