# imports
import pandas as pd
import os

# paths
DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/washington_pop_data.xlsx")

# constants
COL_NAMES = [
    "Geographic_Area",
    "04/01/2020",
    "07/01/2020",
    "07/01/2021",
    "07/01/2022",
    "07/01/2023",
    "07/01/2024",
    "07/01/2025",
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
    df["Geographic_Area"] = df["Geographic_Area"].str.replace(
        r"\.(.+) County, Washington", r"\1", regex=True
    )
    return df


def main() -> dict[str, int]:
    try:
        df = read_excel(DATA_PATH)
        df = rename_columns(df)
        df = rename_counties(df)
        result = pd.Series(
            df["07/01/2025"].values, index=df["Geographic_Area"]
        ).to_dict()
        return result
    except Exception as e:
        print(f"Error : {e}")


if __name__ == "__main__":
    main()
