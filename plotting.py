import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def pie_chart(data, title='Pie Chart', labels=None):
    """
    Plots a pie chart.
    
    Parameters:
    - data: A dictionary or list of values.
    - title: Title of the chart.
    - labels: Labels for the pie slices.
    """
    if isinstance(data, dict):
        labels = list(data.keys()) if labels is None else labels
        sizes = list(data.values())
    else:
        sizes = data
        if labels is None:
            labels = [f'Label {i}' for i in range(len(sizes))]
    
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(title)
    plt.axis('equal')
    plt.show()

def plotList(list, column, top_num, title, xlabel, ylabel):
    """
    Plots a bar chart of the top `top_num` entries in a list.
    
    Parameters:
    - list: A list of data
    - column: The column label of the DataFrame
    - top_num: The number of entries to graph
    - title: The title of the chart
    - xlabel: X label of the chart
    - ylabel: Y label of the chart
    """
    # Create a dataframe to make statistics a lot easier
    df = pd.DataFrame(list, columns=[column])
    df_hist = df.groupby(df[column]).value_counts().nlargest(top_num).plot(kind="bar", figsize=(14,8), title=title)
    # Set axes labels
    df_hist.set_xlabel(xlabel)
    df_hist.set_ylabel(ylabel)
    # Plot the chart
    plt.grid(axis='y', linestyle='--')
    plt.show()

def plotSeries(data, title, xlabel, ylabel):
    """
    Creates a series from the data, plots a bar chart of the series.
    
    Parameters:
    - data: A list of data
    - title: The title of the chart
    - xlabel: X label of the chart
    - ylabel: Y label of the chart
    """
    # Create a series to make data easier to plot
    series = pd.Series(data)
    df_hist = series.value_counts().sort_index().plot(kind="bar", figsize=(14,8), title=title)
    # Set axes labels
    df_hist.set_xlabel(xlabel)
    df_hist.set_ylabel(ylabel)
    # Plot the chart
    plt.grid(axis='y', linestyle='--')
    plt.show()
    
def plotLabelOverTime(data, title, xlabel, ylabel):
    """
    Plots new issues with labels over time.
    
    Parameters:
    - data: A list of dictionaries with label & created_date values
    - title: The title of the chart
    - xlabel: X label of the chart
    - ylabel: Y label of the chart
    """
    # Create a dataframe to make statistics a lot easier
    df = pd.DataFrame(data)
    df["month"] = df["date"].dt.to_period("M")
    # Determine the number of new issues per month with the desired label and generate a graph
    df_hist = df.groupby(["month", "label"]).size().unstack(fill_value=0).plot(figsize=(14,8), title=title)
    # Set axes labels
    df_hist.set_xlabel(xlabel)
    df_hist.set_ylabel(ylabel)
    # Plot trends
    plt.grid()
    plt.tight_layout()
    plt.show()

def plot_gantt_chart(gantt_data: list):
    """
    Plots an enhanced Gantt chart showing created, closed, reopened dates and issue timelines.
    :param gantt_data: List of dict containing lifecycle details
    """
    for item in gantt_data:
        if item["issue_id"] == 454:
            created_date = item['created_date'].strftime("%Y-%m-%d")
            closed_dates = [date.strftime("%Y-%m-%d") for date in item['closed_dates']]
            reopened_dates = [date.strftime("%Y-%m-%d") for date in item['reopened_dates']]
            
            print(f"Issue 454:")
            print(f"Created date: {created_date}")
            print(f"Closed date: {closed_dates}")
            print(f"Reopened date: {reopened_dates}")
    
    gantt_data = [item for item in gantt_data if item["issue_id"] != 454]

    fig, ax = plt.subplots(figsize=(14, 10))

    # Collecting all dates for setting axis limits
    all_dates = [item["created_date"] for item in gantt_data] + \
                [date for item in gantt_data for date in item["closed_dates"] + item["reopened_dates"]]

    for i, lifecycle in enumerate(gantt_data):
        created_date = lifecycle["created_date"]
        closed_dates = lifecycle["closed_dates"]
        reopened_dates = lifecycle["reopened_dates"]

        timeline_start = created_date
        timeline_end = max(closed_dates + reopened_dates) if closed_dates or reopened_dates else created_date

        # Plotting the Gantt timeline
        ax.hlines(i, timeline_start, timeline_end, color="gray", linestyle="-", linewidth=2, alpha=0.6, label="Timeline" if i == 0 else "")

        # Plotting created, closed, and reopened dates
        ax.scatter(created_date, i, color="blue", label="Created" if i == 0 else "")
        for closed_date in closed_dates:
            ax.scatter(closed_date, i, color="red", label="Closed" if i == 0 else "")
        for reopened_date in reopened_dates:
            ax.scatter(reopened_date, i, color="green", label="Reopened" if i == 0 else "")

        ax.hlines(i, min(all_dates), max(all_dates), color="gray", linestyle="--", alpha=0.3)

    ax.set_yticks(range(len(gantt_data)))
    ax.set_yticklabels([f"Issue {item['issue_id']}" for item in gantt_data])
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.xticks(rotation=45, ha='right')

    ax.set_xlim(min(all_dates), max(all_dates))

    ax.set_ylim(0, len(gantt_data) - 1) 
    
    plt.xlabel("Date", fontsize=12)
    plt.ylabel("Issues", fontsize=12)
    plt.title("Gantt Chart of Issue Lifecycles", fontsize=14, fontweight="bold")

    plt.tight_layout(pad=3)  

    plt.legend()
    plt.show()

