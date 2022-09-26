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
    cursor = connection.cursor()
    cursor.execute("select database();")
    db = cursor.fetchone()

    if db:
        print("You're connected to database: ", db)
    else:
        print('Not connected.')
    return connection
