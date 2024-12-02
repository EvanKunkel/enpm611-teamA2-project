import matplotlib.pyplot as plt

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
