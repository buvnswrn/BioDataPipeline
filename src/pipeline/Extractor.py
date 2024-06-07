import sqlite3

import pandas as pd
from src.decorator.LoggerDecoratorFactory import LoggerDecoratorFactory

logger = LoggerDecoratorFactory("Extractor").log_time


class Extractor:
    """
    Base Extractor class to be inherited by the child classes
    """
    def __init__(self, config: dict):
        self.config = config

    @logger
    def extract(self) -> pd.DataFrame:
        """
        Extract method to be implemented by the child class
        :return:
        """
        raise NotImplementedError("Extract method not implemented")


class NPASSExtractor(Extractor):
    """
    Extractor class to extract data from NPASS dataset
    """
    def __init__(self, path):
        super().__init__({"path": path})

    @logger
    def extract(self) -> pd.DataFrame:
        """
        Extract method to extract data from NPASS dataset
        :return: extracted data from the dataset as a pandas DataFrame
        """
        file_path = self.config["path"]
        return pd.read_csv(file_path, sep='\t', encoding="ISO-8859-1")


class NAEBExtractor(Extractor):
    """
    Extractor class to extract data from NAEB dataset
    """
    __csv = None

    def __init__(self, path, csv=True):
        self.__csv = csv
        if not self.__csv:
            self.conn = sqlite3.connect(path)
        super().__init__({"path": path, "csv": csv})

    @logger
    def extract(self, table_name=None) -> pd.DataFrame:
        """
        Extract method to extract data from NAEB dataset
        :param table_name: the table name to extract data from the database
        :return: extracted data from the dataset as a pandas DataFrame
        """
        file_path = self.config["path"]
        if self.__csv:
            return pd.read_csv(file_path)
        else:
            return pd.read_sql(table_name, self.conn)


class ChEMBLExtractor(Extractor):
    """
    Extractor class to extract data from ChEMBL dataset
    """
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        super().__init__({"path": path})

    @logger
    def extract(self, table_name=None) -> pd.DataFrame:
        """
        Extract method to extract data from ChEMBL dataset
        :param table_name: the table name to extract data from the database
        :return: extracted data from the dataset as a pandas DataFrame
        """
        return pd.read_sql(table_name, self.conn)
