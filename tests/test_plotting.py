import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from plotting import pie_chart, plotSeries, plotLabelOverTime, plot_gantt_chart, categorize_reopened_time, plot_reopening_trend
from model import Issue, Event

class TestPlotting(unittest.TestCase):
    
    @patch("matplotlib.pyplot.pie")  
    @patch("matplotlib.pyplot.show")  
    def test_pie_chart(self, mock_show, mock_pie):
        # Test case 1: Using a dictionary for data
        data = {'Category A': 40, 'Category B': 30, 'Category C': 30}
        labels = ['A', 'B', 'C']

        pie_chart(data, title='Test Pie Chart', labels=labels)

        # Check if plt.pie was called with the correct data and labels
        mock_pie.assert_called_with([40, 30, 30], labels=['A', 'B', 'C'], autopct='%1.1f%%', startangle=140)

        mock_show.assert_called_once()

        # Test case 2: Using a list for data without labels
        data = [50, 25, 25]

        pie_chart(data, title='Test Pie Chart without Labels')

        # Check if plt.pie was called with the correct data and default labels
        mock_pie.assert_called_with([50, 25, 25], labels=['Label 0', 'Label 1', 'Label 2'], autopct='%1.1f%%', startangle=140)
        mock_show.assert_called_with()
    
    @patch("matplotlib.pyplot.show") 
    def test_plot_series(self, mock_show):
        data = [1, 2, 2, 3, 3, 3, 4]
        title = "Test Bar Chart"
        xlabel = "Values"
        ylabel = "Frequency"
        plotSeries(data, title, xlabel, ylabel)
        mock_show.assert_called_once()
    
    
    @patch("matplotlib.pyplot.show")  
    def test_plot_label_over_time(self, mock_show):
        data = [
            {"label": "bug", "date": pd.Timestamp("2023-01-15")},
            {"label": "feature", "date": pd.Timestamp("2023-01-16")},
            {"label": "bug", "date": pd.Timestamp("2023-02-01")},
            {"label": "bug", "date": pd.Timestamp("2023-02-10")},
            {"label": "feature", "date": pd.Timestamp("2023-03-01")},
        ]
        
        title = "Issues with Labels Over Time"
        xlabel = "Month"
        ylabel = "Number of Issues"
        plotLabelOverTime(data, title, xlabel, ylabel)
        mock_show.assert_called_once()
    
    @patch('matplotlib.pyplot.show')
    @patch('builtins.print')
    def test_plot_gantt_chart(self, mock_print, mock_show):
        # Sample Gantt chart data
        data = [
            {"issue_id": 454, "created_date": datetime(2024, 1, 1), "closed_dates": [datetime(2024, 2, 1)], "reopened_dates": [datetime(2024, 3, 1)]},
            {"issue_id": 123, "created_date": datetime(2024, 2, 1), "closed_dates": [datetime(2024, 3, 1)], "reopened_dates": []},
            {"issue_id": 456, "created_date": datetime(2024, 3, 1), "closed_dates": [datetime(2024, 4, 1)], "reopened_dates": [datetime(2024, 5, 1)]}
        ]
        
        plot_gantt_chart(data)
        
        # Check if the print statement was called for issue_id 454
        mock_print.assert_any_call("Issue 454:")
        mock_print.assert_any_call("Created date: 2024-01-01")
        mock_print.assert_any_call("Closed date: ['2024-02-01']")
        mock_print.assert_any_call("Reopened date: ['2024-03-01']")
        
        # Verify that show() was called (which means the plot was triggered)
        mock_show.assert_called()
    
    def test_categorize_reopened_time(self):
        # Case 1: Reopened within a day
        issue = MagicMock(events=[
            MagicMock(event_type="closed", event_date=datetime(2024, 1, 1)),
            MagicMock(event_type="reopened", event_date=datetime(2024, 1, 1, 12, 0)),  # 12 hours later
        ])
        self.assertEqual(categorize_reopened_time(issue), "within a day")

        # Case 2: Reopened within a week
        issue = MagicMock(events=[
            MagicMock(event_type="closed", event_date=datetime(2024, 1, 1)),
            MagicMock(event_type="reopened", event_date=datetime(2024, 1, 5)),  # 4 days later
        ])
        self.assertEqual(categorize_reopened_time(issue), "within a week")
    
    @patch("matplotlib.pyplot.show")  
    def test_plot_reopening_trend(self, mock_show):
        # Mock data
        reopened_issues_list = [
            MagicMock(events=[
                MagicMock(event_type="reopened", event_date=pd.Timestamp("2024-01-15")),
                MagicMock(event_type="reopened", event_date=pd.Timestamp("2024-01-20")),
            ]),
            MagicMock(events=[
                MagicMock(event_type="reopened", event_date=pd.Timestamp("2024-02-10")),
            ]),
        ]

        plot_reopening_trend(reopened_issues_list)

        reopenings = [pd.Timestamp("2024-01-15"), pd.Timestamp("2024-01-20"), pd.Timestamp("2024-02-10")]
        expected_reopenings_df = pd.DataFrame(reopenings, columns=["reopened_date"])
        expected_reopenings_df["month_year"] = expected_reopenings_df["reopened_date"].dt.to_period("M")

        reopening_counts = expected_reopenings_df["month_year"].value_counts().sort_index()

        self.assertEqual(len(reopening_counts), 2)  # Two unique months
        self.assertEqual(reopening_counts[0], 2)  # January 2024
        self.assertEqual(reopening_counts[1], 1)  # February 2024
        
        mock_show.assert_called_once()
    
if __name__ == '__main__':
    unittest.main()