# Analytics Project: Washington Electric Vehicle Dataset

To stray sets of meandering eyes,

This is/was a for-practice end-to-end analytics project using publicly available data from Washington State on their electric vehicle population through the years.

## Introduction to the Data

I used the following triplet of datasets for this project:

- [Electric Vehicle Population](https://catalog.data.gov/dataset/electric-vehicle-population-data?from_hint=eyJzb3J0IjoicG9wdWxhcml0eSJ9): A snapshot of the population of electric vehicles in Washington State

- [Electric Vehicle Registration Activity by Year](https://data.wa.gov/Transportation/Electric-Vehicle-Registration-Activity-by-Year/tak8-xdcp): The registration, as well as all the transaction information, for electric vehicles either in or previously in Washington State from 2010 to 2025

- [Resident Population for Counties](https://www.census.gov/data/datasets/time-series/demo/popest/2020s-counties-total.html): The population of Washington and its counties from 2020 to 2025

## Project Overview

With the goal of this project being end-to-end, that meaning, from ingesting of the raw data to modeling the processed data, I outlined the project as such:

1. Setting up an ETL Pipeline (SQL + Python)
  1. Creating a local SQLite Database to house the data in a [star-like schema](https://en.wikipedia.org/wiki/Star_schema) (for Power BI best practice)
  2. Retrieving the data from locally stored .csv|.xlsx files and reformatting it to match the database schema 
  3. Inserting and storing the processed data in the local database for further analysis work
2. EDA (SQL)
  1. Writing some exploratory queries on the data to further check the pipeline and answer some preliminary questions (e.g. most common makes, number of EV registrations per year, etc.)
3. 

1. _Setting up an ETL Pipeline:_ Retrieving the data from CSV files stored locally, reformatting the data to follow a "star-like" database schema and storing the processed data in a SQLite database for further analysis and processing.
2. _Business Ready Outputs:_ Making the outputs of the first step easy to understand and pretty using Microsoft Power BI.
3. Python Modeling: Using the

## Tech Stack Used

- SQLite
  - Used for data processing and storage
- Microsoft Power BI
  - Used for data visualization and "dashboarding"
- Python
  - Used for further data processing and geometric median estimation
