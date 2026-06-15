import sqlite3
import os
import logging

# constants
DB_PATH = os.path.join(os.path.dirname(__file__), "./ev_washington.db")
LOG_PATH = os.path.join(os.path.dirname(__file__), "./create_db.log")
FILENAME = "ev_washington.db"

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
        if not os.path.isfile(DB_PATH):
            with sqlite3.connect(DB_PATH) as connection:
                logger.info("Database %s formed", FILENAME)
        else:
            print("Database already exists")
    except Exception as e:
        print(f"Database {FILENAME} not formed, error : {e}")


if __name__ == "__main__":
    main()
