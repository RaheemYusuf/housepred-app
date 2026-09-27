"""
This module provides fucntionality for building an ML model.

It contains the ModelBuilderService class that offers methods to
train a model, and save it to a specified directory.
"""

from pathlib import Path

from loguru import logger

from config import model_settings
from model.pipeline.model import build_model


class ModelBuilderService:
    """
    A service class for building and saving the ML model.

    This class provides functionalities to train an ML model and
    save it to a specified path.

    Attributes:
        model_path: Directory to save the model to.
        model_name: Name of the saved model.
        model_full_path: It is the model full directory 'model_path/model_name'

    Methods:
        __init__: Constructor that initializes the ModelService.
        train_model: Trains the model and save it to a specified directory.
        predict: Makes a prediction using the loaded model.
    """

    def __init__(self) -> None:
        """Initializes the ModelBuilderService."""
        self.model_path = model_settings.model_path
        self.model_name = model_settings.model_name
        self.model_full_path = Path(
            f'{self.model_path}/{self.model_name}',
        )

    def train_model(self) -> None:
        """Train the model from a specified path, and save to model's dir."""
        logger.info(
            f'building the model config file at {self.model_full_path}',
        )
        build_model()
