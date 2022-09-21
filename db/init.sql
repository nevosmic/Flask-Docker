create database attendance_db;
use attendance_db;


CREATE TABLE csv_table (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Meeting_Name VARCHAR(200) NOT NULL,
  Meeting_Start_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Meeting_End_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Name VARCHAR(200) NOT NULL,
  Attendee_Email VARCHAR(200) NOT NULL,
  Join_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Leave_Time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Attendance_Duration VARCHAR(45) NOT NULL,
  Connection_Type VARCHAR(200) NOT NULL

);

INSERT INTO csv_table
  (Meeting_Name, Meeting_Start_Time, Meeting_End_Time, Name, Attendee_Email, Join_Time, Leave_Time, Attendance_Duration, Connection_Type)
VALUES
  ("Jeff Macloues Personal Room", "2022-08-03 15:27:33", "2022-08-03 19:44:16", "Almog Menashe", "almo99walla@gmail.com", "2022-08-03 16:01:27", "2022-08-03 19:44:21", "223", "Desktop app");


