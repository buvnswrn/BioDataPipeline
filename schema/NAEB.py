import pandas as pd

sources = {
    "id": pd.Int64Dtype,
    "refcode": pd.StringDtype,
    "type": pd.StringDtype,
    "fulltext": pd.StringDtype,
    "address": pd.StringDtype,
    "author": pd.StringDtype,
    "booktitle": pd.StringDtype,
    "comment": pd.StringDtype,
    "edition": pd.StringDtype,
    "editor": pd.StringDtype,
    "journal": pd.StringDtype,
    "month": pd.StringDtype,
    "note": pd.StringDtype,
    "number": pd.StringDtype,
    "pages": pd.StringDtype,
    "publisher": pd.StringDtype,
    "school": pd.StringDtype,
    "title": pd.StringDtype,
    "url": pd.StringDtype,
    "volume": pd.StringDtype,
    "year": pd.Int64Dtype
}

species = {
    "id": pd.Int64Dtype,
    "name": pd.StringDtype,
    "common_names": pd.StringDtype,
    "usda_code": pd.StringDtype,
    "family": pd.StringDtype,
    "family_apg": pd.StringDtype
}

tribes = {
    "id": pd.Int64Dtype,
    "name": pd.StringDtype
}

use_categories = {
    "id": pd.Int64Dtype,
    "name": pd.StringDtype
}

use_subcategories = {
    "id": pd.Int64Dtype,
    "parent": pd.Int64Dtype,
    "name": pd.StringDtype
}

uses = {
    "id": pd.Int64Dtype,
    "species": pd.Int64Dtype,
    "tribe": pd.Int64Dtype,
    "source": pd.Int64Dtype,
    "pageno": pd.StringDtype,
    "use_category": pd.Int64Dtype,
    "use_subcategory": pd.Int64Dtype,
    "notes": pd.StringDtype,
    "rawsource": pd.StringDtype
}