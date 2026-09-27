"""
This module provides fucntionality for managing predictions.

It contains the ModelInferenceService class, which offers methods
to load a model from a file, and to make predictions using the loaded model.
"""

import pickle as pk
from pathlib import Path

from loguru import logger

from config import model_settings


class ModelInferenceService:
    """
    A service class for making predictions.

    This class provides functionalities to load an ML model from
    a specified path, and make predictions using the loaded model.

    Attributes:
        model: ML model managed by this service. Initially set to None.
        model_path: Directory to extract the model from.
        model_name: Name of the saved model to use.

    Methods:
        __init__: Constructor that initializes the ModelInferenceService.
        load_model: loads the model from file or builds it if it doesn't exist.
        predict: Makes a prediction using the loaded model.
    """

    def ___init__(self) -> None:
        """Initializes the ModelInferenceService with no model loaded."""
        self.model = None

    def load_model(self) -> None:
        """
        Loads the model from a specified path.

        Raises:
            FilenotFoundError: If the model file not exist at specified dir.
        """
        self.model = None
        self.model_path = model_settings.model_path
        self.model_name = model_settings.model_name
        self.model_full_path = Path(f'{self.model_path}/{self.model_name}',)

        logger.info(
            'checking the exitence of model config file'
            f'at {self.model_full_path}',
        )

        if not self.model_full_path.exists():
            raise FileNotFoundError('Model file does not exist!')

        logger.info(
            f'model {self.model_name} exists! -> '
            'loading model configuration file'
        )

        with open(self.model_full_path, 'rb') as model_file:
            self.model = pk.load(model_file)

    def predict(self, input_parameters: list) -> list:
        """
        Makes a prediction using the loaded model.

        Takes input parameters and passes it to the model, which
        was loaded using a pickle file.

        Args:
            input_parameters (list): The input data for making a prediction.

        Returns:
            list: The prediction result from the model.
        """
        logger.info('making prediction!')
        return self.model.predict([input_parameters])
