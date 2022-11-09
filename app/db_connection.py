import mysql.connector
import os


def get_connection_to_mysql():
    config = {
        'user': os.environ.get("MYSQL_USER"),
        'password': os.environ.get("MYSQL_PASSWORD"),
        'host': os.environ.get("MYSQL_HOST"),
        'port': '3306',
        'database': os.environ.get("MYSQL_DB")
    }
    connection = mysql.connector.connect(**config)
    connection = init_database(connection)
    cursor = connection.cursor()
    cursor.execute("select database();")
    db = cursor.fetchone()

    if db:
        print("You're connected to database: ", db)
    else:
        print('Not connected.')
        print('db fetchone(): ', db)
    return connection


def init_database(connection):
    """
        Create database if not exist.
        :param connection: mysql connection object (created in db_connection)
    """
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS attendance_db")
    print("attendance_db database has been created!")
    cursor.execute("USE attendance_db;")
    connection.commit()
    return connection

def init_table(connection):
    """
        Create a new csv table.
        :param connection: mysql connection object (created in db_connection)
    """

    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS csv_table;")
    cursor.execute(
        "CREATE TABLE csv_table (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,File_Name VARCHAR(200) NOT NULL,"
        " Meeting_Name VARCHAR(200) NOT NULL, Meeting_Start_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
        "Meeting_End_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, Name VARCHAR(200) NOT NULL, "
        "Attendee_Email VARCHAR(200) NOT NULL, Join_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
        "Leave_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, Attendance_Duration VARCHAR(45) NOT NULL,"
        "Connection_Type VARCHAR(200) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;")
    connection.commit()
    return connection
