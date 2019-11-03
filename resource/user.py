import pymysql
from flask_restful import Resource, reqparse
from flask import jsonify

# 設定參數白名單
parser = reqparse.RequestParser()
parser.add_argument("name")
parser.add_argument("gender")
parser.add_argument("birth")
parser.add_argument("note")

# 設定回傳的統一格式
response = {"code": 200, "msg": "success"}


class Users(Resource):
    # 初始化資料庫設定
    def db_init(self):
        db = pymysql.connect("localhost", "root", "password", "flask_demo")
        cursor = db.cursor(pymysql.cursors.DictCursor)
        return db, cursor

    # 獲取所有 users 此資源的資料
    def get(self):

        # 執行 SQL 語句
        db, cursor = self.db_init()
        sql = """
            select * from flask_demo.users
        """
        cursor.execute(sql)
        db.commit()
        users = cursor.fetchall()
        db.close()

        # 將撈取後的資料設定進統一格式中
        response["code"] = 200
        response["msg"] = "success"
        response["data"] = users
        return jsonify(response)

    # 新增一筆 user
    def post(self):
        db, cursor = self.db_init()
        arg = parser.parse_args()

        # 檢查，如果使用者傳來的參數沒有 name，就回傳錯誤訊息
        if arg["name"] == None:
            response["code"] = 400
            response["msg"] = "name is missing"
            return jsonify(response)

        # 將參數轉化為資料庫的欄位格式，製作一個 dictionary
        user = {
            "name": arg["name"],
            "gender": arg["gender"],
            "birth": arg["birth"] or "1900-01-01",
            "note": arg["note"],
        }

        # 執行 SQL 語句
        sql = """
        Insert into flask_demo.users (name, gender, birth, note)
        Values('{}', '{}', '{}', '{}')
        """.format(
            user["name"], user["gender"], user["birth"], user["note"]
        )
        result = cursor.execute(sql)
        db.commit()
        db.close()

        # 根據 SQL 執行結果，判斷要回傳啥
        if result == 0:
            response["msg"] = "error"
            response["code"] = "500"
        else:
            response["msg"] = "success"
            response["code"] = "200"

        return jsonify(response)

