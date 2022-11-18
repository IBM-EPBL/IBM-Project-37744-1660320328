import pymysql
from db_config import mysql
from flask import jsonify, request
from datetime import date, datetime
from hashlib import sha256
from app import app, forbidden
import random


@app.route('/username_check', methods=['POST'])
def username_check():
    try:
        username = request.form.get("username")
        if username and request.method == 'POST':
            # insert record in database
            conn = mysql.connect()
            usr_chk = conn.cursor()
            usr_query = f"SELECT EXISTS(SELECT username FROM `STRTjSSGl1`.`ohs_user_details` WHERE username = '{username}');"
            usr_chk.execute(usr_query)
            chk = usr_chk.fetchall()
            usr_chk.close()
            conn.close()
            if chk[0][0] == 1:
                res = jsonify("failed")
                return res
            else:
                res = jsonify("success")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)
