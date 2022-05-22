from crypt import methods
import json
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt
import sqlite3

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies
from common.utils import profile as prof
from common.getdb import con


user = Blueprint("user", __name__)


# @user.route("/getUser/<public_id>", methods=["GET"])
# @jwt_required()
# def get_one_user(public_id):
#     current_user = get_jwt()
#     if not current_user["is_admin"]:
#         return jsonify({"message": "You are not authorized to perform this"})
#     user = collection.find_one(
#         {"public_id": public_id},
#         {
#             "_id": 0,
#             "public_id": 1,
#             "username": 1,
#             "password": 1,
#             "email": 1,
#             "is_admin": 1,
#         },
#     )

#     if not user:
#         return jsonify({"message": "No user found!"})

#     return jsonify({"user": user})


@user.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    cur = con.cursor()
    if not data or not data["username"] or not data["password"]:
        return jsonify({"message": "could not register user"}), 400
    hased_pass = generate_password_hash(data["password"], method="sha256")
    try:
        cur.execute(
            "INSERT INTO user(name,username,password)values(?,?,?)",
            (data["name"], data["username"], hased_pass),
        )
        con.commit()
        return jsonify({"message": f"New user, {data['username']} has been created"})
    except:
        print("could not register user in db")
        return jsonify({"message": "could not register user"}), 400


@user.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    cur = con.cursor()
    if not data or not data["username"] or not data["password"]:
        return {"message": "Could not verify invalid username/password"}, 401
    try:
        cur.execute("SELECT * FROM user WHERE username = ?", [data["username"]])
        user = cur.fetchone()
        if not user:
            return {"message": "User not Found"}, 404
        if check_password_hash(user[3], data["password"]):
            access_token = create_access_token(
                identity=data["username"],
                additional_claims={"username": data["username"]},
            )
            response = jsonify(
                {"msg": "login successful", "access_token": access_token}
            )
            set_access_cookies(response, access_token)
            return response
    except Exception as e:
        print("could not verify, exception:", e)
        return {"message": "Could not verify"}, 401

@user.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@user.route("/profile", methods=["GET"])
def profile():
    try:
        return prof
    except Exception as e:
        print("exception:", e)
        return {"message": "Could not load profile"}, 401


# @user.route("/updateUser/<user_id>", methods=["PUT"])
# @jwt_required()
# def update_user():
#     current_user = get_jwt()
#     if not current_user["is_admin"]:
#         return jsonify({"message": "You are not authorized to perform this"})
#     return ""


# @user.route("/deleteUser/<public_id>", methods=["DELETE"])
# @jwt_required()
# def delete_user(public_id):
#     current_user = get_jwt()
#     if not current_user["is_admin"]:
#         return jsonify({"message": "You are not authorized to perform this"})
#     user = collection.find_one(
#         {"public_id": public_id},
#         {
#             "_id": 0,
#             "public_id": 1,
#             "username": 1,
#             "password": 1,
#             "email": 1,
#             "is_admin": 1,
#         },
#     )

#     if not user:
#         return jsonify({"message": "No user found!"})
#     collection.delete_one({"username": public_id})
#     return f"User {public_id} deleted"
