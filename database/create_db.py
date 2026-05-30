import sqlite3

# filename to form database
file = "ev_washington.db"

try:
    conn = sqlite3.connect(file)
    print(f"Database {file} formed")
except Exception as e:
    print(f"Database {file} not formed, error : {e}")
