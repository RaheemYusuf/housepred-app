"""
This module creates the pipeline for building, training and saving ML model.

It includes the process of data preparation, model training using
RandomForestRegressor, hyperparameter tuning with GridSearchCV,
model evaluation, and serialization of the trained model.
"""

import pickle as pk

import pandas as pd
from loguru import logger
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split

from config import model_settings
from model.pipeline.preparation import prepare_data


def build_model() -> None:
    """
    Build, evaluate and save a RandomForestRegressor model.

    This function orchestrates the model building pipeline.
    It starts by preparing the data, followed by defining feature names
    and splitting the dataset into features and target variables.
    The dataset is then divided into training and testing sets.
    The model's performance is evaluated on the test set, and
    finally, the model is saved for future use.

    Arg:
        None

    Return:
        None
    """
    logger.info("starting up model building pipeline")
    df = prepare_data()
    X, y = _get_x_y(df)
    X_train, X_test, y_train, y_test = _split_train_test(
        X,
        y,
    )
    rf = _train_model(
        X_train,
        y_train,
    )
    _evaluate_model(
        rf,
        X_test,
        y_test,
    )
    _save_model(rf)


def _get_x_y(dataframe: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split the dataset into features and target variable.

    Arg:
        data (pd.DataFrame): The dataset to be split.

    Returns:
        tuple: Features and target variables.
    """
    num_col_not_used = [
        'rooms',
        'bathrooms',
        'rent',
    ]
    num_col_used = [
        col
        for col in dataframe.columns
        if (
            dataframe[col].dtype == 'int64'
            or dataframe[col].dtype == 'float64'
        )
        and col not in num_col_not_used
    ]
    X = dataframe[num_col_used]
    y = dataframe["rent"]
    logger.info(f'defining X and y variables. \nX vars: {X}\ny var: {y}')
    return X, y


def _split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Split the data into training and testing sets.

    Args:
        X (pd.DataFrame): Features dataset.
        y (pd.Series): Target variable.

    Returns:
        tuple: Training and testing sets for features and target.
    """
    logger.info("splitting data into train and test sets")
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
    )
    return X_train, X_test, y_train, y_test


def _train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
) -> RandomForestRegressor:
    """
    Train the RandomForestRegressor model with hyperparameter tuning.

    Args:
        X_train (pd.DataFrame): Training set features.
        y_train (pd.Series): Training set target.

    Return:
        RandomForestRegressor: The best estimator after GridSearch.
    """
    logger.info('training a model with hyperparameters')
    grid_space = {
        "n_estimators": [100, 200, 300],
        "max_depth": [3, 6, 9, 12],
    }
    logger.debug(f'grid_space = {grid_space}')
    grid = GridSearchCV(
        RandomForestRegressor(),
        param_grid=grid_space,
        cv=5,
        scoring="r2",
    )
    model_grid = grid.fit(
        X_train,
        y_train,
    )
    return model_grid.best_estimator_


def _evaluate_model(
    model: RandomForestRegressor,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> float:
    """
    Evaluate the trained model's performance.

    Args:
        model (RandomForestRegressor): The trained model.
        X_test (pd.DataFrame): Testing set features.
        y_test (pd.Series): Testing set target.

    Return:
        float: The model's score.
    """
    model_score = model.score(
        X_test,
        y_test,
    )
    logger.info(f'evaluating model performance. SCORE = {model_score}')
    return float(model_score)


def _save_model(model: RandomForestRegressor) -> None:
    """
    Save the trained model to a specified directory.

    Args:
        model (RandomForestRegressor): The model to save.

    Return:
        None
    """
    model_full_path = (
        f'{model_settings.model_path}/{model_settings.model_name}'
    )
    logger.info(f'saving a model to a directory: {model_full_path}')
    with open(model_full_path, 'wb') as model_file:
        pk.dump(model, model_file)


# test
# build_model()
# X,_ = get_X_y(prepare_data())
# print(X.dtypes)
