"""
file_io.py
----------
Handles saving processed data and reports to files in three formats:
.txt (human-readable), .csv (spreadsheet-friendly), and .json (machine-readable).

Satisfies the File I/O requirement of the project.
Includes basic error handling for invalid paths and write failures.
"""

import csv
import json


def save_report_txt(filename, records, title="Report"):
    """
    Writes a plain-text summary of a list of DiseaseRecord objects.

    Returns True on success, False on failure.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 60 + "\n")
            f.write(f"{title}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Total records: {len(records)}\n\n")

            for i, r in enumerate(records, start=1):
                f.write(f"{i}. {r}\n")

        print(f"  Report written to: {filename}")
        return True

    except (OSError, PermissionError) as e:
        print(f"  ERROR: could not write '{filename}': {e}")
        return False


def save_report_csv(filename, records):
    """
    Writes a list of records to a CSV file.
    Columns: year, state, topic, question, stratification,
             value, unit, value_type.
    """
    try:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "year", "state", "topic", "question",
                "stratification", "value", "unit", "value_type"
            ])
            for r in records:
                writer.writerow([
                    r.year, r.state, r.topic, r.question,
                    r.stratification, r.data_value,
                    r.data_value_unit, r.data_value_type,
                ])

        print(f"  CSV written to: {filename}")
        return True

    except (OSError, PermissionError) as e:
        print(f"  ERROR: could not write '{filename}': {e}")
        return False


def save_report_json(filename, records):
    """
    Writes a list of records to a JSON file (one big list of dicts).
    Uses the to_dict() method we defined on DiseaseRecord.
    """
    try:
        data = [r.to_dict() for r in records]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)

        print(f"  JSON written to: {filename}")
        return True

    except (OSError, PermissionError, TypeError) as e:
        print(f"  ERROR: could not write '{filename}': {e}")
        return False


def save_statistics(filename, stats_dict, title="Statistics"):
    """
    Writes a stats dictionary (from analysis.basic_statistics) to a text file.
    """
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{title}\n")
            f.write("-" * len(title) + "\n")
            for key, value in stats_dict.items():
                if isinstance(value, float):
                    f.write(f"{key:<10} : {value:.4f}\n")
                else:
                    f.write(f"{key:<10} : {value}\n")

        print(f"  Statistics written to: {filename}")
        return True

    except (OSError, PermissionError) as e:
        print(f"  ERROR: could not write '{filename}': {e}")
        return False
