# imports
import pandas as pd
import numpy as np

import logging
import os
import sqlite3

import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json

from geometric_median_computation import load_in_coordinates, main as gm_main
from county_population_imports import main as cpi_main

# constants
LOG_PATH = os.path.join(os.path.dirname(__file__), "../logs/visualizations.log")
DB_PATH = os.path.join(os.path.dirname(__file__), "../database/ev_washington.db")

region_dict = {
    "San Juan": "Northwest",
    "Kitsap": "Peninsulas",
    "Clallam": "Peninsulas",
    "Jefferson": "Peninsulas",
    "Grays Harbor": "Peninsulas",
    "Mason": "Peninsulas",
    "Pacific": "Southwest",
    "Thurston": "Metro Puget Sound",
    "Lewis": "Southwest",
    "Wahkiakum": "Southwest",
    "Cowlitz": "Southwest",
    "Clark": "Southwest",
    "Skamania": "Southwest",
    "Pierce": "Metro Puget Sound",
    "King": "Metro Puget Sound",
    "Snohomish": "Metro Puget Sound",
    "Skagit": "Northwest",
    "Whatcom": "Northwest",
    "Okanogan": "North Central",
    "Chelan": "North Central",
    "Douglas": "North Central",
    "Kittitas": "North Central",
    "Yakima": "Wine Country",
    "Klickitat": "Wine Country",
    "Grant": "North Central",
    "Benton": "Wine Country",
    "Ferry": "Eastern",
    "Stevens": "Eastern",
    "Pend Oreille": "Eastern",
    "Lincoln": "Eastern",
    "Spokane": "Eastern",
    "Adams": "Eastern",
    "Franklin": "Wine Country",
    "Walla Walla": "Wine Country",
    "Columbia": "Wine Country",
    "Garfield": "Wine Country",
    "Asotin": "Wine Country",
    "Whitman": "Eastern",
    "Island": "Northwest",
}

# configuring/creating a logger
logging.basicConfig(
    filename=LOG_PATH,
    encoding="utf-8",
    level=logging.DEBUG,
    filemode="w",
    format="%(levelname)s:%(message)s",
)
logger = logging.getLogger(__name__)


# loading in location data for choropleth mapbox county level
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


def add_pop_count(county_pops: dict[str, int], df: pd.DataFrame) -> pd.DataFrame:
    df["pop_count"] = df["County"].map(county_pops)
    return df


def add_per_person(df: pd.DataFrame) -> pd.DataFrame:
    df["ev_per_person_count"] = df.apply(
        lambda row: row["Count per County"] / row["pop_count"], axis=1
    )
    return df


def county_grouping_df(df: pd.DataFrame) -> pd.DataFrame:
    county_df = (
        df.groupby(["County", "fips_location"], as_index=False)["Count per Coordinate"]
        .sum()
        .rename(columns={"Count per Coordinate": "Count per County"})
    )
    return county_df


def add_log_count(df: pd.DataFrame) -> pd.DataFrame:
    df["log_count"] = np.log10(df["Count per County"])
    return df


def dataframe_transformations(
    df: pd.DataFrame, county_fips_dict: dict[str, str], pop_counts: dict[str, int]
) -> pd.DataFrame:
    df = add_df_fips_index(county_fips_dict, df)
    df = county_grouping_df(df)
    df = add_pop_count(pop_counts, df)
    df = add_log_count(df)
    df = add_per_person(df)
    return df


def gm_plot(
    df: pd.DataFrame, gm_dict: dict[str, list[float]], counties: dict, region_dict: dict
) -> go.Figure:

    # choroplethmapbox underlay (color coded counties by region), scattermapbox over lay with corresponding gm approximation
    df = df[
        ["County", "fips_location"]
    ].copy()  # left with county, fips_location, need a region column
    df["Region"] = df["County"].map(region_dict)

    # creating pd.dataframe from dictonary
    region_gm_df = pd.DataFrame(
        [(key, value[0], value[1]) for key, value in gm_dict.items()],
        columns=["region", "longitude", "latitude"],
    )

    fig = px.choropleth_map(
        data_frame=df,
        geojson=counties,
        locations="fips_location",
        color="Region",
        featureidkey="properties.COUNTY",
        center={"lat": 47.45, "lon": -120.9},
        zoom=6,
        hover_name="County",
        hover_data={"fips_location": False},
    )

    fig.add_trace(
        go.Scattermap(
            lat=region_gm_df["latitude"],
            lon=region_gm_df["longitude"],
            text=region_gm_df["region"],
            mode="markers",
            marker=dict(size=12, color="rgb(0, 0,0)"),
            hovertemplate="<b>%{text}</b><br>Lat: %{lat:.3f}<br>Lon: %{lon:.3f}<extra></extra>",
            name="Geometric Median",
        )
    )

    print(df)
    return fig


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


def main() -> None:
    try:
        with sqlite3.connect(DB_PATH) as connection:
            logger.info("Connected to database at: %s", DB_PATH)
            coordinates_df = load_in_coordinates(connection=connection)

        pop_counts = cpi_main()
        counties = load_counties()
        gm_dict = gm_main()
        county_fips_dict = get_county_fips_dict(counties)
        coordinates_df = dataframe_transformations(
            coordinates_df, county_fips_dict, pop_counts
        )
        # plot_choropleth_map_raw(coordinates_df, counties).show()
        # plot_choropleth_map_norm(coordinates_df, counties).show()
        gm_plot(coordinates_df, gm_dict, counties, region_dict).show()
    except Exception as e:
        logger.error("Error: %s", e)
        raise


if __name__ == "__main__":
    main()

