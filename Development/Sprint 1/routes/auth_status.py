import pymysql
from db_config import mysql
from flask import jsonify, request
from app import app, forbidden


@app.route('/auth_status', methods=['POST'])
def auth_status():
    try:
        username = request.form.get("username")
        auth_token = request.form.get("auth_token")
        if username and auth_token and request.method == 'POST':
            # insert record in database
            auth_query = f"SELECT `username`,`auth_token`,`email`,`name`,`mobile_no` from `STRTjSSGl1`.`ohs_user_details` WHERE username = '{username}' OR email = '{username}' OR mobile_no = '{username}'"
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(auth_query)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            if rows[0][1] == auth_token:
                res = jsonify(rows)
                return res
            else:
                res = jsonify("false")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)
