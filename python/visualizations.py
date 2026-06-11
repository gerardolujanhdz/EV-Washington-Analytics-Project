# imports
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json

from coordinate_analysis import main as ca_main


def load_counties() -> dict:
    with urlopen(
        "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
    ) as response:
        counties = json.load(response)
        # Washington State Fips Code : '53'
    filtered_counties = {
        **counties,
        "features": [
            county_data
            for county_data in counties["features"]
            if county_data["properties"]["STATE"] == "53"
        ],
    }
    return filtered_counties


def get_county_fips_dict(counties: dict) -> dict:
    county_fips_dict = {}
    for county_data in counties["features"]:
        if county_data["properties"]["NAME"] not in county_fips_dict:
            county_fips_dict[county_data["properties"]["NAME"]] = county_data[
                "properties"
            ]["COUNTY"]
    return county_fips_dict


def add_df_fips_index(
    county_fips_dict: dict[str, str], df: pd.DataFrame
) -> pd.DataFrame:
    df["fips_location"] = df["County"].map(county_fips_dict)
    return df


def add_log_scale_for_coloring(df: pd.DataFrame) -> pd.DataFrame:
    df["log_scale"] = np.log2(df["Count per County"])
    return df


def region_grouping_df(df: pd.DataFrame) -> pd.DataFrame:
    county_df = (
        df.groupby(["County", "fips_location"], as_index=False)["Count per Coordinate"]
        .sum()
        .rename(columns={"Count per Coordinate": "Count per County"})
    )
    return county_df


def plot_choropleth_map(df: pd.DataFrame, counties: dict) -> go.Figure:
    fig = px.choropleth_map(
        df,
        geojson=counties,
        locations="fips_location",
        color="log_scale",
        color_continuous_scale="Viridis",
        zoom=7,
        center={"lat": 47.45, "lon": -120.9},
        featureidkey="properties.COUNTY",
        title="Count of Electric Vehicles per County",
        subtitle="Washington State EV Census",
        hover_name="County",
        hover_data={
            "Count per County": True,
            "fips_location": False,
            "log_scale": False,
        },
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig


def main() -> None:
    coordinates_df, results = ca_main()
    # print(coordinates_df.head())
    counties = load_counties()
    county_fips_dict = get_county_fips_dict(counties)
    coordinates_df = add_df_fips_index(county_fips_dict, coordinates_df)
    coordinates_df = region_grouping_df(coordinates_df)
    coordinates_df = add_log_scale_for_coloring(coordinates_df)
    fig = plot_choropleth_map(coordinates_df, counties)
    fig.show()


if __name__ == "__main__":
    main()
