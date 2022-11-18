import pymysql
from db_config import mysql
from flask import jsonify, request
from datetime import datetime
from hashlib import sha256
from app import app, forbidden
import random


@app.route('/post_upload', methods=['POST'])
def post_upload():
    try:
        username = request.form.get("username")
        title = request.form.get("title")
        link = request.form.get("link")
        time = request.form.get("time")
        desc = request.form.get("desc")

        post_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if username and title and link and time and desc and request.method == 'POST':
            # insert record in database
            conn = mysql.connect()
            post = conn.cursor()
            post_query = f"INSERT INTO `STRTjSSGl1`.`ohs_posts` (username,title,description,posted_time,event_time,meet_link) VALUES ('{username}','{title}','{desc}','{post_time}','{time}','{link}');"
            if (post.execute(post_query)):
                conn.commit()
                post.close()
                conn.close()
                res = jsonify("success")
                return res
            else:
                conn.close()
                res = jsonify("failed")
                return res
        else:
            return forbidden()

    except Exception as e:
        print(e)
