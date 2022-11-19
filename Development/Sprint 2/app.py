from flask import Flask, jsonify, request, render_template
from datetime import datetime
from hashlib import sha256
import random
import ibm_db


app = Flask(__name__, static_url_path='', static_folder='.')
try:
    conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ypd18144;PWD=VWNovCJ0JksVacab",'','')
    print("Connected to database: ", conn)
except:
    print ("Unable to connect to the database")


# CORS section

@app.after_request
def after_request_func(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# end CORS section


# 404 handle


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Your requested url could not be found: ' + request.url,
    }
    res = jsonify(message)
    res.status_code = 404
    return res

# 403 handler


@app.errorhandler(403)
def forbidden(error=None):
    message = {
        'status': 403,
        'message': 'Forbidden',
    }
    res = jsonify(message)
    res.status_code = 403
    return res


# Add your API endpoints here


# @app.route('/')
# def get_endpoint_function():
#     try:
#         res = "<h1 style='position: fixed; top: 50%;  left: 50%; transform: translate(-50%, -50%);'>FLASK API HOME</h1>"
#         return res

#     except Exception as e:
#         print(e)
if __name__ == "__main__":
    app.run(debug=True)



@app.route('/login', methods=['POST'])
def login():
    try:
        email = request.form.get("email")
        paswd = request.form.get("pass")
        h = sha256()
        h.update(b'{paswd}')
        password = h.hexdigest()
        if email and password and request.method == 'POST':
            # insert record in database
            usr_query = f"SELECT COUNT(email) FROM YPD18144.user_details WHERE email='{email}';"
            stmt=ibm_db.exec_immediate(conn,usr_query)
            chk = ibm_db.fetch_assoc(stmt)
            if chk['1'] == 1:
                pass_query = f"SELECT email, password , blood_type, name,verified FROM YPD18144.user_details WHERE email = '{email}'"
                stmt=ibm_db.exec_immediate(conn,pass_query)
                pass_chk = ibm_db.fetch_assoc(stmt)
                
                if password == pass_chk['PASSWORD']:
                    auth = sha256()
                    rand = random.random()
                    auth.update(b'{rand}')
                    auth_token = h.hexdigest()
                    updt_query = f"UPDATE YPD18144.user_details SET auth_token = '{auth_token}' WHERE email = '{email}' ;"
                    print(updt_query)
                    updt_stmt=ibm_db.exec_immediate(conn,updt_query)
                    pass_chk['AUTH_TOKEN']=auth_token
                    res = jsonify(pass_chk)
                    return res
                else:
                    res = jsonify("failed")
                    return res
            else:
                res = jsonify("false")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)

@app.route('/signup', methods=['POST'])
def signup():
    try:
        print("text")
        name = request.form.get("name")
        paswd = request.form.get("pass")
        h = sha256()
        h.update(b'{paswd}')
        password = h.hexdigest()
        email = request.form.get("email")
        mob_no = request.form.get("ph_no")
        type = request.form.get("type")
        plasma = request.form.get("plasma")
        auth = sha256()
        rand = random.random()
        auth.update(b'{rand}')
        auth_token = h.hexdigest()
        if name and password and email and mob_no and type and plasma and auth_token and request.method == 'POST':
            # insert record in database
            query = f"INSERT INTO YPD18144.user_details (email,name,mobile_no,user_type,password,auth_token,verified,blood_type) VALUES ('{email}','{name}',{mob_no},{type},'{password}','{auth_token}',0,'{plasma}');"
            if (ibm_db.exec_immediate(conn,query)):
                res = jsonify(auth_token)
                return res
            else:
                res = jsonify("failed")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


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
