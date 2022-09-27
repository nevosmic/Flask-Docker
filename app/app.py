from flask import Flask, render_template, request, redirect, url_for

from db_connection import *
from sftp_connection import *
from calculate_attendance import *
import csv


app = Flask(__name__)


def insert_csv_to_db(path_to_csv, connection):
    """
        Insert csv rows into 'csv_table' in database.
        :param path_to_csv: a path to one of the csv file
        :param connection: mysql connection object (created in db_connection)
    """
    with open(path_to_csv, newline='', encoding='utf-16') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        # skip header
        next(spamreader, None)
        for row in spamreader:
            Meeting_Name, Meeting_Start_Time_str, Meeting_End_Time_str, Name, Attendee_Email, Join_Time_str, Leave_Time_str, Attendance_Duration_str, Connection_Type = row
            Meeting_Start_Time, Meeting_End_Time, Join_Time, Leave_Time, Attendance_Duration = parse_times(
                Meeting_Start_Time_str, Meeting_End_Time_str, Join_Time_str, Leave_Time_str, Attendance_Duration_str)
            sql = "INSERT IGNORE INTO csv_table (`Meeting_Name`,`Meeting_Start_Time`,`Meeting_End_Time`, `Name`,`Attendee_Email`,`Join_Time`, `Leave_Time`, `Attendance_Duration`, `Connection_Type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (Meeting_Name, Meeting_Start_Time, Meeting_End_Time, Name, Attendee_Email, Join_Time, Leave_Time, Attendance_Duration, Connection_Type)

            connection.cursor().execute(sql, val)
            connection.commit()


def parse_times(start_, end_, join_, leave_, duration_):
    """
        Removing unnecessary characters like '=' or '"'
    """
    start = start_[2:-1]
    end = end_[2:-1]
    join = join_[2:-1]
    leave = leave_[2:-1]
    duration = duration_.split(' ')[0]
    return start, end, join, leave, duration


@app.route('/')
def index():
    students_object, header = create_students_display_list_from_csv()
    return render_template('students.html', headings=header, data=students_object)


def csv_files_handler(connection):
    """
        Get files via sftp connection and insert them to csv_table in database using insert_csv_to_db()
        :param connection: mysql connection object (created in db_connection
    """
    csv_files = sftp_get_files()
    print("CSV FILES:")
    print(csv_files)

    for file_name in csv_files:
        file_path = 'static/files/{}'.format(file_name)
        insert_csv_to_db(file_path, connection)
    print("Done !")


def create_students_list_csv(connection):
    """
        Get students Webex data from db and calculate attendance statistics
        :param connection: mysql connection object (created in db_connection)
        Outputs a csv file
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM csv_table')
    students = cursor.fetchall()
    # create a csv file with participation statistics
    calculate_attendance(students)


def create_students_display_list_from_csv():
    """
            Get attendance statistics from csv file and turn it into an object
            which will be displayed on the browser.
            :return students: an object with students statistics
            :return header
    """
    csvfile = open('attendance_output.csv', newline='')
    # make a new variable - c - for Python's DictReader object
    c = csv.DictReader(csvfile)
    # read from DictReader object using the column headings from the CSV as the dict keys
    # header
    students = []
    header = ('Name', 'Average participation', 'Total time (minutes)', 'Email name')
    for row in c:
        students.append(( row['names'], row['average'], row['total time'], row['']))
    return students, header


""" DOTO: 1)log file """
if __name__ == '__main__':
    connection = get_connection_to_mysql()
    csv_files_handler(connection)
    create_students_list_csv(connection)

    app.run(host='0.0.0.0', debug=True)

