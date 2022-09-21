create database attendance_db;
use attendance_db;

CREATE TABLE csv_table (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  Name VARCHAR(10) NOT NULL,
  Meeting_start_time TIMESTAMP NOT NULL
);

INSERT INTO csv_table
  (Name, Meeting_start_time)
VALUES
  ("Michal", "2022-08-18 15:53:47"),
  ("Keren", "2022-08-18 15:53:47");
