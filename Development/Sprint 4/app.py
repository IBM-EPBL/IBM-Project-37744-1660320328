from flask import Flask, jsonify, request, render_template
from datetime import datetime
from hashlib import sha256
import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import ibm_db


app = Flask(__name__, static_url_path='', static_folder='.')
try:
    conn = ibm_db.connect("DATABASE=BLUDB;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ypd18144;PWD=VWNovCJ0JksVacab", '', '')
    print("Connected to database: ", conn)
except:
    print("Unable to connect to the database")


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
            stmt = ibm_db.exec_immediate(conn, usr_query)
            chk = ibm_db.fetch_assoc(stmt)
            if chk['1'] == 1:
                pass_query = f"SELECT email, password , blood_type, name,verified,user_type FROM YPD18144.user_details WHERE email = '{email}'"
                stmt = ibm_db.exec_immediate(conn, pass_query)
                pass_chk = ibm_db.fetch_assoc(stmt)

                if password == pass_chk['PASSWORD']:
                    auth = sha256()
                    rand = random.random()
                    auth.update(b'{rand}')
                    auth_token = h.hexdigest()
                    updt_query = f"UPDATE YPD18144.user_details SET auth_token = '{auth_token}' WHERE email = '{email}' ;"
                    updt_stmt = ibm_db.exec_immediate(conn, updt_query)
                    pass_chk['AUTH_TOKEN'] = auth_token
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
            if (ibm_db.exec_immediate(conn, query)):
                res = jsonify(auth_token)
                return res
            else:
                res = jsonify("failed")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


@app.route('/addplasma', methods=['POST'])
def addplasma():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        mob_no = request.form.get("ph_no")
        hospital = request.form.get("hospital")
        plasma = request.form.get("plasma")
        maps = request.form.get("gmaps")
        if name and email and mob_no and hospital and plasma and maps and request.method == 'POST':
            # insert record in database
            query = f"INSERT INTO YPD18144.request_details (email,name,contact_no,plasma_required,hospital,gmaps_link,status) VALUES ('{email}','{name}',{mob_no},'{plasma}','{hospital}','{maps}',0);"
            print(query)
            if (ibm_db.exec_immediate(conn, query)):
                res = jsonify("success")
                return res
            else:
                res = jsonify("failed")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


@app.route('/userplasma', methods=['POST'])
def userplasma():
    try:
        email = request.form.get("email")
        if email and request.method == 'POST':
            # insert record in database
            query = f"SELECT email,name,contact_no,plasma_required,hospital,gmaps_link,status FROM YPD18144.request_details  WHERE email= '{email}';"
            stmt = ibm_db.exec_immediate(conn, query)
            chk = ibm_db.fetch_assoc(stmt)
            data = list()
            while chk != False:
                data.append(chk)
                chk = ibm_db.fetch_assoc(stmt)
            res = jsonify(data)
            return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


@app.route('/plasma', methods=['POST'])
def plasma():
    try:
        email = request.form.get("email")
        if email and request.method == 'POST':
            # insert record in database
            query = "SELECT email,name,contact_no,plasma_required,hospital,gmaps_link,status FROM YPD18144.request_details;"
            stmt = ibm_db.exec_immediate(conn, query)
            chk = ibm_db.fetch_assoc(stmt)
            data = list()
            while chk != False:
                data.append(chk)
                chk = ibm_db.fetch_assoc(stmt)
            res = jsonify(data)
            return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


@app.route('/user', methods=['POST'])
def user():
    try:
        email = request.form.get("email")
        if email and request.method == 'POST':
            # insert record in database
            query = "SELECT email,name,user_type FROM YPD18144.user_details WHERE verified=0;"
            stmt = ibm_db.exec_immediate(conn, query)
            chk = ibm_db.fetch_assoc(stmt)
            data = list()
            while chk != False:
                data.append(chk)
                chk = ibm_db.fetch_assoc(stmt)
            res = jsonify(data)
            return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


@app.route('/verify', methods=['POST'])
def verify():
    try:
        email = request.form.get("email")
        if email and request.method == 'POST':
            # insert record in database
            updt_query = f"UPDATE YPD18144.user_details SET verified = 1 WHERE email = '{email}' ;"
            if (ibm_db.exec_immediate(conn, updt_query)):
                message = Mail(from_email='hareeshkumaar.23cs@licet.ac.in', to_emails=email,
                               subject='Your Account is verified! Huraah Login')
                try:
                    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                    response = sg.send(message)
                except Exception as e:
                    print(e.message)
                res = jsonify("success")
                return res
            else:
                res = jsonify("failed")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


@app.route('/drive', methods=['POST'])
def drive():
    try:
        email = request.form.get("email")
        if email and request.method == 'POST':
            # insert record in database
            query = f"SELECT email,donation_drive_name,contact_no,venue,gmaps_link,date FROM YPD18144.donation_details;"
            stmt = ibm_db.exec_immediate(conn, query)
            chk = ibm_db.fetch_assoc(stmt)
            data = list()
            while chk != False:
                data.append(chk)
                chk = ibm_db.fetch_assoc(stmt)
            res = jsonify(data)
            return res
        else:
            return forbidden()

    except Exception as e:
        print(e)


@app.route('/adddrive', methods=['POST'])
def adddrive():
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        mob_no = request.form.get("ph_no")
        venue = request.form.get("venue")
        date = request.form.get("date")
        maps = request.form.get("gmaps")
        if name and email and mob_no and venue and date and maps and request.method == 'POST':
            # insert record in database
            query = f"INSERT INTO YPD18144.donation_details (email,donation_drive_name,contact_no,date,venue,gmaps_link) VALUES ('{email}','{name}',{mob_no},'{date}','{venue}','{maps}');"
            if (ibm_db.exec_immediate(conn, query)):
                res = jsonify("success")
                return res
            else:
                res = jsonify("failed")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)
