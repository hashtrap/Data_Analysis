
## This module will deal with the sorting and filtering of the data.
## It prepares the data so that the visualisation can be achieved


# ─────────────────────────────────────────────────────────────
# SEARCH / FILTER (operate on lists of DiseaseRecord objects)
# ─────────────────────────────────────────────────────────────

def search_by_state(records, state_query):

    state_query = state_query.lower().strip()
    matches=[]
    for r in records:
        if state_query in r.state.lower():
            matches.append(r)
    return matches


def search_by_topic(records,topic_query):

    topic_query = topic_query.lower().strip()
    matches=[]

    for r in records:
        if topic_query in r.topic.lower():
            matches.append(r)
    return matches

def filter_by_year_range(records, year_start,year_end):
    out = []
    for r in records:
        if year_start <= r.year <= year_end:
            out.append(r)
    return out

def filter_by_value_threshold(records,min_value=None,max_value=None):

    out=[]
    for r in records:
        if min_value is not None and r.data_value < min_value:
            continue
        if max_value is not None and r.data_value > max_value:
            continue
        out.append(r)
    return out

# ─────────────────────────────────────────────────────────────
# SORTING
# ─────────────────────────────────────────────────────────────

def sort_records(records,key="value",descending=True):

    key_map={
            "value": lambda r: r.data_value,
            "year": lambda r: r.year,
            "state": lambda r: r.state,
            "topic": lambda r: r.topic,
        }

    if key not in key_map:
        raise ValueError(f"Unknown sort key: {key}")
    return sorted(records, key=key_map[key],reverse=descending)

def top_n(records, n=10, by="value",descending=True ):

    return sort_records(records,key=by,descending=descending)[:n]

# ─────────────────────────────────────────────────────────────
# STATISTICS (operate on list of DiseaseRecord)
# ─────────────────────────────────────────────────────────────

def basic_statistics(records):

    if not records:
        return {"count":0,"mean":0,"median":0, "min":0,"max":0}

    values=[r.data_value for r in records]
    values_sorted=sorted(values)
    n=len(values)

    mean=sum(values)/n

    if n%2==1:
        median=values_sorted[n//2]
    else:
        median=(values_sorted[n//2-1] + values_sorted[n//2])/2

    return {
        "count": n,
        "mean": mean,
        "median": median,
        "min": min(values),
        "max": max(values),
    }

# ─────────────────────────────────────────────────────────────
# PANDAS ACTIONS
# ─────────────────────────────────────────────────────────────

def average_value_by_state(df,topic=None):
    
    work=df.copy()
    if topic:
        work=work[work["topic"].str.contains(topic,case=False,na=False)]
    grouped=work.groupby("state")["value"].mean()
    return grouped.sort_values(ascending=False)

def average_value_by_year(df,topic=None):
    work=df.copy()
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