from crypt import methods
from unittest import expectedFailure
from flask import Blueprint
import json

portfolio = Blueprint("portfolio", __name__)


@portfolio.route("/holdings", methods=["GET"])
def get_holdings():
    try:
        holdings = open("./mock/holdings.json")
        if holdings:
            return json.load(holdings)
    except Exception as e:
        print("Excepton:", e)
        return {"message": "Could not load holdings"}, 401
