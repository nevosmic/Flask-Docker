from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
#from dotenv import load_dotenv
from db_connection import *
from sftp_connection import *
import json
import os

app = Flask(__name__)
sftp_get_files()
connection, cursor = get_connection_to_mysql()
#load_dotenv()
@app.route('/')
def index():
    # get students from db:
    
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM csv_table')
    students = cursor.fetchall()
    print("STUDENTS")
    print(students)
    return render_template('students.html', data=students)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
