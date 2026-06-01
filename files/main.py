"""
main.py
-------
Entry point for the Chronic Disease Indicators analysis project.

Pulls together every other module via a text menu so the user can
load data, search, filter, sort, view statistics, plot charts,
and export reports — all from one place.

Run with:    python3 main.py
"""

import os

from data_loader import load_records
from disease_record import DiseaseRecord
import analysis
import visualization as viz
import file_io
import utils


# Default file name. Can be overridden when the user starts the program.
DEFAULT_CSV = "U_S__Chronic_Disease_Indicators.csv"


# ─────────────────────────────────────────────────────────────
# MENU PRINTING
# ─────────────────────────────────────────────────────────────

def print_main_menu():
    print()
    print("============================================")
    print("  Chronic Disease Indicators — Main Menu")
    print("============================================")
    print("  1. Show dataset summary")
    print("  2. Search by state")
    print("  3. Search by topic")
    print("  4. Filter by year range")
    print("  5. Filter by value threshold")
    print("  6. Top N records (sorted)")
    print("  7. Basic statistics")
    print("  8. Visualizations")
    print("  9. Save report to file")
    print("  0. Exit")
    print("============================================")


def print_viz_menu():
    print()
    print("--- Visualisations -------------------------")
    print("  1. Bar chart: top states (by topic)")
    print("  2. Line chart: average value over years")
    print("  3. Histogram: value distribution")
    print("  4. Pie chart: share of records by topic")
    print("  5. Scatter: year vs value")
    print("  0. Back")
    print("--------------------------------------------")


# ─────────────────────────────────────────────────────────────
# MENU ACTIONS
# ─────────────────────────────────────────────────────────────

def show_summary(df, records):
    """Quick overview of what was loaded."""
    print()
    print(f"  Total valid records loaded : {len(records)}")
    print(f"  Years covered              : "
          f"{df['year'].min()} - {df['year'].max()}")
    print(f"  Unique states / locations  : {df['state'].nunique()}")
    print(f"  Unique topics              : {df['topic'].nunique()}")
    print()
    print("  Top 5 topics by record count:")
    for topic, count in analysis.topic_counts(df).head(5).items():
        print(f"    - {topic}: {count}")


def action_search_state(records):
    query = utils.ask_text("  Enter state name (or part of it): ")
    results = analysis.search_by_state(records, query)
    print(f"\n  Found {len(results)} matching records.")
    utils.print_records_table(results)
    return results


def action_search_topic(records):
    query = utils.ask_text("  Enter topic (e.g. Diabetes, Cancer): ")
    results = analysis.search_by_topic(records, query)
    print(f"\n  Found {len(results)} matching records.")
    utils.print_records_table(results)
    return results


def action_filter_year(records):
    y1 = utils.ask_int("  Start year: ", min_value=1900, max_value=2100)
    y2 = utils.ask_int("  End year:   ", min_value=y1, max_value=2100)
    results = analysis.filter_by_year_range(records, y1, y2)
    print(f"\n  {len(results)} records in {y1}–{y2}.")
    utils.print_records_table(results)
    return results


def action_filter_value(records):
    print("  Press Enter to leave a bound blank.")
    lo = utils.ask_float("  Minimum value: ", allow_blank=True)
    hi = utils.ask_float("  Maximum value: ", allow_blank=True)
    results = analysis.filter_by_value_threshold(records, lo, hi)
    print(f"\n  {len(results)} records match the value range.")
    utils.print_records_table(results)
    return results


def action_top_n(records):
    n = utils.ask_int("  How many records (N)? ", min_value=1, max_value=200)
    print("  Sort by: 1=value  2=year  3=state  4=topic")
    choice = utils.ask_int("  Choice: ", min_value=1, max_value=4)
    desc = utils.ask_yes_no("  Descending order? (y/n) ")
    key_map = {1: "value", 2: "year", 3: "state", 4: "topic"}
    results = analysis.top_n(records, n=n, by=key_map[choice], descending=desc)
    utils.print_records_table(results, max_rows=n)
    return results


