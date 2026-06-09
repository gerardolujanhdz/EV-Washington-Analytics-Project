# imports
import pandas as pd
import numpy as np

import pyproj
from scipy.spatial.distance import cdist, euclidean

import logging
import sqlite3
import os


# projections used for Coordinate(lat,long)
wgs84 = pyproj.CRS("EPSG:4326")  # source

# constants
EPSILON = 1e-6
DB_PATH = os.path.expanduser("~/code/analytics/ev/database/ev_washington.db")
LOG_PATH = os.path.expanduser("~/code/analytics/ev/python/coordinate_analysis.log")

# dictionary used to store projections for each region
region_projections: dict[str, pyproj.CRS] = {
    "Northwest": pyproj.CRS("EPSG:32610"),
    "Peninsulas": pyproj.CRS("EPSG:32610"),
    "Southwest": pyproj.CRS("EPSG:32610"),
    "Metro Puget Sound": pyproj.CRS("EPSG:32610"),
    "North Central": pyproj.CRS("EPSG:2285"),
    "Wine Country": pyproj.CRS("EPSG:2286"),
    "Eastern": pyproj.CRS("EPSG:32611"),
}

# squeel query that will be used to import coords from .db
sql_query = """
SELECT 
	l.region AS Region,
	c.longitude AS Longitude,
	c.latitude AS Latitude,
	COUNT(*) AS "Count per Coordinate"
FROM 
	population 
	LEFT JOIN locations l ON population.location_id = l.location_ID
	LEFT JOIN coordinates c ON population.coordinate_id = c.coordinate_id
WHERE l.state = 'WA' AND 
	c.latitude IS NOT NULL AND 
	c.longitude IS NOT NULL
GROUP BY c.latitude, c.longitude 
ORDER BY "Count per Coordinate" DESC;
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


#     reference: scoutant/l1_median.py (shoutout)
def weighted_l1_median(X: np.ndarray, WX: np.ndarray, eps: float = 1e-6) -> np.ndarray:
    """
    Approximates the weighted geometric median using the Weiszeld algorithm
    Minimizes weighted sum of Euclidean distances until convergence threshold met

    And returns the weighted geometric median of the set of points in [x, y] format
    """
    y = np.average(X, axis=0, weights=WX)
    while True:
        while np.any(cdist(X, [y]) == 0):
            y += 0.1 * np.ones(len(y))
        W = np.expand_dims(WX, axis=1) / cdist(X, [y])
        y1 = np.sum(W * X, 0) / np.sum(W)
        if euclidean(y, y1) < eps:
            return y1
        y = y1


# querying for region, unique(long, lat), (long,lat) pairing count
def load_in_coordinates(connection: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql_query(sql=sql_query, con=connection)
    logger.info("Loaded %d coordinate rows from the ev_washington database", len(df))
    logger.debug("Sample:\n%s", df.head())
    return df


# creating x,y columns of the 2d cartesian projections
def wgs84_to_cartesian(df: pd.DataFrame, projection: pyproj.CRS) -> pd.DataFrame:
    transformer = pyproj.Transformer.from_crs(wgs84, projection, always_xy=True)
    df["x"], df["y"] = transformer.transform(
        df["Longitude"].to_numpy(), df["Latitude"].to_numpy()
    )
    return df


# gm_approximation
def approx_gm(df: pd.DataFrame) -> np.ndarray:
    points = df[["x", "y"]].to_numpy()
    weights = df["Count per Coordinate"].to_numpy()
    return weighted_l1_median(points, weights, EPSILON)


# transforming 2d cartesian gm_approximation back to (long, lat) projction
def cartesian_to_wgs84(point: np.ndarray, source: pyproj.CRS) -> tuple[float, float]:
    transformer = pyproj.Transformer.from_crs(source, wgs84, always_xy=True)
    return transformer.transform(point[0], point[1])


def main() -> None:
    try:
        # connecting to sqlite3 db
        with sqlite3.connect(DB_PATH) as connection:
            logger.info("Connected to database at: %s", DB_PATH)
            coordinates_df = load_in_coordinates(connection=connection)

        results: dict[str, tuple[float, float]] = {}

        for region, crs in region_projections.items():
            region_df = coordinates_df[coordinates_df["Region"] == region].copy()
            region_df = wgs84_to_cartesian(region_df, projection=crs)
            cartesian_gm = approx_gm(region_df)
            longitude, latitude = cartesian_to_wgs84(cartesian_gm, crs)
            results[region] = (longitude, latitude)
            logger.info("%-20s -> (long: %.6f, lat: %.6f)", region, longitude, latitude)

        # Printing results
        print("Final Geometric Median Approximations per region:")
        for region, result in results.items():
            print(
                "{:<20} -> (longitude: {:.6f}, latitude: {:.6f})".format(
                    region, result[0], result[1]
                )
            )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
