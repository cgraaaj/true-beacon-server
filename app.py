from crypt import methods
from flask import Flask, request
from flask.helpers import make_response
from flask.json import jsonify
from flask_cors import CORS
from waitress import serve
from flask_jwt_extended import JWTManager
import asyncio
import websockets
import pandas as pd
import requests
import os
import logging
import csv
import time
from datetime import datetime, timedelta, timezone
import csv, sqlite3

# from bson import json_util
from dotenv import load_dotenv

from user.user import user
from portfolio.portfolio import portfolio
from order.order import order
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

app = Flask(__name__)

jwt = JWTManager(app)
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = "super-dooper-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=3)
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(portfolio, url_prefix="/portfolio")
app.register_blueprint(order, url_prefix="/order")

CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


con = sqlite3.connect("./data.sqlite", check_same_thread=False)
cur = con.cursor()
cur.execute("DROP TABLE IF EXISTS historical_prices;")
cur.execute("CREATE TABLE historical_prices (date, price, instrument_name);")
cur.execute(
    "CREATE TABLE IF NOT EXISTS user(pid integer primary key,name text,username text,password text)"
)

with open("historical_prices.csv", "r") as fin:
    # check fin and dr
    dr = csv.DictReader(fin)
    to_db = [(i["date"], i["price"], i["instrument_name"]) for i in dr]

cur.executemany(
    "INSERT INTO historical_prices (date, price, instrument_name) VALUES (?, ?, ?);",
    to_db,
)
con.commit()
con.close()


@app.route("/hi", methods=["GET"])
def hi():
    return "hi"


@app.route("/historical-data", methods=["GET"])
# @jwt_required()
def get_historical_data():
    symbol = "NIFTY 50" if request.args.get("symbol") == "nifty_50" else "NIFTY BANK"
    from_date = request.args.get("from_date")
    to_date = request.args.get("to_date")
    select_query = "SELECT * FROM historical_prices WHERE date between '{}' and '{}' and instrument_name='{}'".format(
        from_date, to_date, symbol
    )
    con = sqlite3.connect("./data.sqlite", check_same_thread=False)
    df = pd.read_sql(select_query, con)
    return df.to_json(orient="records")


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


if __name__ == "__main__":

    LOCATE_PY_DIRECTORY_PATH = os.path.abspath(os.path.dirname(__file__))
    load_dotenv("{}/.env".format(LOCATE_PY_DIRECTORY_PATH))
    port = 5000
    if os.getenv("FLASK_ENV") == "development":
        app.run(port=port, host="0.0.0.0", debug=True)
    else:
        serve(app, host="0.0.0.0", port=port)
