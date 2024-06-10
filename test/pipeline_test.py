import os
import time

import pandas as pd
from dotenv import load_dotenv

from schema.NAEB import sources, species, tribes, use_categories, use_subcategories, uses

load_dotenv()

from src.pipeline.ETLPipeline import SourceToLandingPipeline
from src.pipeline.Extractor import NPASSExtractor, ParquetExtractor, NAEBExtractor
from src.pipeline.Loader import SQLiteLoader, ParquetLoader, Neo4jLoader
from src.pipeline.Transformer import Transformer, BasicTransformer, Neo4jTransformer
from schema.NPASS import activities, general_info, species_pair, species_info, target_info, structure_info

npass_source_path = "../data/source/npass/txt/"
temp_name = "NPASSv2.0_download_naturalProducts_"
npass = {
    "activities": (npass_source_path + temp_name + "activities.txt", activities),
    "generalInfo": (npass_source_path + temp_name + "generalInfo.txt", general_info),
    "species_pair": (npass_source_path + temp_name + "species_pair.txt", species_pair),
    "speciesInfo": (npass_source_path + temp_name + "speciesInfo.txt", species_info),
    "targetInfo": (npass_source_path + temp_name + "targetInfo.txt", target_info),
    "structureInfo": (npass_source_path + temp_name + "structureInfo.txt", structure_info)
}

naeb_source_path = "../data/source/naeb_dump/csv/"
naeb = {
    "sources": (naeb_source_path + "sources.csv", sources),
    "species": (naeb_source_path + "species.csv", species),
    "tribes": (naeb_source_path + "tribes.csv", tribes),
    "use_categories": (naeb_source_path + "use_categories.csv", use_categories),
    "use_subcategories": (naeb_source_path + "use_subcategories.csv", use_subcategories),
    "uses": (naeb_source_path + "uses.csv", uses)
}


def test_source_to_landing_pipeline():
    for key, value in npass.items():
        path, schema = value
        source_to_landing_pipeline = SourceToLandingPipeline(
            extractors=[NPASSExtractor(path)],
            transformers=[Transformer(schema)],
            loaders=[ParquetLoader("../data/temp/bronze/landing_npass_")]
        )
        assert source_to_landing_pipeline.run([key]) is True


def test_source_to_landing_pipeline_naeb():
    for key, value in naeb.items():
        path, schema = value
        source_to_landing_pipeline = SourceToLandingPipeline(
            extractors=[NAEBExtractor(path, csv=True)],
            transformers=[Transformer(schema)],
            loaders=[ParquetLoader("../data/temp/bronze/landing_naeb_")]
        )
        assert source_to_landing_pipeline.run([key]) is True


def test_landing_to_curated_pipeline(name, data_dict):
    for key, value in data_dict.items():
        path, schema = value
        landing_to_curated_pipeline = SourceToLandingPipeline(
            extractors=[ParquetExtractor("../data/temp/bronze/landing_"+name+"_" + key + ".parquet")],
            transformers=[BasicTransformer(schema)],
            loaders=[ParquetLoader("../data/temp/silver/curated_"+name+"_")]
        )
        assert landing_to_curated_pipeline.run([key]) is True


def test_curated_to_consumable_pipeline():
    key = "targetInfo"
    landing_to_curated_pipeline = SourceToLandingPipeline(
        extractors=[ParquetExtractor("../data/temp/silver/curated_npass_" + key + ".parquet")],
        transformers=[Neo4jTransformer('target_id', 'target')],
        loaders=[Neo4jLoader(os.environ.get("NEO4J_URI"),
                             os.environ.get("NEO4J_USER"), os.environ.get("NEO4J_PASS"))]
    )
    assert landing_to_curated_pipeline.run([key]) is True


if __name__ == '__main__':
    start = time.time()
    test_source_to_landing_pipeline()
    end = time.time()
    print(f"Execution time: {end - start}")
    test_landing_to_curated_pipeline("npass", npass)
    end2 = time.time()
    print(f"Execution time: {end2 - end}")
    test_curated_to_consumable_pipeline()
    end3 = time.time()
    print(f"Execution time: {end3 - end2}")
    print("Total Execution time: ", end3 - start)
    print("Starting with NAEB dataset")
    start = time.time()
    test_source_to_landing_pipeline_naeb()
    end = time.time()
    print(f"Execution time: {end - start}")
    test_landing_to_curated_pipeline("naeb", naeb)
    end2 = time.time()
    print(f"Execution time: {end2 - end}")

