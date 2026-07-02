# imports
import pandas as pd
import os

# path to data
DATA_PATH = os.path.join(
    os.path.dirname(__file__), "../../data/raw/washington_pop_data.xlsx"
)

# constants
COL_NAMES = [
    "county",
    "2020",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024",
    "2025",
]


# functions
def read_excel(filepath: str) -> pd.DataFrame:
    df = pd.read_excel(filepath, header=[2, 3], engine="openpyxl", nrows=39, skiprows=1)
    return df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = COL_NAMES
    return df


def rename_counties(df: pd.DataFrame) -> pd.DataFrame:
    # county name structure : ".{County name} County, Washington"
    # vim motion "s/\v \.(.+) County, Washington/\1/"
    df["county"] = df["county"].str.replace(
        r"\.(.+) County, Washington", r"\1", regex=True
    )
    return df


def main() -> dict[str, int]:
    try:
        df = read_excel(DATA_PATH)
        df = rename_columns(df)
        df = rename_counties(df)
        result = pd.Series(df["2025"].values, index=df["county"]).to_dict()
        print(result)
        return result
    except Exception as e:
        print(f"Error : {e}")


if __name__ == "__main__":
    main()
