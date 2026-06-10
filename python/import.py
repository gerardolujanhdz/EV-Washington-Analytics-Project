# Pipeline for importing csv file
import csv
import sqlite3
import os
import logging

# constants
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/ev_washington.db")
LOG_PATH = os.path.join(os.path.dirname(__file__), "./import.log")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "../sql/schema.sql")

POPUlATION_CSV_PATH = os.path.join(
    os.path.dirname(__file__), "../data/Electric_Vehicle_Population_Data.csv"
)
REGISTRATION_CSV_PATH = os.path.join(
    os.path.dirname(__file__),
    "../data/Electric_Vehicle_Title_and_Registration_Activity_20260523.csv",
)

# pre-structured column Mappings for the .csv files
population_column_mappings = {
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

registration_column_mappings = {
    "VIN (1-10)": "vin",
    "DOL Vehicle ID": "dol_vehicle_id",
    "Model Year": "model_year",
    "Make": "make",
    "Model": "model",
    "Clean Alternative Fuel Vehicle Type": "ev_type",
    "Primary Use": "primary_use",
    "New or Used Vehicle": "used_status",
    "Electric Range": "ev_range",
    "Odometer Reading": "odometer",
    "Odometer Reading Description": "odometer_description",
    "Sale Price": "sale_price",
    "Sale Date": "sale_date",
    "Transaction Type": "transaction_type",
    "Transaction Date": "transaction_date",
    "Year": "transaction_year",
    "County": "county",
    "City": "city",
    "State": "state",
    "Postal Code": "postal_code",
    "2019 HB 2042: Clean Alternative Fuel Vehicle (CAFV) Eligibility": "cafv_eligibility",
    "Meets 2019 HB 2042 Electric Range Requirement": "meets_hb2042_range_requirement",
    "Meets 2019 HB 2042 Sale Date Requirement": "meets_hb2042_sale_date_requirement",
    "Meets 2019 HB 2042 Sale Price/Value Requirement": "meets_hb2042_sale_price_requirement",
    "2019 HB 2042: Battery Range Requirement": "hb2042_range_requirement_reason",
    "2019 HB 2042: Purchase Date Requirement": "hb2042_purchase_date_requirement_reason",
    "2019 HB 2042: Sale Price/Value Requirement": "hb2042_sale_price_requirement_reason",
    "Electric Vehicle Fee Paid": "ev_fee_paid",
    "Transportation Electrification Fee Paid": "transportation_electrification_fee_paid",
    "Hybrid Vehicle Electrification Fee Paid": "hybrid_vehicle_electrification_fee_paid",
    "2020 GEOID": "census_tract_2020",
    "Legislative District": "legislative_district",
    "Electric Utility": "electric_utility",
}

# columns that the csv data will be inserted into
population_columns_list = list(population_column_mappings.values())

registration_columns_list = list(registration_column_mappings.values())

# Writing the structure of the SQL INSERT statements
population_sql_insert = f"""
INSERT INTO population ({", ".join(population_columns_list)})
    VALUES ({", ".join(["?"] * len(population_columns_list))})
"""
registration_sql_insert = f"""
INSERT INTO registration ({", ".join(registration_columns_list)})
    VALUES ({", ".join(["?"] * len(registration_columns_list))})
"""


# configuring/creating a logger
logging.basicConfig(
    filename=LOG_PATH,
    encoding="utf-8",
    level=logging.DEBUG,
    filemode="w",
    format="%(levelname)s:%(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    try:
        # connecting to sqlite3 db
        with sqlite3.connect(DB_PATH) as connection:
            logger.info("Connected to database at: %s", DB_PATH)
            cursor = connection.cursor()

            # running schema.sql
            with open(SCHEMA_PATH) as sql_file:
                sql_script = sql_file.read()
                cursor.executescript(sql_script)
                logger.info("Schema script executed")

            # reading csv rows -> into tuples following the column_list order

            population_csv_rows = []
            registration_csv_rows = []

            with open(POPUlATION_CSV_PATH, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    population_csv_rows.append(
                        tuple(
                            None if row[csv_column_name] == "" else row[csv_column_name]
                            for csv_column_name in population_column_mappings.keys()
                        )
                    )

            with open(REGISTRATION_CSV_PATH, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    registration_csv_rows.append(
                        tuple(
                            None if row[csv_column_name] == "" else row[csv_column_name]
                            for csv_column_name in registration_column_mappings.keys()
                        )
                    )
            logger.info("csv rows copied")

            # inserting the rows from the csv into the facts tables using the .executemany()method
            batch_size = 10000
            try:
                for i in range(0, len(population_csv_rows), batch_size):
                    batch = population_csv_rows[i : i + batch_size]
                    cursor.executemany(population_sql_insert, batch)
                connection.commit()
                logger.info(f"Inserted {len(population_csv_rows)} population rows")
            except sqlite3.Error as e:
                connection.rollback()
                logger.error(f"Population insert failed: {e}")

            try:
                for i in range(0, len(registration_csv_rows), batch_size):
                    batch = registration_csv_rows[i : i + batch_size]
                    cursor.executemany(registration_sql_insert, batch)
                connection.commit()
                logger.info(f"Inserted {len(registration_csv_rows)} registration rows")
            except sqlite3.Error as e:
                connection.rollback()
                logger.error(f"Registration insert failed: {e}")

            # Insertion validation Check
            sql_check_population = "SELECT * FROM population LIMIT 5;"
            sql_check_registration = "SELECT * FROM registration LIMIT 5;"

            cursor.execute(sql_check_population)
            print("Population Sample:")
            print(cursor.fetchall())

            cursor.execute(sql_check_registration)
            print("\nRegistration Sample:")
            print(cursor.fetchall())
    except Exception as e:
        logger.error(f"Error: {e}")


# Used once, now unneeded
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
#
"""

"""
# Getting the csv column names
    try:
        with open("../data/Electric_Vehicle_Title_and_Registration_Activity_20260523.csv", "r") as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames
        print("CSV Fieldnames: ", fieldnames)

    except Exception as e:
        print("Error:", e)

# Expected output
# Field names: ['Clean Alternative Fuel Vehicle Type', 'VIN (1-10)', 'DOL Vehicle ID', 'Model Year', 'Make', 'Model', 'Primary Use', 'Electric Range', 'Odometer Reading', 'Odometer Reading Description', 'New or Used Vehicle', 'Sale Price', 'Sale Date', 'Transaction Type', 'Transaction Date', 'Year', 'County', 'City', 'State', 'Postal Code', '2019 HB 2042: Clean Alternative Fuel Vehicle (CAFV) Eligibility', 'Meets 2019 HB 2042 Electric Range Requirement', 'Meets 2019 HB 2042 Sale Date Requirement', 'Meets 2019 HB 2042 Sale Price/Value Requirement', '2019 HB 2042: Battery Range Requirement', '2019 HB 2042: Purchase Date Requirement', '2019 HB 2042: Sale Price/Value Requirement', 'Electric Vehicle Fee Paid', 'Transportation Electrification Fee Paid', 'Hybrid Vehicle Electrification Fee Paid', '2020 GEOID', 'Legislative District', 'Electric Utility']
#
"""
if __name__ == "__main__":
    main()
