import sqlite3
from graphdatascience import GraphDataScience
from neo4j import GraphDatabase

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


def create_nodes(tx, node_label, properties):
    node_properties = ", ".join([f"{key}: ${key}" for key in properties.keys()])
    query = f"MERGE (n: {node_label} {{{node_properties}}})"
    tx.run(query, **properties)


class Neo4jLoader(Loader):
    """
    Loader class to load data to Neo4j database
    """
    create_graph_query = """
    CREATE (n:{label} {props})
    """

    def __init__(self, uri, user, password):
        super().__init__()
        self.uri = uri
        self.user = user
        self.password = password
        self.gds = GraphDataScience(self.uri, (self.user, self.password))
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    @logger
    def load(self, data: pd.DataFrame, graph_name: str) -> bool:
        """
        Load method to load data to the Neo4j database
        :param graph_name: the graph name to load the data
        :param data: the dataframe to load
        :return: True if the data is loaded successfully else False
        """
        test = pd.DataFrame({
            "nodeId": [1, 2, 3],
            "target": ["Test2", "Test8", "Test9"],
            "weight": [10, 20, 30]
        })
        nodes = pd.DataFrame().assign(
            nodeId=test['nodeId'].replace('NPT', '', regex=True).astype(int),
            labels='Target',
            subject=test['nodeId'].replace('NPT', '', regex=True).astype(int),
            features=test.drop(columns=['nodeId']).apply(list, axis=1)
        )
        df = data.fillna('').astype(str)
        with self.driver.session() as session:
            for index, row in df.iterrows():
                properties = row.to_dict()
                session.write_transaction(create_nodes, 'Target', properties)
        return True
