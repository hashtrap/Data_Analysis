"""
disease_record.py
-----------------
Defines the DiseaseRecord class used to represent a single row of the
U.S. Chronic Disease Indicators dataset as an object.

This satisfies the OOP requirement of the project: one custom class
with attributes, methods, and a constructor.
"""


class DiseaseRecord:
    """
    Represents one chronic disease indicator measurement.

    Each row of the CDC dataset becomes one DiseaseRecord object
    with the most relevant fields stored as attributes.
    """

    def __init__(self, year, state, topic, question, data_value,
                 data_value_unit, data_value_type, stratification):
        # Basic identifying information
        self.year = year                          # int — e.g. 2019
        self.state = state                        # str — e.g. "Texas"
        self.topic = topic                        # str — e.g. "Diabetes"
        self.question = question                  # str — full question text
        self.stratification = stratification      # str — e.g. "Male", "Overall"

        # The actual measurement
        self.data_value = data_value              # float — the numeric value
        self.data_value_unit = data_value_unit    # str — "%", "cases per 1000", etc.
        self.data_value_type = data_value_type    # str — "Crude Prevalence", etc.

    def is_valid(self):
        """
        Returns True if this record has a usable numeric data value.
        Many rows in the CDC dataset are missing DataValueAlt, so we
        need to filter those out before doing maths on them.
        """
        if self.data_value is None:
            return False
        # Reject NaN (NaN is the only value not equal to itself)
        if self.data_value != self.data_value:
            return False
        return True

    def short_label(self):
        """Returns a short readable label, useful for chart axes."""
        return f"{self.state} ({self.year}) - {self.topic}"

    def __str__(self):
        """Human-readable text version of the record."""
        if self.is_valid():
            value_text = f"{self.data_value:.2f} {self.data_value_unit}"
        else:
            value_text = "no data"
        return (f"[{self.year}] {self.state} | {self.topic} | "
                f"{self.stratification} -> {value_text}")

    def __repr__(self):
        """Developer-facing representation, used by lists when printed."""
        return (f"DiseaseRecord(year={self.year}, state='{self.state}', "
                f"topic='{self.topic}', value={self.data_value})")

    def to_dict(self):
        """
        Converts the object to a plain dictionary.
        Used when exporting records to JSON.
        """
        return {
            "year": self.year,
            "state": self.state,
            "topic": self.topic,
            "question": self.question,
            "stratification": self.stratification,
            "data_value": self.data_value,
            "data_value_unit": self.data_value_unit,
            "data_value_type": self.data_value_type,
        }
