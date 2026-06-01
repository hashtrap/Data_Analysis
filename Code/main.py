import os
import File_Reader as fr
from Disease_Record import Disease_Record
import Data_Filter as df
import Plot_Maker as pm
import Sentinel as sn


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

def show_summary(data_frame, records):
    """Quick overview of what was loaded."""
    print()
    print(f"  Total valid records loaded : {len(records)}")
    print(f"  Years covered              : "
          f"{data_frame['year'].min()} - {data_frame['year'].max()}")
    print(f"  Unique states / locations  : {data_frame['state'].nunique()}")
    print(f"  Unique topics              : {data_frame['topic'].nunique()}")
    print()
    print("  Top 5 topics by record count:")
    for topic, count in df.topic_counts(data_frame).head(5).items():
        print(f"    - {topic}: {count}")


def action_search_state(records):
    query = sn.ask_text("  Enter state name (or part of it): ")
    results = df.search_by_state(records, query)
    print(f"\n  Found {len(results)} matching records.")
    sn.print_records_table(results)
    return results


def action_search_topic(records):
    query = sn.ask_text("  Enter topic (e.g. Diabetes, Cancer): ")
    results = df.search_by_topic(records, query)
    print(f"\n  Found {len(results)} matching records.")
    sn.print_records_table(results)
    return results


def action_filter_year(records):
    y1 = sn.ask_int("  Start year: ", min_value=1900, max_value=2100)
    y2 = sn.ask_int("  End year:   ", min_value=y1, max_value=2100)
    results = df.filter_by_year_range(records, y1, y2)
    print(f"\n  {len(results)} records in {y1}–{y2}.")
    sn.print_records_table(results)
    return results


def action_filter_value(records):
    print("  Press Enter to leave a bound blank.")
    lo = sn.ask_float("  Minimum value: ", allow_blank=True)
    hi = sn.ask_float("  Maximum value: ", allow_blank=True)
    results = df.filter_by_value_threshold(records, lo, hi)
    print(f"\n  {len(results)} records match the value range.")
    sn.print_records_table(results)
    return results


def action_top_n(records):

    number = sn.ask_int("  How many records (N)? ", min_value=1, max_value=200)
    print("  Sort by: 1=value  2=year  3=state  4=topic")
    choice = sn.ask_int("  Choice: ", min_value=1, max_value=4)
    desc = sn.ask_yes_no("  Descending order? (y/n) ")
    key_map = {1: "value", 2: "year", 3: "state", 4: "topic"}
    results = df.top_n(records, n=number, by=key_map[choice], descending=desc)
    sn.print_records_table(results, max_rows=number)
    return results


def action_statistics(records):
    stats = df.basic_statistics(records)
    print()
    print("  Basic statistics for the current record set:")
    for key, value in stats.items():
        if isinstance(value, float):
            print(f"    {key:<8} : {value:.3f}")
        else:
            print(f"    {key:<8} : {value}")
    if sn.ask_yes_no("\n  Save statistics to a file? (y/n) "):
        fname = sn.ask_text("  Filename (e.g. stats.txt): ")



def action_visualizations(data_frame, records):
    while True:
        print_viz_menu()
        choice = sn.ask_int("  Choice: ", min_value=0, max_value=5)

        if choice == 0:
            return

        # All charts (except pie) accept an optional topic filter
        topic = ""
        if choice in (1, 2, 3, 5):
            topic = sn.ask_text(
                "  Filter to a topic? (blank = all data): ",
                allow_blank=True
            )

        topic_label = topic if topic else "All Topics"

        if choice == 1:
            state_means = df.average_value_by_state(data_frame, topic or None)
            pm.BarChart_States(state_means, topic_label)

        elif choice == 2:
            year_means = df.average_value_by_year(data_frame, topic or None)
            pm.Line_Chart_Years(year_means, topic_label)

        elif choice == 3:
            filtered = (df.search_by_topic(records, topic)
                        if topic else records)
            pm.Histogram_Values(filtered, topic_label)

        elif choice == 4:
            counts = df.topic_counts(data_frame)
            pm.Pie_Chart(counts)

        elif choice == 5:
            filtered = (df.search_by_topic(records, topic)
                        if topic else records)
            pm.Scatter_Year_Value(filtered, topic_label)








def main():
    csv_path = fr.get_file()

    print(f"\n  Loading {csv_path} ... (this may take a few seconds)")

    try:
        data_frame, records = fr.load_records()
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
        choice = sn.ask_int("  Choice: ", min_value=0, max_value=9)

        if choice == 0:
            print("\n  Goodbye!")
            break
        elif choice == 1:
            show_summary(data_frame, records)
        elif choice == 2:
            action_search_state(records)
        elif choice == 3:
            action_search_topic(records)
        elif choice == 4:
            action_filter_year(current_records)
        elif choice == 5:
            action_filter_value(current_records)
        elif choice == 6:
            action_top_n(current_records)
        elif choice == 7:
            action_statistics(current_records)
        elif choice == 8:
            action_visualizations(data_frame, current_records)



if __name__ == "__main__":
    main()