"""
This module provides functionality for preparing a dataset for ML model.

It consists of functions to load data from a database, encode categorical
columns, and parse specific columns for further processing.
"""

import re

import pandas as pd
from loguru import logger

from model.pipeline.collection import load_data_from_db


def prepare_data() -> pd.DataFrame:
    """
    Prepare the dataset for analysis and modelling.

    This involves loading the data, encoding categorical columns,
    and parsing the 'garden' column.

    Returns:
        pd.DataFrame: The processed dataset.
    """
    logger.info('starting up preprocessing pipeline')
    dataframe = load_data_from_db()
    data_encoded = _encode_cat_cols(dataframe)
    return _parse_garden_col(data_encoded)


def _encode_cat_cols(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Encode categorical columns into dummy variables.

    Arg:
        data (pd.DataFrame): The original dataset.

    Returns:
        pd.DataFrame: Dataset with categorical columns encoded.
    """
    columns_to_exclude = [
        'address',
        'facilities',
        'zip',
        'neighborhood',
        'energy',
        'garden',
    ]
    # empty list to saved the extracted columns
    columns_to_be_transformed = [
        col
        for col in dataframe.columns
        if dataframe[col].dtype == 'str' and col not in columns_to_exclude
    ]
    logger.info(f'encoding categorical columns: {columns_to_be_transformed}')
    # encode the columns
    return pd.get_dummies(
        dataframe,
        columns=columns_to_be_transformed,
        drop_first=True,
        dtype=int
    )


def _parse_garden_col(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Parse the 'garden' column in the dataset.

    Args:
        data (pd.DataFrame): The dataset with a 'garden' column.

    Returns:
        pd.DataFrame: The dataset with the 'garden' column parsed.
    """
    logger.info("parsing garden column")
    for index in range(len(dataframe)):
        garden_value = str(dataframe.loc[index, 'garden'])
        if garden_value == 'Not present':
            dataframe.loc[index, 'garden'] = '0'
        else:
            dataframe.loc[index, 'garden'] = re.findall(
                r'\d+', garden_value
            )[0]

    # Convert the whole column to integers
    dataframe['garden'] = dataframe['garden'].astype(int)
    return dataframe


# test
# prep = prepare_data()
# print(prep.dtypes)
# data = load_data_from_db()
# data_encoded = encode_cat_cols(data)
# print(data_encoded)
