import pymysql
from db_config import mysql
from flask import jsonify, request
from datetime import datetime
from hashlib import sha256
from app import app, forbidden
import random


@app.route('/post_getinfo', methods=['POST'])
def post_getinfo():
    try:
        username = request.form.get("username")
        paswd = request.form.get("pass")
        h = sha256()
        h.update(b'{paswd}')
        password = h.hexdigest()
        last_login = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if username and password and request.method == 'POST':
            # insert record in database
            conn = mysql.connect()
            usr_chk = conn.cursor()
            usr_query = f"SELECT EXISTS(SELECT username FROM `STRTjSSGl1`.`ohs_user_details` WHERE username = '{username}' or email='{username}' or mobile_no='{username}');"
            usr_chk.execute(usr_query)
            chk = usr_chk.fetchall()
            usr_chk.close()
            if chk[0][0] == 1:
                pass_query = f"SELECT username, password FROM `STRTjSSGl1`.`ohs_user_details` WHERE username = '{username}' or email='{username}' or mobile_no='{username}'"
                pass_csr = conn.cursor()
                pass_csr.execute(pass_query)
                pass_chk = pass_csr.fetchall()
                pass_csr.close()
                if password == pass_chk[0][1]:
                    user = pass_chk[0][0]
                    auth = sha256()
                    rand = random.random()
                    auth.update(b'{rand}')
                    auth_token = h.hexdigest()
                    updt_query = f"UPDATE `STRTjSSGl1`.`ohs_user_details` SET `auth_token` = '{auth_token}' , `last_login`='{last_login}' WHERE (`username` = '{user}');"
                    updt = conn.cursor()
                    updt.execute(updt_query)
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
                conn.close()
                res = jsonify("false")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)
