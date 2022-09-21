from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import json
import os

app = Flask(__name__)
print("PWDDDDDDDDDD")
print(os.getcwd())
def csv_table():
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'attendance_db'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM csv_table')
    
    results = [{id:Meeting_start_time} for (id, Meeting_start_time) in cursor]
    cursor.close()
    connection.close()

    return results


@app.route('/')
def index() -> str:
    # get students from db:
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'db',
        'port': '3306',
        'database': 'attendance_db'
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
