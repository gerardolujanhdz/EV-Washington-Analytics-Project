# imports
import os
import logging
import sqlite3

import sys

cwd = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cwd)
sys.path.append(par_dir)

from analysis import geometric_median_computation
from county_population_imports import main as cpi_main


# paths
DB_PATH = os.path.join(
    os.path.dirname(__file__), "../../data/database/ev_washington.db"
)
LOG_PATH = os.path.join(os.path.dirname(__file__), "../../logs/gm_pop_insert.log")

# logging configuration
logging.basicConfig(
    filename=LOG_PATH,
    encoding="utf-8",
    level=logging.DEBUG,
    filemode="w",
    format="%(levelname)s:%(message)s",
)
logger = logging.getLogger(__name__)

# sql db table structures
gm_table_columns_list = ["region", "latitude", "longitude"]
county_pops_table_columns_list = ["county", "population"]

# squeel insert queries (using same logic as in import.py)
gm_table_sql_insert = f"""
INSERT OR IGNORE INTO region_geometric_medians ({", ".join(gm_table_columns_list)})
    VALUES ({",".join(["?"] * len(gm_table_columns_list))})
"""
county_pops_table_sql_insert = f"""
INSERT OR IGNORE INTO county_populations ({", ".join(county_pops_table_columns_list)})
    VALUES ({",".join(["?"] * len(county_pops_table_columns_list))})
"""


def dict_to_list(dict, list_name) -> list:
    list_name = []

    # insert data in dictionary into list as tuple entries
    for key, value in dict.items():
        if isinstance(value, int):
            list_name.append((key, value))
        else:
            list_name.append((key, value[0], value[1]))
    return list_name


def list_to_sql_table(cursor, list_name, sql_query, table_name) -> None:

    # insert data from list into sql table
    try:
        cursor.executemany(sql_query, list_name)
        logger.info(
            "inserted %s rows from %s into %s", len(list_name), list_name, table_name
        )
    except sqlite3.Error as e:
        logger.error("%s insert failed :%s", table_name, e)


def main() -> None:
    try:
        # importing {region:geometric_median} dict and {county:2025 population} dict
        coords_gm_dict = geometric_median_computation.main()
        county_pops_dict = cpi_main()

        logger.info("geometric median + county populations loaded in")

        with sqlite3.connect(DB_PATH) as connection:
            logger.info("Connected to db at %s", DB_PATH)
            cursor = connection.cursor()

            gm_rows = []
            gm_rows = dict_to_list(coords_gm_dict, gm_rows)
            print(gm_rows)
            list_to_sql_table(
                cursor, gm_rows, gm_table_sql_insert, "region_geometric_medians"
            )

            county_pops_rows = []
            county_pops_rows = dict_to_list(county_pops_dict, county_pops_rows)
            print(county_pops_rows)
            list_to_sql_table(
                cursor,
                county_pops_rows,
                county_pops_table_sql_insert,
                "county_populations",
            )

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
