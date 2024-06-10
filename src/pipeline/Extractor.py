import sqlite3

from pyspark import pandas as s_pd
from pyspark.pandas import DataFrame
from pyspark.sql import SparkSession

from src.decorator.LoggerDecoratorFactory import LoggerDecoratorFactory

logger = LoggerDecoratorFactory("Extractor").log_time


class Extractor:
    """
    Base Extractor class to be inherited by the child classes
    """

    def __init__(self, config: dict, spark: SparkSession):
        self.config = config
        self.spark = spark

    @logger
    def extract(self) -> DataFrame:
        """
        Extract method to be implemented by the child class
        :return:
        """
        raise NotImplementedError("Extract method not implemented")


class NPASSExtractor(Extractor):
    """
    Extractor class to extract data from NPASS dataset
    """

    def __init__(self, path, spark: SparkSession):
        super().__init__({"path": path}, spark)

    @logger
    def extract(self) -> DataFrame:
        """
        Extract method to extract data from NPASS dataset
        :return: extracted data from the dataset as a pandas DataFrame
        """
        file_path = self.config["path"]
        return self.spark.read.csv(file_path, sep='\t', encoding="ISO-8859-1")


class NAEBExtractor(Extractor):
    """
    Extractor class to extract data from NAEB dataset
    """
    __csv = None

    def __init__(self, path, spark: SparkSession, csv=True):
        self.__csv = csv
        if not self.__csv:
            self.conn = sqlite3.connect(path)
        super().__init__({"path": path, "csv": csv},spark)

    @logger
    def extract(self, table_name=None) -> DataFrame:
        """
        Extract method to extract data from NAEB dataset
        :param table_name: the table name to extract data from the database
        :return: extracted data from the dataset as a pandas DataFrame
        """
        file_path = self.config["path"]
        if self.__csv:
            return self.spark.read.csv(file_path, header=True)
        else:
            return s_pd.read_sql(table_name, self.config["path"])


class ChEMBLExtractor(Extractor):
    """
    Extractor class to extract data from ChEMBL dataset
    """

    def __init__(self, path, spark: SparkSession):
        self.conn = sqlite3.connect(path)
        super().__init__({"path": path}, spark)

    @logger
    def extract(self, table_name=None) -> DataFrame:
        """
        Extract method to extract data from ChEMBL dataset
        :param table_name: the table name to extract data from the database
        :return: extracted data from the dataset as a pandas DataFrame
        """
        return s_pd.read_sql(table_name, self.config["path"])


class ParquetExtractor(Extractor):
    """
    Extractor class to extract data from Parquet file
    """

    def __init__(self, path, spark: SparkSession):
        super().__init__({"path": path}, spark)

    @logger
    def extract(self) -> DataFrame:
        """
        Extract method to extract data from Parquet file
        :return: extracted data from the file as a pandas DataFrame
        """
        return self.spark.read.parquet(self.config["path"])
