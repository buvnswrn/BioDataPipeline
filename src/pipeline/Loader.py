import sqlite3

import pandas as pd

from src.decorator.LoggerDecoratorFactory import LoggerDecoratorFactory

logger = LoggerDecoratorFactory("Loader").log_time


class Loader:
    """
    Base Loader class to be inherited by the child classes
    """

    def __init__(self):
        pass

    def load(self):
        """
        Load method to be implemented by the child class
        :return:
        """
        raise NotImplementedError("Load method not implemented")


class SQLiteLoader(Loader):
    """
    Loader class to load data to SQLite database
    """

    def __init__(self, path):
        super().__init__()
        self.conn = sqlite3.connect(path)

    @logger
    def load(self, data: pd.DataFrame, table_name: str) -> bool:
        """
        Load method to load data to the SQLite database
        :param table_name: the table name to load the data
        :param data: the dataframe to load
        :return: True if the data is loaded successfully else False
        """
        data.to_sql(table_name, self.conn, if_exists='replace')
        return True


class ParquetLoader(Loader):
    """
    Loader class to load data to Parquet file
    """

    def __init__(self, path):
        super().__init__()
        self.path = path

    @logger
    def load(self, data: pd.DataFrame, file_name: str) -> bool:
        """
        Load method to load data to the Parquet file
        :param file_name: the file name to load the data
        :param data: the dataframe to load
        :return: True if the data is loaded successfully else False
        """
        data.to_parquet(self.path + file_name + ".parquet")
        return True