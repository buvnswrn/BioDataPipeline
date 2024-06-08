import numpy as np
import pandas as pd

from src.decorator.LoggerDecoratorFactory import LoggerDecoratorFactory

logger = LoggerDecoratorFactory("Transformer").log_time


class Transformer:
    """
    Base Transformer class to be inherited by the child classes
    """

    def __init__(self, schema):
        """
        Constructor for Transformer class
        :param schema: the schema to validate the data
        """
        self.schema = schema

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform method to be implemented by the child class
        :param data: the data to transform
        :return: transformed data as a pandas DataFrame
        """
        data = data.replace('n.a.', np.nan)
        for column in data.columns:
            data[column] = data[column].astype(self.schema[column]())
        return data


class BasicTransformer(Transformer):
    def __init__(self, schema):
        super().__init__(schema)

    @logger
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform method to transform the data.
        It drops the rows with missing values and duplicates.
        :param schema: the schema to validate the data
        :param data: the data to transform
        :return: transformed data as a pandas DataFrame
        """
        # data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)
        return data


class NPASSTransformer(BasicTransformer):
    """
    Transformer class to transform data from NPASS dataset
    """

    def __init__(self, schema):
        super().__init__(schema)

    @logger
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform method to transform the data.
        It drops the rows with missing values and duplicates.
        It also renames the columns to the npass column names.
        :param data: the data to transform
        :return: transformed data as a pandas DataFrame
        """
        data = super().transform(data)
        # replace column names with npass column names
        data = data.add_prefix("npass_")
        return data
