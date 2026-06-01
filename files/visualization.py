"""
visualization.py
----------------
Matplotlib chart functions. The project requires at least two
visualisations; this module provides five so the user can pick
from the menu.

Every chart has a title and axis labels (project requirement).
"""

import matplotlib.pyplot as plt


def bar_chart_top_states(state_means, topic_label, top_n=10):
    """
    Bar chart: top N states by average indicator value.

    Parameters:
        state_means -- pandas Series indexed by state name
        topic_label -- string used in the chart title
        top_n       -- how many states to show
    """
    top = state_means.head(top_n)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(top.index, top.values, color="steelblue", edgecolor="black")

    ax.set_title(f"Top {top_n} States by Average Value — {topic_label}")
    ax.set_xlabel("State")
    ax.set_ylabel("Average value")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def line_chart_over_years(year_means, topic_label):
    """
    Line chart showing how the average value changed over time.

    Parameters:
        year_means -- pandas Series indexed by year
        topic_label -- topic shown in the title
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(year_means.index, year_means.values,
            marker="o", color="darkorange", linewidth=2)

    ax.set_title(f"Average Value Over Time — {topic_label}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average value")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def histogram_of_values(records, topic_label, bins=30):
    """
    Histogram showing how often each value range appears.
    Useful for understanding the distribution of the indicator.
    """
    values = [r.data_value for r in records]
    if not values:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(values, bins=bins, color="seagreen",
            edgecolor="black", alpha=0.8)

    ax.set_title(f"Distribution of Values — {topic_label}")
    ax.set_xlabel("Value")
    ax.set_ylabel("Number of records")
    plt.tight_layout()
    plt.show()


def pie_chart_topic_share(topic_counts, top_n=8):
    """
    Pie chart of the top N topics by record count.
    Smaller topics are grouped into "Other" so the chart stays readable.
    """
    if len(topic_counts) > top_n:
        top = topic_counts.head(top_n)
        other = topic_counts.iloc[top_n:].sum()
        # Append 'Other' bucket
        top = top.copy()
        top["Other"] = other
    else:
        top = topic_counts

    fig, ax = plt.subplots(figsize=(9, 9))
    ax.pie(top.values, labels=top.index, autopct="%1.1f%%",
           startangle=90)
    ax.set_title("Share of Records by Topic")
    plt.tight_layout()
    plt.show()


def scatter_year_vs_value(records, topic_label, max_points=2000):
    """
    Scatter plot of year vs value. Useful for spotting trends or outliers.

    Limits to max_points so the plot doesn't get unreadable when the
    full dataset has hundreds of thousands of rows.
    """
    if not records:
        print("No data to plot.")
        return

    sample = records[:max_points]
    years = [r.year for r in sample]
    values = [r.data_value for r in sample]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(years, values, alpha=0.4, color="crimson", s=15)

    ax.set_title(f"Year vs Value — {topic_label}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Value")
    ax.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    plt.show()
