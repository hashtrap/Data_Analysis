import matplotlib.pyplot as plt


def BarChart_States(state_means,topic_label,top_n=10):

    top=state_means.head(top_n)

    fig,ax=plt.subplot(figsize=(10,6))
    ax.bar(top.index,top.values,color='blue',edgecolor='black')

    ax.set_title(f"Top {top_n} States by Average Value — {topic_label}")
    ax.set_xlabel("State")
    ax.set_ylabel("Average value")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def Line_Chart_Years(year_means,topic_label):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(year_means.index, year_means.values,
            marker="o", color="darkorange", linewidth=2)

    ax.set_title(f"Average Value Over Time — {topic_label}")
    ax.set_xlabel("Year")
    ax.set_ylabel("Average value")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.show()


def Histogram_Values(records, topic_label, bins=30):

    values=[r.data_value for r in records]
    if not values:
        print("Data Unavailable")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(values, bins=bins, color="seagreen",
            edgecolor="black", alpha=0.8)

    ax.set_title(f"Distribution of Values — {topic_label}")
    ax.set_xlabel("Value")
    ax.set_ylabel("Number of records")
    plt.tight_layout()
    plt.show()

def Pie_Chart(topic_counts, top_n=8):

    if len(topic_counts) > top_n:
        top = topic_counts.head(top_n)
        other = topic_counts.iloc[top_n:].sum()
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

def Scatter_Year_Value(records, topic_label, max_points=2000):

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


