# Imports
import sqlite3
import logging
import os

# constants
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/ev_washington.db")
POPUlATING_SQL_PATH = os.path.join(
    os.path.dirname(__file__), "../sql_scripts/populating.sql"
)
LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/populating.log")

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
    with sqlite3.connect(DB_PATH) as connection:
        logger.info("Connected to database at %s", DB_PATH)
        cursor = connection.cursor()
        with open(POPUlATING_SQL_PATH, "r") as sql_file:
            sql_script = sql_file.read()
            cursor.executescript(sql_script)
            logger.info("Populating script executed")
        connection.commit()
        logger.info("Script Committed")


if __name__ == "__main__":
    main()
