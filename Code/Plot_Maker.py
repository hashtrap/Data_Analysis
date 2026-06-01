import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import defaultdict


## grouoping method to make the graphs better

def _group_records_by_unit(records, min_size=30):
    groups = defaultdict(list)
    for r in records:
        unit = r.data_value_unit or "(no unit)"
        groups[unit].append(r)

    big = [(u, rs) for u, rs in groups.items() if len(rs) >= min_size]
    big.sort(key=lambda kv: len(kv[1]), reverse=True)
    return big


def _group_df_by_unit(df, min_size=30):
    """Same idea but for a Pandas DataFrame. Requires an 'unit' column."""
    if "unit" not in df.columns:
        return [("(no unit)", df)]
    groups = []
    for unit, subset in df.groupby("unit"):
        if len(subset) >= min_size:
            groups.append((unit, subset))
    groups.sort(key=lambda kv: len(kv[1]), reverse=True)
    return groups


def _trim_outliers(values, low_pct=0.01, high_pct=0.99):
    if not values:
        return values
    s = sorted(values)
    lo = int(len(s) * low_pct)
    hi = int(len(s) * high_pct)
    return s[lo:hi] or s


# ─────────────────────────────────────────────────────────────
# 1. BAR CHART — top states (unit-aware)
# ─────────────────────────────────────────────────────────────

def bar_chart_top_states(df, topic_label, top_n=10):
    if df.empty:
        print("  No data to plot.")
        return

    unit_groups = _group_df_by_unit(df)[:4]
    if not unit_groups:
        print("  Not enough data per unit to plot.")
        return

    n = len(unit_groups)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 6), squeeze=False)
    axes = axes[0]

    for ax, (unit, subset) in zip(axes, unit_groups):
        means = subset.groupby("state")["value"].mean()
        means = means.sort_values(ascending=False).head(top_n)

        ax.bar(means.index, means.values,
               color="steelblue", edgecolor="black")
        ax.set_title(f"Top {top_n} states — {unit}  (n={len(subset)})")
        ax.set_xlabel("State")
        ax.set_ylabel(f"Avg value ({unit})")
        ax.tick_params(axis="x", rotation=45)
        for label in ax.get_xticklabels():
            label.set_horizontalalignment("right")

    fig.suptitle(f"Top States by Average Value — {topic_label}",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────
# 2. LINE CHART — average value over years (unit-aware)
# ─────────────────────────────────────────────────────────────

def line_chart_over_years(df, topic_label):
    if df.empty:
        print("  No data to plot.")
        return

    unit_groups = _group_df_by_unit(df)[:4]
    if not unit_groups:
        print("  Not enough data per unit to plot.")
        return

    n = len(unit_groups)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5), squeeze=False)
    axes = axes[0]

    for ax, (unit, subset) in zip(axes, unit_groups):
        year_means = subset.groupby("year")["value"].mean().sort_index()

        ax.plot(year_means.index, year_means.values,
                marker="o", color="darkorange", linewidth=2)
        ax.set_title(f"{unit}  (n={len(subset)})")
        ax.set_xlabel("Year")
        ax.set_ylabel(f"Avg value ({unit})")
        ax.grid(True, linestyle="--", alpha=0.5)
        # Force the x-axis to show only whole-number years.
        # Without this, matplotlib auto-generates fractional ticks
        # like 2014.5 because it doesn't know years are discrete.
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.suptitle(f"Average Value Over Time — {topic_label}",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────
# 3. HISTOGRAM — value distribution (unit-aware)
# ─────────────────────────────────────────────────────────────

def histogram_of_values(records, topic_label, bins=30):
    """One histogram per unit, with extreme 1% trimmed for readability."""
    if not records:
        print("  No data to plot.")
        return

    unit_groups = _group_records_by_unit(records)[:4]
    if not unit_groups:
        print("  Not enough data per unit to plot a histogram.")
        return

    n = len(unit_groups)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 5), squeeze=False)
    axes = axes[0]

    for ax, (unit, group_records) in zip(axes, unit_groups):
        values = [r.data_value for r in group_records]
        trimmed = _trim_outliers(values)

        ax.hist(trimmed, bins=bins, color="seagreen",
                edgecolor="black", alpha=0.8)
        ax.set_title(f"{unit}  (n={len(values)})")
        ax.set_xlabel(f"Value ({unit})")
        ax.set_ylabel("Number of records")
        ax.grid(True, linestyle="--", alpha=0.3)

    fig.suptitle(f"Distribution of Values — {topic_label}",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────
# 4. PIE CHART — share of records by topic (unit-safe by design)
# ─────────────────────────────────────────────────────────────

def pie_chart_topic_share(topic_counts, top_n=8):
    if topic_counts.empty:
        print("  No data to plot.")
        return

    if len(topic_counts) > top_n:
        top = topic_counts.head(top_n).copy()
        top["Other"] = topic_counts.iloc[top_n:].sum()
    else:
        top = topic_counts

    fig, ax = plt.subplots(figsize=(9, 9))
    ax.pie(top.values, labels=top.index, autopct="%1.1f%%", startangle=90)
    ax.set_title("Share of Records by Topic")
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────────────────────────
# 5. SCATTER — year vs value (unit-aware)
# ─────────────────────────────────────────────────────────────

def scatter_year_vs_value(records, topic_label, max_points_per_unit=2000):
    """One subplot per unit. Y-axis is clipped to 1st–99th percentile."""
    if not records:
        print("  No data to plot.")
        return

    unit_groups = _group_records_by_unit(records)[:4]
    if not unit_groups:
        print("  Not enough data per unit to plot.")
        return

    n = len(unit_groups)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 5), squeeze=False)
    axes = axes[0]

    for ax, (unit, group_records) in zip(axes, unit_groups):
        sample = group_records[:max_points_per_unit]
        years = [r.year for r in sample]
        values = [r.data_value for r in sample]

        # Clip y-axis so outliers don't flatten the rest of the cloud
        if values:
            s = sorted(values)
            lo = s[int(len(s) * 0.01)]
            hi = s[int(len(s) * 0.99)]
            ax.set_ylim(lo, hi)

        ax.scatter(years, values, alpha=0.4, color="crimson", s=15)
        ax.set_title(f"{unit}  (n={len(group_records)})")
        ax.set_xlabel("Year")
        ax.set_ylabel(f"Value ({unit})")
        ax.grid(True, linestyle="--", alpha=0.4)
        # Force whole-number year ticks on the x-axis
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    fig.suptitle(f"Year vs Value — {topic_label}",
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()