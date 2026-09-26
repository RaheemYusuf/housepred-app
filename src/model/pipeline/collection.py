"""
This module provides functionalities to load data from a database.

It includes a function to extract data from the RentApartments table
in the database and load it into a pandas DataFrame. This module is useful
for scenarios where data needs to be retrieved from a database for further
analysis or processing. It uses duckdb for executing database queries and
pandas for handling the data in a DataFrame format.
"""

import pandas as pd
from loguru import logger

from config import db, db_settings


def load_data() -> pd.DataFrame:
    """
    Extract raw data from the RentApartments.csv file.

    Returns:
        pd.DataFrame: DataFrame containing the RentApartments data.
    """
    file_path = db_settings.data_file_name
    logger.info(f'loading csv file at path {file_path}')
    return pd.read_csv(file_path)


def load_data_from_db() -> pd.DataFrame:
    """
    Extract raw the entire RentApartmentstable from the database.

    Returns:
        pd.DataFrame: DataFrame containing the RentApartments data.
    """
    table_name = db_settings.table_name
    logger.info(f'Reading data from {table_name}')
    db.init_db()
    query = f'SELECT * FROM {table_name}'
    result_df = db.query_to_df(query)
    return result_df


def check_data_types() -> pd.DataFrame:
    """
    Check the data type of the columns of the RentApartments table from db.

    Returns:
        pd.DataFrame: DataFrame containing schema info of RentApartments table.
    """
    query = f'DESCRIBE {db_settings.table_name}'
    # Returns a DataFrame with columns: column_name, column_type,
    # null, key, default, extra
    schema_df = db.query_to_df(query)
    return schema_df


# Test
# df = load_data_from_db()
# print(df)
# print()
# types_df = check_data_types()
# print(types_df)
