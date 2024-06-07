import sqlite3

import pandas as pd


class Extractor:
    def __init__(self, config: dict):
        self.config = config

    def extract(self, data) -> pd.DataFrame:
        raise NotImplementedError


class NPASSExtractor(Extractor):
    def __init__(self, path):
        super().__init__({"path": path})

    def extract(self, data) -> pd.DataFrame:
        file_path = self.config["path"]
        return pd.read_csv(file_path, sep='\t', encoding="ISO-8859-1")


class NAEBExtractor(Extractor):
    def __init__(self, path, csv=True):
        if not csv:
            self.conn = sqlite3.connect(path)
        super().__init__({"path": path, "csv": csv})

    def extract(self, table_name=None) -> pd.DataFrame:
        file_path = self.config["path"]
        if self.config["csv"]:
            return pd.read_csv(file_path)
        else:
            return pd.read_sql(table_name, self.conn)


class ChEMBLExtractor(Extractor):
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        super().__init__({"path": path})

    def extract(self, table_name=None) -> pd.DataFrame:
        return pd.read_sql(table_name, self.conn)
