"""
data_loader.py
--------------
Handles loading the CDC Chronic Disease Indicators CSV file.

Uses Pandas (project requirement) to read and clean the data, then
converts each row into a DiseaseRecord object so the rest of the
program can work with objects instead of raw DataFrame rows.
"""

import pandas as pd
from disease_record import DiseaseRecord


# Columns we actually care about from the 34-column raw CSV.
# Keeping only these makes the DataFrame much smaller and faster.
USEFUL_COLUMNS = [
    "YearStart",
    "LocationDesc",
    "Topic",
    "Question",
    "DataValueUnit",
    "DataValueType",
    "DataValueAlt",
    "Stratification1",
]


def load_dataframe(csv_path):
    """
    Reads the CSV file with Pandas and returns a cleaned DataFrame.

    Cleaning steps:
      1. Read the file (low_memory=False prevents column type warnings).
      2. Keep only useful columns.
      3. Drop rows where the numeric value is missing.
      4. Rename columns to shorter, friendlier names.

    Raises FileNotFoundError if the file does not exist.
    """
    try:
        df = pd.read_csv(csv_path, low_memory=False)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Could not find dataset file: {csv_path}\n"
            f"Please make sure the CSV is in the project folder."
        )

    # Keep only the columns we need (intersection in case of variants)
    available = [c for c in USEFUL_COLUMNS if c in df.columns]
    df = df[available].copy()

    # DataValueAlt is the numeric form. Drop rows without a number.
    if "DataValueAlt" in df.columns:
        df = df.dropna(subset=["DataValueAlt"])

    # Drop rows missing state — needed for almost every analysis
    if "LocationDesc" in df.columns:
        df = df.dropna(subset=["LocationDesc"])

    # Rename to short friendly names used everywhere else
    df = df.rename(columns={
        "YearStart": "year",
        "LocationDesc": "state",
        "Topic": "topic",
        "Question": "question",
        "DataValueUnit": "unit",
        "DataValueType": "value_type",
        "DataValueAlt": "value",
        "Stratification1": "stratification",
    })

    # Reset row indices after the dropna calls
    df = df.reset_index(drop=True)
    return df


def dataframe_to_records(df):
    """
    Converts a cleaned DataFrame into a list of DiseaseRecord objects.

    Returns:
        list of DiseaseRecord
    """
    records = []
    for _, row in df.iterrows():
        record = DiseaseRecord(
            year=int(row.get("year", 0)),
            state=row.get("state", ""),
            topic=row.get("topic", ""),
            question=row.get("question", ""),
            data_value=row.get("value", None),
            data_value_unit=row.get("unit", ""),
            data_value_type=row.get("value_type", ""),
            stratification=row.get("stratification", ""),
        )
        if record.is_valid():
            records.append(record)
    return records


def load_records(csv_path):
    """
    Convenience function: read CSV and return both the DataFrame
    AND the list of DiseaseRecord objects.

    Returns:
        (DataFrame, list_of_DiseaseRecord)
    """
    df = load_dataframe(csv_path)
    records = dataframe_to_records(df)
    return df, records
