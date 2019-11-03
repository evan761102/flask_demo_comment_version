import flask
from flask import request, jsonify
import pymysql

from resource.user import Users
from flask_restful import Api, Resource


app = flask.Flask(__name__)
app.config["DEBUG"] = True

# 設定 users 的路由表
api = Api(app)
api.add_resource(Users, "/users")


@app.route("/", methods=["GET"])
def home():
    return "hello world"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
