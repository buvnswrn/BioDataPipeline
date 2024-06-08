import pandas as pd
from pydantic import BaseModel


class GeneralInfo(BaseModel):
    np_id: str
    pref_name: str
    iupac_name: str
    chembl_id: str
    pubchem_cid: int
    num_of_organism: int
    num_of_target: int
    num_of_activity: int
    if_has_Quantity: bool


class Activities(BaseModel):
    np_id: str
    target_id: str
    activity_type_grouped: str
    activity_relation: str
    activity_type: str
    activity_value: float
    activity_units: str
    assay_organism: str
    assay_tax_id: int  # this can be extracted out with assay_organism id.
    # Count in database - 958866 vs 3047 (958866+9588660 vs 958866+3047+30470 = 9.55143 MB saved)
    assay_strain: str
    assay_tissue: str
    assay_cell_type: str
    ref_id: str
    ref_type: str  # this can be extracted out with ref_id.
    # Count in database - 958866 vs 134741 (9588660+9588660 vs 958866+1347410+1347410 = 3.653686 MB saved)
    # Total 13.205116 MB saved (11% of the original size - 86.1 MB)


class SpeciesInfo(BaseModel):
    org_id: str
    org_name: str
    org_tax_level: str
    org_tax_id: int
    subspecies_tax_id: str
    subspecies_name: str
    species_tax_id: int
    species_name: str
    genus_tax_id: int
    genus_name: str
    family_tax_id: int
    family_name: str
    kingdom_tax_id: int
    kingdom_name: str
    superkingdom_tax_id: int
    superkingdom_name: str


class SpeciesPair(BaseModel):
    src_org_pair: str
    org_id: str
    np_id: str
    new_cp_found: bool
    org_isolation_part: str
    org_collect_location: str
    org_collect_time: str
    ref_type: str
    ref_id: str
    ref_id_type: str
    ref_url: str


class StructureInfo(BaseModel):
    np_id: str
    InChI: str
    InChIKey: str
    SMILES: str


class TargetInfo(BaseModel):
    target_id: str
    target_type: str
    target_name: str
    target_organism_tax_id: int
    target_organism: str
    uniprot_id: str


activities = {
    "np_id": pd.StringDtype,
    "target_id": pd.StringDtype,
    "activity_type_grouped": pd.StringDtype,
    "activity_relation": pd.StringDtype,
    "activity_type": pd.StringDtype,
    "activity_value": pd.Float64Dtype,
    "activity_units": pd.StringDtype,
    "assay_organism": pd.StringDtype,
    "assay_tax_id": pd.Int64Dtype,
    "assay_strain": pd.StringDtype,
    "assay_tissue": pd.StringDtype,
    "assay_cell_type": pd.StringDtype,
    "ref_id": pd.StringDtype,
    "ref_id_type": pd.StringDtype
}
general_info = {
    "np_id": pd.StringDtype,
    "pref_name": pd.StringDtype,
    "iupac_name": pd.StringDtype,
    "chembl_id": pd.StringDtype,
    "pubchem_cid": pd.StringDtype,
    "num_of_organism": pd.Int64Dtype,
    "num_of_target": pd.Int64Dtype,
    "num_of_activity": pd.Int64Dtype,
    "if_has_Quantity": pd.StringDtype
}
species_info = {
    "org_id": pd.StringDtype,
    "org_name": pd.StringDtype,
    "org_tax_level": pd.StringDtype,
    "org_tax_id": pd.Int64Dtype,
    "subspecies_tax_id": pd.StringDtype,
    "subspecies_name": pd.StringDtype,
    "species_tax_id": pd.Int64Dtype,
    "species_name": pd.StringDtype,
    "genus_tax_id": pd.Int64Dtype,
    "genus_name": pd.StringDtype,
    "family_tax_id": pd.Int64Dtype,
    "family_name": pd.StringDtype,
    "kingdom_tax_id": pd.Int64Dtype,
    "kingdom_name": pd.StringDtype,
    "superkingdom_tax_id": pd.Int64Dtype,
    "superkingdom_name": pd.StringDtype
}
species_pair = {
    "src_org_pair": pd.StringDtype,
    "org_id": pd.StringDtype,
    "np_id": pd.StringDtype,
    "new_cp_found": pd.StringDtype,
    "org_isolation_part": pd.StringDtype,
    "org_collect_location": pd.StringDtype,
    "org_collect_time": pd.StringDtype,
    "ref_type": pd.StringDtype,
    "ref_id": pd.StringDtype,
    "ref_id_type": pd.StringDtype,
    "ref_url": pd.StringDtype
}
structure_info = {
    "np_id": pd.StringDtype,
    "InChI": pd.StringDtype,
    "InChIKey": pd.StringDtype,
    "SMILES": pd.StringDtype
}
target_info = {
    "target_id": pd.StringDtype,
    "target_type": pd.StringDtype,
    "target_name": pd.StringDtype,
    "target_organism_tax_id": pd.Int64Dtype,
    "target_organism": pd.StringDtype,
    "uniprot_id": pd.StringDtype
}