def plot_reopening_trend(reopened_issues_list: list):
    """
    Plots a bar chart showing the number of times issues were reopened over time.
    :param reopened_issues_list: List of issues that have been reopened
    """
    reopenings = []

    # Collecting all reopening dates from the reopened issues
    for issue in reopened_issues_list:
        for event in issue.events:
            if event.event_type == 'reopened':
                reopenings.append(event.event_date)

    # Creating a DataFrame
    reopenings_df = pd.DataFrame(reopenings, columns=["reopened_date"])

    # Grouping by month/year 
    reopenings_df['month_year'] = reopenings_df['reopened_date'].dt.to_period('M')
    
    # Counting the occurrences of reopenings in each period
    reopening_counts = reopenings_df['month_year'].value_counts().sort_index()

    # Creating a DataFrame for plotting
    reopening_data = pd.DataFrame({
        'Month/Year': reopening_counts.index.astype(str), 
        'Number of Reopenings': reopening_counts.values
    })

    # Plotting bar chart
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.bar(reopening_data['Month/Year'], reopening_data['Number of Reopenings'], color='teal', alpha=0.7)

    ax.set_title('Reopening Trend Over Time', fontsize=16, fontweight='bold')
    ax.set_xlabel('Month/Year', fontsize=12)
    ax.set_ylabel('Number of Reopenings', fontsize=12)

    plt.xticks(rotation=45, ha='right', fontsize=10)

    ax.grid(axis='y', linestyle='--', alpha=0.6)

    ax.set_yticks(range(0, int(reopening_data['Number of Reopenings'].max()) + 1, 1))

    plt.tight_layout()
    plt.show()

def categorize_reopened_time(issue):
    """
    Categorize the reopened issue based on the time difference between closing and reopening.
    :param issue: Issue object with events.
    :return: Category name as a string.
    """
    for event in issue.events:
        closed_date: datetime.datetime
        if event.event_type == "closed":
            closed_date = event.event_date
        if event.event_type == "reopened":
            time_difference = event.event_date - closed_date
            days = time_difference.days

            if days <= 1:
                return "within a day"
            elif 1 < days < 7:
                return "within a week"
            elif 7 < days < 14:
                return "7-14 days"
            elif 14< days < 30:
                return "14 days to a month"
            elif 30< days < 182:
                return "1-6 months"
            elif 182< days < 365:
                return "6-12 months"
            else:
                return "after one year"
    return None

def plot_reopened_issue_timing(issues_list):
    """
    Plot reopened issue timing as a Donut Chart with a legend showing percentages and counts.
    :param issues_list: List of Issue objects.
    """
    # Categorize each reopened issue
    reopen_categories = [
        categorize_reopened_time(issue) 
        for issue in issues_list 
        if any(event.event_type == 'reopened' for event in issue.events)
    ]

    # Filter out None values and count occurrences
    reopen_counts = pd.Series(filter(None, reopen_categories)).value_counts()

    # Calculate percentages
    total_reopened_issues = reopen_counts.sum()
    reopen_percentages = (reopen_counts / total_reopened_issues) * 100
    
    category_order = [
        "within a day", "within a week", "7-14 days", 
        "14 days to a month", "1-6 months", "6-12 months", "after one year"
    ]
    reopen_counts = reopen_counts[category_order]
    reopen_percentages = reopen_percentages[category_order]

    # Labels for the donut chart
    labels = reopen_counts.index

    legend_labels = [
        f"{category}: {reopen_percentages[category]:.1f}% ({reopen_counts[category]})"
        for category in category_order
        if category in reopen_counts.index
    ]

    # Plot Donut Chart
    plt.figure(figsize=(8, 8))
    wedges, texts = plt.pie(
        reopen_percentages,
        labels=labels,
        startangle=140,
        colors=plt.cm.Paired.colors,
        wedgeprops={'width': 0.3}
    )

    plt.legend(
        wedges, legend_labels, title="Reopen Timing", bbox_to_anchor=(1.05, 0.5)
    )

    plt.title("Time to Reopen Issues after being Closed\nTotal Reopened Issues: " + str(total_reopened_issues))
    plt.tight_layout()
    plt.show()
