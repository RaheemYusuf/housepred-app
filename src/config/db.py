"""
This module sets up the database configuration.

It utilises Pydantic's BaseSettings for configuration management,
allowing settings to be read from environment variables and a .env file.
It uses duckdb for database manamgent, loading data from the csv file
available in the data folder.
"""

import duckdb
import pandas as pd
from pydantic import FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict

from db.db_model import PropertyData, get_duckdb_schema


class DbSettings(BaseSettings):
    """
    Database configuration settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Model  config,
        loaded from .env file.
        data_file_name (FilePath): File system path to the raw data file.
        table_name (str): Name of the table in the db.
        db_conn_str (str): Database connection string.
    """

    model_config = SettingsConfigDict(
        env_file='config/.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )

    data_file_name: FilePath
    table_name: str
    db_conn_str: str


db_settings = DbSettings()


class DatabaseCon:
    """
    Setup and configure database for the app.

    This class provides the functionality to create a db using
    duckdb, insert a table into it if it doesn't exist, update
    the table schema and query the whole record set in the table
    and return a pandas dataframe.

    Attributes:
        schema_dicts: It helps get the schema dynamically from
            the PropertyData class
        types_sql: It helps to format the schema for DuckDB's CSV
            reader.
        con: It helps to create a connection to the db and execute
            query
        query: query to be executed on the db

    Methods:
        init_db:  It initialise the db and creates the db object, and
            send query to the database.
        query_to_df (str):  queries the table in the database.
    """

    def init_db(self) -> None:
        """
        It initialise the db and creates the db object, and
            send query to the database
        """
        # 1. Get the schema dynamically from the PropertyData class
        schema_dict = get_duckdb_schema(
            PropertyData,
        )

        # 2. Format it for DuckDB's CSV reader:
        # {'address': 'VARCHAR', 'area': 'DOUBLE', ..}
        types_sql = str(
            schema_dict,
        ).replace("'", "")

        with duckdb.connect(db_settings.db_conn_str) as con:
            # 3. Drop the old table so DuckDB is forced to recreate
            # it with new types
            table_name = db_settings.table_name
            con.execute(f'DROP TABLE IF EXISTS {table_name}')
            # 4. Create the table and strictly enforce these data types
            # while importing the CSV
            query = f"""
                CREATE TABLE IF NOT EXISTS {table_name} AS
                SELECT * FROM read_csv('{table_name}', types={types_sql})
            """
            con.execute(query)

    def query_to_df(self, query_string: str) -> pd.DataFrame:
        """
        queries the table in the database.

        Takes a query_string and return the result in a
            pandas dataframe.

        Arg:
            query_string (str): The SQL query to be sent to the database.

         Returns:
            pd.DataFrame
        """
        with duckdb.connect(db_settings.db_conn_str) as con:
            return con.sql(query_string).df()


db = DatabaseCon()
