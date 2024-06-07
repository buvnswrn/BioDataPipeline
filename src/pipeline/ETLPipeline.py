
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
    def run(self, file_paths: list) -> bool:
        """
        Run the ETL pipeline for source to landing (Bronze Layer)
        :param file_paths: the file paths to extract the data
        :return: True if the data is loaded successfully else False
        """
        for file_path, extractor in zip(file_paths, self.extractors):
            data = extractor.extract()
            for loader in self.loaders:
                if not loader.load(data):
                    return False
        return True


class LandingToCuratedPipeline(ETLPipeline):
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
