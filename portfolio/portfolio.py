from flask import Blueprint
from common.utils import holdings

portfolio = Blueprint("portfolio", __name__)


@portfolio.route("/holdings", methods=["GET"])
def get_holdings():
    try:
        return holdings
    except Exception as e:
        print("Excepton:", e)
        return {"message": "Could not load holdings"}, 401
