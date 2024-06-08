from src.decorator.LoggerDecoratorFactory import LoggerDecoratorFactory

bronze_logger = LoggerDecoratorFactory("Source2Landing (Bronze Layer)").log_time
silver_logger = LoggerDecoratorFactory("Landing2Curated (Silver Layer)").log_time
gold_logger = LoggerDecoratorFactory("Curated2Consumable (Gold Layer)").log_time


class ETLPipeline:
    """
    Base class for ETL pipeline
    """

    def __init__(self, extractors, transformers, loaders):
        """
        Constructor for ETLPipeline
        :param extractors: the extractors to extract the data
        :param transformers: the transformers to transform the data
        :param loaders: the loaders to load the data
        """
        self.extractors = extractors
        self.transformers = transformers
        self.loaders = loaders

    def run(self, file_paths):
        raise NotImplementedError("Run method not implemented")


class SourceToLandingPipeline(ETLPipeline):
    @bronze_logger
    def run(self, table_names: list) -> bool:
        """
        Run the ETL pipeline for source to landing (Bronze Layer)
        :param table_names: the table names to load the data
        :return: True if the data is loaded successfully else False
        """
        for table_name, extractor in zip(table_names, self.extractors):
            data = extractor.extract()
            for transformer in self.transformers:
                data = transformer.transform(data)
            for loader in self.loaders:
                if not loader.load(data, table_name):
                    return False
        return True


class LandingToCuratedPipeline(ETLPipeline):
    @silver_logger
    def run(self, file_paths: list):
        """
        Run the ETL pipeline for landing to curated (Silver Layer)
        :param file_paths: the file paths to extract the data
        :return: True if the data is loaded successfully else False
        """
        for file_path, extractor in zip(file_paths, self.extractors):
            data = extractor.extract()
            for transformer in self.transformers:
                data = transformer.transform(data)
            for loader in self.loaders:
                loader.load(data)


class CuratedToConsumablePipeline(ETLPipeline):
    @gold_logger
    def run(self, file_paths: list):
        """
        Run the ETL pipeline for curated to consumable (Gold Layer)
        :param file_paths: the file paths to extract the data
        :return: True if the data is loaded successfully else False
        """
        for file_path, extractor in zip(file_paths, self.extractors):
            data = extractor.extract()
            for transformer in self.transformers:
                data = transformer.transform(data)
            for loader in self.loaders:
                loader.load(data)
