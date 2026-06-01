"""
analysis.py
-----------
Searching, sorting, filtering, and basic statistics on the dataset.

Demonstrates:
  - Lists, tuples and dictionaries (data structures requirement)
  - Search / sort / filter operations (project requirement)
  - Pandas grouping and aggregation (Pandas requirement)
"""

import pandas as pd


# ─────────────────────────────────────────────────────────────
# SEARCH / FILTER (operate on lists of DiseaseRecord objects)
# ─────────────────────────────────────────────────────────────

def search_by_state(records, state_query):
    """
    Returns all DiseaseRecord objects whose state name contains the
    search text (case-insensitive). Useful for "find all entries for Texas".
    """
    state_query = state_query.lower().strip()
    matches = []
    for r in records:
        if state_query in r.state.lower():
            matches.append(r)
    return matches


def search_by_topic(records, topic_query):
    """Same idea but on the Topic field (e.g. 'Diabetes', 'Cancer')."""
    topic_query = topic_query.lower().strip()
    return [r for r in records if topic_query in r.topic.lower()]


def filter_by_year_range(records, year_start, year_end):
    """Returns records whose year is between year_start and year_end inclusive."""
    return [r for r in records if year_start <= r.year <= year_end]


def filter_by_value_threshold(records, min_value=None, max_value=None):
    """
    Returns records whose data_value is within [min_value, max_value].
    Either bound can be left as None to mean "no lower/upper limit".
    """
    out = []
    for r in records:
        if min_value is not None and r.data_value < min_value:
            continue
        if max_value is not None and r.data_value > max_value:
            continue
        out.append(r)
    return out


# ─────────────────────────────────────────────────────────────
# SORT
# ─────────────────────────────────────────────────────────────

def sort_records(records, key="value", descending=True):
    """
    Sorts a list of records. The `key` argument selects which
    attribute to sort by: "value", "year", "state", or "topic".
    """
    key_map = {
        "value": lambda r: r.data_value,
        "year":  lambda r: r.year,
        "state": lambda r: r.state,
        "topic": lambda r: r.topic,
    }
    if key not in key_map:
        raise ValueError(f"Unknown sort key: {key}")
    return sorted(records, key=key_map[key], reverse=descending)


def top_n(records, n=10, by="value", descending=True):
    """Returns the first n records after sorting."""
    return sort_records(records, key=by, descending=descending)[:n]


# ─────────────────────────────────────────────────────────────
# STATISTICS (operate on list of DiseaseRecord)
# ─────────────────────────────────────────────────────────────

def basic_statistics(records):
    """
    Computes mean, median, min, max, and count from a list of records.

    Returns a dictionary so the caller can pick whichever stats it needs.
    """
    if not records:
        return {"count": 0, "mean": 0, "median": 0,
                "min": 0, "max": 0}

    values = [r.data_value for r in records]
    values_sorted = sorted(values)
    n = len(values)

    # Mean = sum / count
    mean = sum(values) / n

    # Median = middle value, or average of two middle values
    if n % 2 == 1:
        median = values_sorted[n // 2]
    else:
        median = (values_sorted[n // 2 - 1] + values_sorted[n // 2]) / 2

    return {
        "count": n,
        "mean": mean,
        "median": median,
        "min": min(values),
        "max": max(values),
    }


# ─────────────────────────────────────────────────────────────
# PANDAS AGGREGATIONS (DataFrame requirement)
# ─────────────────────────────────────────────────────────────

def average_value_by_state(df, topic=None):
    """
    Pandas DataFrame operation: group by state, compute mean value.

    If a topic is given, filter to that topic first. Returns a Series
    indexed by state, sorted highest to lowest.
    """
    work = df.copy()
    if topic:
        work = work[work["topic"].str.contains(topic, case=False, na=False)]

    grouped = work.groupby("state")["value"].mean()
    return grouped.sort_values(ascending=False)


def average_value_by_year(df, topic=None):
    """Time-series style aggregation: average value per year."""
    work = df.copy()
    if topic:
        work = work[work["topic"].str.contains(topic, case=False, na=False)]
    return work.groupby("year")["value"].mean().sort_index()


def topic_counts(df):
    """How many records exist per Topic. Returns a Pandas Series."""
    return df["topic"].value_counts()


def unique_states(df):
    """List of unique states/locations as a Python list."""
    return sorted(df["state"].dropna().unique().tolist())


def unique_topics(df):
    """List of unique topics as a Python list."""
    return sorted(df["topic"].dropna().unique().tolist())
