from typing import List, Dict
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
# from dotenv import load_dotenv
from db_connection import *
from sftp_connection import *
from calculate_attendance import *
import json
import os
import csv


app = Flask(__name__)

csv_files = sftp_get_files()


# load_dotenv()
def insert_to_db():
    connection = get_connection_to_mysql()
    
    print("AFTER CONNECT")
    connection.cursor().execute('SELECT * FROM csv_table')
    students = cursor.fetchall()
    print("STUDENTS")
    print(students)
    
    sql = "INSERT INTO csv_table (`Meeting_Name`,`Meeting_Start_Time`,`Meeting_End_Time`, `Name`,`Attendee_Email`,`Join_Time`, `Leave_Time`, `Attendance_Duration`, `Connection_Type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = ("Jeff Macloues Personal Room", "2022-08-03 15:27:33", "2022-08-03 19:44:16", "MIMI", "MIMI@gmail.com",
           "2022-08-03 16:01:27", "2022-08-03 19:44:21", "223", "Desktop app")
    connection.cursor().execute(sql, val)
    connection.commit()


def insert_csv_to_db(path_to_csv):
    connection = get_connection_to_mysql()
    with open(path_to_csv, newline='', encoding='utf-16') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        next(spamreader, None)
        print("BEFORE INSERT")
        for row in spamreader:
            Meeting_Name, Meeting_Start_Time_str, Meeting_End_Time_str, Name, Attendee_Email, Join_Time_str, Leave_Time_str, Attendance_Duration_str, Connection_Type = row
            Meeting_Start_Time, Meeting_End_Time, Join_Time, Leave_Time, Attendance_Duration = parse_times(
                Meeting_Start_Time_str, Meeting_End_Time_str, Join_Time_str, Leave_Time_str, Attendance_Duration_str)
            sql = "INSERT INTO csv_table (`Meeting_Name`,`Meeting_Start_Time`,`Meeting_End_Time`, `Name`,`Attendee_Email`,`Join_Time`, `Leave_Time`, `Attendance_Duration`, `Connection_Type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (Meeting_Name, Meeting_Start_Time, Meeting_End_Time, Name, Attendee_Email, Join_Time, Leave_Time, Attendance_Duration, Connection_Type)
            # sql = "INSERT INTO `csv_table` (`Meeting_Name`,`Meeting_Start_Time`,`Meeting_End_Time`, `Name`,`Attendee_Email`,`Join_Time`, `Leave_Time`, `Attendance_Duration`, `Connection_Type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

            connection.cursor().execute(sql, val)
            connection.commit()


def parse_times(start_, end_, join_, leave_, duration_):
    start = start_[2:-1]
    end = end_[2:-1]
    join = join_[2:-1]
    leave = leave_[2:-1]
    duration = duration_.split(' ')[0]
    return start, end, join, leave, duration


@app.route('/')
def index():
    # get students from db:
    # connection, cursor = get_connection_to_mysql()
    connection = get_connection_to_mysql()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM csv_table')
    students = cursor.fetchall()
    calculate_attendance(students)
    return render_template('students.html', data=students)


if __name__ == '__main__':

    print("CSV FILES:")
    print(csv_files)
    # insert_to_db()

    for file_name in csv_files:
        file_path = 'static/files/{}'.format(file_name)
        insert_csv_to_db(file_path)
    print("Done !")

    app.run(host='0.0.0.0', debug=True)
