from crypt import methods
from flask import Blueprint
import json

order = Blueprint("order", __name__)


@order.route("/place_order", methods=["GET"])
def place_order():
    try:
        place_ord = open("./mock/place_order_response.json")
        if place_ord:
            return json.load(place_ord)
    except Exception as e:
        print("Excepton:", e)
        return {"message": "Could not load holdings"}, 401
