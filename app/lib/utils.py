import os
import json
import logging
from pathlib import Path

from dotenv import load_dotenv
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

from lib import utils


BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    logger.propagate = False
    return logger


def get_engine():
    db_user = os.environ["DB_USER"]
    db_pass = os.environ["DB_PASS"]
    db_name = os.environ["DB_NAME"]
    db_host = os.environ["DB_HOST"]
    db_port = os.environ["DB_PORT"]


    engine = sqlalchemy.create_engine(
        # Equivalent URL:
        # mysql+pymysql://<db_user>:<db_pass>@<db_host>:<db_port>/<db_name>
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,  # e.g. "my-database-user"
            password=db_pass,  # e.g. "my-database-password"
            host=db_host,  # e.g. "127.0.0.1"
            port=db_port,  # e.g. 3306
            database=db_name,  # e.g. "my-database-name"
        )
    )
    return engine
ENGINE = get_engine()

def create_data(date_, value):
    ENGINE.execute(
        text("insert into weather_log set date= :date_ , value= :value ;"),
        date_=date_,
        value=value
    )

def update_data(date_, value):
    # 同じ日付のデータがある場合は、そのデータを更新する
    # ない場合は、新しくデータを追加する
    df = load_data()
    if df.loc[df["date"] == date_].empty:
        create_data(date_, value)
    else:
        ENGINE.execute(
            text("update weather_log set value= :value where date= :date_ ;"),
            date_=date_,
            value=value
        )

def load_data():
    df = pd.read_sql_query(
        sql="select * from weather_log;",
        con=ENGINE
    )
    return df

def delete_data(id):
    ENGINE.execute(
        text("delete from weather_log where id= :id ;"),
        id=id
    )
