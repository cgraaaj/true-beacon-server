from flask import Blueprint
from common.utils import place_ord

order = Blueprint("order", __name__)


@order.route("/place_order", methods=["GET"])
def place_order():
    try:
        return place_ord
    except Exception as e:
        print("Excepton:", e)
        return {"message": "Could not load holdings"}, 401
