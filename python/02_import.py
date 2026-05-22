# Pipeline for importing csv file


import csv
import sqlite3

# Creating an SQLite database file from Python
try:
    with sqlite3.connect("../database/ev_washington.db") as conn:
        print(
            f"Opened SQLite database with version {sqlite3.sqlite_version} successfully."
        )

except sqlite3.OperationalError as e:
    print("Failed to open database:", e)


# Connecting to the ev_washington database
connection = sqlite3.connect("../database/ev_washington.db")

# Creating a cursor object to execute sql queries on a db table
cursor = connection.cursor()

# Running schema.sql
with open("../sql/01_schema.sql", "r") as sql_file:
    sql_script = sql_file.read()

cursor.executescript(sql_script)

# Logging schema creation
print("schema created!")

"""
# Getting the csv column names
try:
    with open("../data/Electric_Vehicle_Population_Data.csv", "r") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
    print("CSV Fieldnames: ", fieldnames)

except Exception as e:
    print("Error:", e)

# Expected output
# Field names:  ['VIN (1-10)', 'County', 'City', 'State', 'Postal Code', 'Model Year', 'Make', 'Model', 'Electric Vehicle Type', 'Clean Alternative Fuel Vehicle (CAFV) Eligibility', 'Electric Range', 'Legislative District', 'DOL Vehicle ID', 'Vehicle Location', 'Electric Utility', '2020 Census Tract']
"""

# Pre-structured column Mappings for .csv file to ev_washington table
column_mappings = {
    "VIN (1-10)": "vin",
    "County": "county",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "Model Year": "model_year",
    "Make": "make",
    "Model": "model",
    "Electric Vehicle Type": "ev_type",
    "Clean Alternative Fuel Vehicle (CAFV) Eligibility": "cafv_eligibility",
    "Electric Range": "ev_range",
    "Legislative District": "legislative_district",
    "DOL Vehicle ID": "dol_vehicle_id",
    "Vehicle Location": "coordinate",
    "Electric Utility": "electric_utility",
    "2020 Census Tract": "census_tract_2020",
}

# Columns that the csv data will be inserted into
table_columns_list = list(column_mappings.values())

# Writing the structure of the SQL INSERT statement
sql_insert = f"""
INSERT INTO ev_washington ({", ".join(table_columns_list)})
    VALUES ({", ".join(["?"] * len(table_columns_list))})
"""

# Reading .csv rows and converting them to tuples following the
# table_columns_list order

csv_rows = []

with open("../data/Electric_Vehicle_Population_Data.csv", "r") as file:
    reader = csv.DictReader(file)

    for row in reader:
        csv_rows.append(
            tuple(row[csv_column_name] for csv_column_name in column_mappings.keys())
        )

# Performing the SQL INSERT statement using .executemany()method
cursor.executemany(sql_insert, csv_rows)

# Commiting insert and closing connection
connection.commit()

# Validation Check
sql_check = "SELECT * FROM ev_washington LIMIT 10;"
cursor.execute(sql_check)
print(cursor.fetchall())

# Closing Connection
connection.close()
