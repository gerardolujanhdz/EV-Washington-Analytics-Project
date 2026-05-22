# Imports
import sqlite3

# Connecting to the ev_washington database
connection = sqlite3.connect("../database/ev_washington.db")

# Creating a cursor object to execute sql queries on a db table
cursor = connection.cursor()

# Opening populating.sql file and saving it as a file object
with open("../sql/03_populating.sql", "r") as sql_file:
    sql_script = sql_file.read()

# Executing sql script populating.sql
cursor.executescript(sql_script)
print("Populating script executed")

# Commiting Change
connection.commit()
print("Committed!")
