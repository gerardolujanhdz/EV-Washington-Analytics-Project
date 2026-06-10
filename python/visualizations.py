# imports
import numpy as np
import pandas as pd
import plotly
from coordinate_analysis import main as ca_main


def main() -> None:
    coordinates_df, results = ca_main()


if __name__ == "__main__":
    main()
