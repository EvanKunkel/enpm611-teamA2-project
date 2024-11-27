import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

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
        'Month/Year': reopening_counts.index.astype(str),  # Convert period to string for display
        'Number of Reopenings': reopening_counts.values
    })

    # Plotting with matplotlib (bar chart)
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