def action_statistics(records):
    stats = analysis.basic_statistics(records)
    print()
    print("  Basic statistics for the current record set:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"    {key:<8} : {value:.3f}")
        else:
            print(f"    {key:<8} : {value}")
    if utils.ask_yes_no("\n  Save statistics to a file? (y/n) "):
        fname = utils.ask_text("  Filename (e.g. stats.txt): ")
        file_io.save_statistics(fname, stats)


def action_visualizations(df, records):
    while True:
        print_viz_menu()
        choice = utils.ask_int("  Choice: ", min_value=0, max_value=5)

        if choice == 0:
            return

        # All charts (except pie) accept an optional topic filter
        topic = ""
        if choice in (1, 2, 3, 5):
            topic = utils.ask_text(
                "  Filter to a topic? (blank = all data): ",
                allow_blank=True
            )

        topic_label = topic if topic else "All Topics"

        if choice == 1:
            state_means = analysis.average_value_by_state(df, topic or None)
            viz.bar_chart_top_states(state_means, topic_label)

        elif choice == 2:
            year_means = analysis.average_value_by_year(df, topic or None)
            viz.line_chart_over_years(year_means, topic_label)

        elif choice == 3:
            filtered = (analysis.search_by_topic(records, topic)
                        if topic else records)
            viz.histogram_of_values(filtered, topic_label)

        elif choice == 4:
            counts = analysis.topic_counts(df)
            viz.pie_chart_topic_share(counts)

        elif choice == 5:
            filtered = (analysis.search_by_topic(records, topic)
                        if topic else records)
            viz.scatter_year_vs_value(filtered, topic_label)


def action_save_report(records):
    if not records:
        print("  No records to save.")
        return

    print("  Save format: 1=txt  2=csv  3=json")
    fmt = utils.ask_int("  Choice: ", min_value=1, max_value=3)
    fname = utils.ask_text("  Filename (with extension): ")

    if fmt == 1:
        file_io.save_report_txt(fname, records, title="Chronic Disease Report")
    elif fmt == 2:
        file_io.save_report_csv(fname, records)
    elif fmt == 3:
        file_io.save_report_json(fname, records)


# ─────────────────────────────────────────────────────────────
# PROGRAM ENTRY POINT
# ─────────────────────────────────────────────────────────────

def get_csv_path():
    """Ask the user where the CSV lives, falling back to the default."""

    print("Welcome to the Chronic Disease Indicators analyser.")
    path = input(
        f"  Path to CSV (Enter for '{DEFAULT_CSV}'): "
    ).strip()
    return path if path else DEFAULT_CSV


def main():
    csv_path = get_csv_path()

    if not os.path.exists(csv_path):
        print(f"  ERROR: file not found: {csv_path}")
        return

    print(f"\n  Loading {csv_path} ... (this may take a few seconds)")

    try:
        df, records = load_records(csv_path)
    except Exception as e:
        print(f"  ERROR while loading: {e}")
        return

    print(f"  Loaded {len(records)} valid records.")

    # `current_records` is the working set — search/filter results
    # become the new working set so the user can chain operations.
    current_records = records

    while True:
        print_main_menu()
        print(f"  Current working set : {len(current_records)} records")
        choice = utils.ask_int("  Choice: ", min_value=0, max_value=8)

        if choice == 0:
            print("\n  Goodbye!")
            break
        elif choice == 1:
            show_summary(df, records)
        elif choice == 2:
            current_records = action_search_state(records)
        elif choice == 3:
            current_records = action_search_topic(records)
        elif choice == 4:
            current_records = action_filter_year(current_records)
        elif choice == 5:
            current_records = action_filter_value(current_records)
        elif choice == 6:
            current_records = action_top_n(current_records)
        elif choice == 7:
            action_statistics(current_records)
        elif choice == 8:
            action_visualizations(df, current_records)
        elif choice == 9:
            action_save_report(current_records)


if __name__ == "__main__":
    main()
