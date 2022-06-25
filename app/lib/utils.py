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

from lib.error import DataExistError, DataNotFoundError


BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")


def get_logger(name, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(logging.StreamHandler())
    # logger.propagate = False
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
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        )
    )
    return engine
ENGINE = get_engine()


def check_not_none(func):
    def wrapper(*args, **kwargs):
        if any(arg is None for arg in args):
            raise ValueError("Argument is None")
        return func(*args, **kwargs)
    return wrapper


def load_data(date_=None):
    if date_ is None:
        df = pd.read_sql_query(
            sql="select * from weather_log;",
            con=ENGINE
        )
        return df
    else:
        df = pd.read_sql_query(
            sql="select * from weather_log where date=%(date_)s;",
            con=ENGINE,
            params={"date_": date_}
        )
        return df

def is_data_exist(date_):
    df = load_data(date_)
    return not df.empty

@check_not_none
def create_data(date_, value):
    if is_data_exist(date_):
        raise DataExistError("Data already exist")
    ENGINE.execute(
        text("insert into weather_log set date= :date_ , value= :value ;"),
        date_=date_,
        value=value
    )

@check_not_none
def update_data(date_, value):
    if is_data_exist(date_):
        ENGINE.execute(
            text("update weather_log set value= :value where date= :date_ ;"),
            date_=date_,
            value=value
        )
    else:
        raise DataNotFoundError("Data not exist")

@check_not_none
def delete_data(date_):
    ENGINE.execute(
        text("delete from weather_log where date= :date_ ;"),
        date_=date_
    )
