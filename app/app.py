from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
#from dotenv import load_dotenv
import json
import os

app = Flask(__name__)

#load_dotenv()
@app.route('/')
def index():
    # get students from db:
    config = {
        'user': os.environ.get("MYSQL_USER"),
        'password': os.environ.get("MYSQL_PASSWORD"),
        'host': os.environ.get("MYSQL_HOST"),
        'port': '3306',
        'database': os.environ.get("MYSQL_DB")
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM csv_table')
    students = cursor.fetchall()
    print("STUDENTS")
    print(students)
    return render_template('students.html', data=students)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
