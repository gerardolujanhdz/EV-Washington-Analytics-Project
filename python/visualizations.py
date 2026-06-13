# imports
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json

from coordinate_analysis import main as ca_main
from county_population_imports import main as cpi_main


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


def add_pop_counts(county_pops: dict[str, int], df: pd.DataFrame) -> pd.DataFrame:
    df["pop"] = df["County"].map(county_pops)
    return df


def add_per_person(df: pd.DataFrame, pop_counts: dict[str, int]) -> pd.DataFrame:
    df["ev_per_person_count"] = df.apply(
        lambda row: row["Count per County"] / pop_counts[row["County"]], axis=1
    )
    return df


def region_grouping_df(df: pd.DataFrame) -> pd.DataFrame:
    county_df = (
        df.groupby(["County", "fips_location"], as_index=False)["Count per Coordinate"]
        .sum()
        .rename(columns={"Count per Coordinate": "Count per County"})
    )
    return county_df


def add_log_count(df: pd.DataFrame) -> pd.DataFrame:
    df["log_count"] = np.log10(df["Count per County"])
    return df


def plot_choropleth_map_raw(df: pd.DataFrame, counties: dict) -> go.Figure:
    fig = px.choropleth_map(
        data_frame=df,
        geojson=counties,
        locations="fips_location",
        color="log_count",
        color_continuous_scale="YlGn",
        zoom=6,
        center={"lat": 47.45, "lon": -120.9},
        featureidkey="properties.COUNTY",
        title="Count of Electric Vehicles per County",
        hover_name="County",
        hover_data={
            "Count per County": True,
            "fips_location": False,
            "log_count": False,
            "ev_per_person_count": False,
        },
    )
    fig.update_coloraxes(
        colorbar_ticklabelposition="outside",
        colorbar_tickmode="array",
        colorbar_tickvals=[1, 2, 3, 4, 5],
        colorbar_ticktext=["10", "100", "1,000", "10,000", "100,000"],
        colorbar_title_text="EV Count",
    )
    fig.update_layout(font_family="Geneva")
    return fig


def plot_choropleth_map_norm(df: pd.DataFrame, counties: dict) -> go.Figure:
    fig = px.choropleth_map(
        data_frame=df,
        geojson=counties,
        locations="fips_location",
        color="ev_per_person_count",
        color_continuous_scale="YlGn",
        zoom=6,
        center={"lat": 47.45, "lon": -120.9},
        featureidkey="properties.COUNTY",
        title="Count of Electric Vehicles per County",
        hover_name="County",
        hover_data={
            "Count per County": False,
            "fips_location": False,
            "log_count": False,
            "ev_per_person_count": True,
        },
    )
    fig.update_coloraxes(colorbar_title_text="EVs per Person")
    fig.update_layout(font_family="Geneva")
    return fig


def main() -> pd.DataFrame:
    coordinates_df, coords_gms = ca_main()
    pop_counts = cpi_main()
    counties = load_counties()
    county_fips_dict = get_county_fips_dict(counties)
    coordinates_df = add_df_fips_index(county_fips_dict, coordinates_df)
    coordinates_df = region_grouping_df(coordinates_df)
    coordinates_df = add_log_count(coordinates_df)
    coordinates_df = add_per_person(coordinates_df, pop_counts)
    # plot_choropleth_map_raw(coordinates_df, counties).show()
    # plot_choropleth_map_norm(coordinates_df, counties).show()
    return coordinates_df


if __name__ == "__main__":
    main()
