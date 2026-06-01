import pandas as pd
import os
import sys

from Disease_Record import *

File_Path = "..\\Data\\U.S._Chronic_Disease_Indicators.csv"

COLUMNS = [
    "YearStart",
    "LocationDesc",
    "Topic",
    "Question",
    "DataValueUnit",
    "DataValueType",
    "DataValueAlt",
    "Stratification1",
]


def verify_file(path=File_Path) -> bool:

    if not (os.path.exists(path)):
        return False
    else:
        return True


def get_file(path=File_Path):

    if verify_file(path):
        return path
    else:
        sys.exit("Programm shut down because file doesn't exist :)")


def load_dataframe(csv):

    if not verify_file(csv):
        sys.exit("Programm shut down because file doesn't exist :)")

    data_frame = pd.read_csv(csv, low_memory=False)

    needed_columns = [c for c in COLUMNS if c in data_frame.columns]
    data_frame = data_frame[needed_columns].copy()



    ## We drop columns that have NA in them as they mess up the data analysis
    if "DataValueAlt" in data_frame.columns:
        data_frame = data_frame.dropna(subset=["DataValueAlt"])

    # Drop rows missing state — needed for almost every analysis
    if "LocationDesc" in data_frame.columns:
        data_frame = data_frame.dropna(subset=["LocationDesc"])

    data_frame = data_frame.rename(columns={
        "YearStart": "year",
        "LocationDesc": "state",
        "Topic": "topic",
        "Question": "question",
        "DataValueUnit": "unit",
        "DataValueType": "value_type",
        "DataValueAlt": "value",
        "Stratification1": "stratification",
    })

    data_frame = data_frame.reset_index(drop=True)
    return data_frame


def dataframe_to_records(df):

    records = []

    for _, row in df.iterrows():
        record = Disease_Record(
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


def load_records(csv_path=None):

    path = csv_path if csv_path else File_Path
    df = load_dataframe(path)
    records = dataframe_to_records(df)
    return df, records



if __name__ == "__main__":
    get_file()