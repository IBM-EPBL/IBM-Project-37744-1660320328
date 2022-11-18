import pymysql
from db_config import mysql
from flask import jsonify, request
from datetime import datetime
from hashlib import sha256
from app import app, forbidden
import random


@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form.get("username")
        name = request.form.get("name")
        paswd = request.form.get("pass")
        h = sha256()
        h.update(b'{paswd}')
        password = h.hexdigest()
        email = request.form.get("email")
        mob_no = request.form.get("ph_no")
        auth = sha256()
        rand = random.random()
        auth.update(b'{rand}')
        auth_token = h.hexdigest()
        last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        acct_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if username and password and acct_created and last_login and email and mob_no and auth_token and name and request.method == 'POST':
            # insert record in database
            conn = mysql.connect()
            updt_query = f"INSERT INTO `STRTjSSGl1`.`ohs_user_details` (username,name,email,mobile_no,auth_token,password,account_created,last_login) VALUES ('{username}','{name}','{email}',{mob_no},'{auth_token}','{password}','{acct_created}','{last_login}');"
            updt = conn.cursor()
            if (updt.execute(updt_query)):
                conn.commit()
                updt.close()
                conn.close()
                res = jsonify(auth_token)
                return res
            else:
                conn.close()
                res = jsonify("failed")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)
