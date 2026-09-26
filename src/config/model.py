"""
This module sets up the ML model configuration.

It utilises Pydantic's BaseSettings for configuration management,
allowing settings to be read from environment variables and a .env file.
"""

from pydantic import DirectoryPath, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelSettings(BaseSettings):
    """
    Ml model configuration settings for the application.

    Attributes:
        model_config (SettingsConfigDict): Model  config,
        loaded from .env file.
        data_file_name (FilePath): File system path to the raw data file.
        model_path (DirectoryPath): File system path too the model.
        model_name (str): Name of the ML model.
    """

    model_config = SettingsConfigDict(
        env_file='config/.env',
        env_file_encoding='utf-8',
        extra="ignore",
    )

    data_file_name: FilePath
    model_path: DirectoryPath
    model_name: str


model_settings = ModelSettings()
