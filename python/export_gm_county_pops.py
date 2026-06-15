# imports
import os
import logging
import sqlite3

from coordinate_analysis import main as ca_main
from ../data_processing/county_population_imports.py import main as cpi_main

# paths
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/ev_washington.db")
LOG_PATH = os.path.join(os.path.dirname(__file__), "./export_gm_county_pops.log")

# logging configuration
logging.basicConfig(
    filename=LOG_PATH,
    encoding="utf-8",
    level=logging.DEBUG,
    filemode="w",
    format="%(levelname)s:%(message)s",
)
logger = logging.getLogger(__name__)

gm_table_columns_list = ["county", "latitude", "longitude"]
county_pops_table_columns_list = ["county", "population"]

gm_table_sql_insert = f"""
INSERT OR IGNORE INTO region_geometric_medians ({", ".join(gm_table_columns_list)})
    VALUES ({",".join(["?"] * len(gm_table_columns_list))})
"""
county_pops_table_sql_insert = f"""
INSERT OR IGNORE INTO county_populations ({", ".join(county_pops_table_columns_list)})
    VALUES ({",".join(["?"] * len(county_pops_table_columns_list))})
"""


def main() -> None:
    try:
        coordinates_df, coords_gm_dict = ca_main()
        county_pops_dict = cpi_main()
        with sqlite3.connect(DB_PATH) as connection:
            logger.info("Connected to db at %s", DB_PATH)
            cursor = connection.cursor()

            gm_rows = []
            county_pops_rows = []

            # inserting data into tables
            for key, value in county_pops_dict.items():
                county_pops_rows.append((key, value))

            for key, value in coords_gm_dict.items():
                gm_rows.append((key, value[1], value[0]))

            try:
                cursor.executemany(county_pops_table_sql_insert, county_pops_rows)
                logger.info("Inserted county population data")
            except sqlite3.Error as e:
                logger.error("Population insert failed : %s", e)
            try:
                cursor.executemany(gm_table_sql_insert, gm_rows)
                logger.info("Inserted county population data")
            except sqlite3.Error as e:
                logger.error("Geometric median insert failed %s", e)

            """
            # checks
            sql_check_gm = "SELECT * FROM region_geometric_medians LIMIT 5;"
            sql_check_population = "SELECT * FROM county_populations LIMIT 5;"

            try:
                cursor.execute(sql_check_gm)
                print("gm sample:")
                print(cursor.fetchall())

                cursor.execute(sql_check_population)
                print("popuation sample:")
                print(cursor.fetchall())
            except sqlite3.Error as e:
                print(f"Table check failed : {e}")
            """
    except Exception as e:
        print(e)
        raise


if __name__ == "__main__":
    main()
