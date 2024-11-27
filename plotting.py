import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

    # Collect all dates for setting axis limits
    all_dates = [item["created_date"] for item in gantt_data] + \
                [date for item in gantt_data for date in item["closed_dates"] + item["reopened_dates"]]

    for i, lifecycle in enumerate(gantt_data):
        created_date = lifecycle["created_date"]
        closed_dates = lifecycle["closed_dates"]
        reopened_dates = lifecycle["reopened_dates"]

        timeline_start = created_date
        timeline_end = max(closed_dates + reopened_dates) if closed_dates or reopened_dates else created_date

        # Plot the Gantt timeline
        ax.hlines(i, timeline_start, timeline_end, color="gray", linestyle="-", linewidth=2, alpha=0.6, label="Timeline" if i == 0 else "")

        # Plot created, closed, and reopened dates
        ax.scatter(created_date, i, color="blue", label="Created" if i == 0 else "")
        for closed_date in closed_dates:
            ax.scatter(closed_date, i, color="red", label="Closed" if i == 0 else "")
        for reopened_date in reopened_dates:
            ax.scatter(reopened_date, i, color="green", label="Reopened" if i == 0 else "")

        # Add dashed line linking the issue with the timeline
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
