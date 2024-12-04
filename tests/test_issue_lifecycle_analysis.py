import unittest
from unittest.mock import patch, MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from issue_lifecycle_analysis import IssueLifecycleAnalysis

class TestIssueLifecycleAnalysis(unittest.TestCase):
    
    @patch('issue_lifecycle_analysis.config')
    def test_configuration_initialization(self, mock_config):
        # Mocking configuration parameters
        mock_config.get_parameter.side_effect = lambda key: f"mock_{key}"

        # Instantiating the class
        analysis = IssueLifecycleAnalysis()

        # Validation
        self.assertEqual(analysis.USER, "mock_user")
        self.assertEqual(analysis.FEATURE, "mock_feature")
    
    @patch('issue_lifecycle_analysis.plot_gantt_chart')
    @patch('issue_lifecycle_analysis.plot_reopening_trend')
    @patch('issue_lifecycle_analysis.plot_reopened_issue_timing')
    @patch('issue_lifecycle_analysis.DataLoader')
    @patch('issue_lifecycle_analysis.config')
    def test_plot_lifecycle(
        self, mock_config, mock_dataloader, mock_plot_timing, mock_plot_trend, mock_plot_chart
    ):
        # Mocking
        mock_config.get_parameter.side_effect = lambda key: f"mock_{key}"

        #Mocking data for issues
        mock_event_reopened = MagicMock(event_type="reopened", event_date="2024-01-01")
        mock_event_closed = MagicMock(event_type="closed", event_date="2024-02-01")
        mock_issue = MagicMock()
        mock_issue.number = 1
        mock_issue.created_date = "2023-12-01"
        mock_issue.updated_date = "2024-02-01"
        mock_issue.events = [mock_event_reopened, mock_event_closed]

        # Mocking DataLoader to return the mock issue
        mock_dataloader.return_value.get_issues.return_value = [mock_issue]

        # Instantiating the class and run the method
        analysis = IssueLifecycleAnalysis()
        analysis.plot_lifecycle()

        # Assert that plotting functions were called with correct data
        mock_plot_chart.assert_called_once()
        mock_plot_trend.assert_called_once()
        mock_plot_timing.assert_called_once()

        # Validation
        gantt_data = mock_plot_chart.call_args[0][0]
        self.assertEqual(len(gantt_data), 1)
        self.assertEqual(gantt_data[0]['issue_number'], 1)
        self.assertEqual(gantt_data[0]['issue_id'], 1)
        self.assertIn("2024-01-01", gantt_data[0]['reopened_dates'])
        self.assertIn("2024-02-01", gantt_data[0]['closed_dates'])

        reopened_issues = mock_plot_trend.call_args[0][0]
        self.assertEqual(len(reopened_issues), 1)
        self.assertEqual(reopened_issues[0].number, 1)
    
    @patch('issue_lifecycle_analysis.plot_gantt_chart')
    @patch('issue_lifecycle_analysis.plot_reopening_trend')
    @patch('issue_lifecycle_analysis.plot_reopened_issue_timing')
    @patch('issue_lifecycle_analysis.DataLoader')
    @patch('issue_lifecycle_analysis.config')
    def test_multiple_issues(
        self, mock_config, mock_dataloader, mock_plot_timing, mock_plot_trend, mock_plot_chart
    ):
        # Mocking configuration parameters
        mock_config.get_parameter.side_effect = lambda key: f"mock_{key}"

        # Mocking data for multiple issues
        mock_event_reopened_1 = MagicMock(event_type="reopened", event_date="2024-01-01")
        mock_event_closed_1 = MagicMock(event_type="closed", event_date="2024-02-01")
        mock_issue_1 = MagicMock()
        mock_issue_1.number = 1
        mock_issue_1.created_date = "2023-12-01"
        mock_issue_1.updated_date = "2024-02-01"
        mock_issue_1.events = [mock_event_reopened_1, mock_event_closed_1]

        mock_event_closed_2 = MagicMock(event_type="closed", event_date="2024-03-01")
        mock_issue_2 = MagicMock()
        mock_issue_2.number = 2
        mock_issue_2.created_date = "2024-01-01"
        mock_issue_2.updated_date = "2024-03-01"
        mock_issue_2.events = [mock_event_closed_2]

        # Mocking DataLoader to return the mock issues
        mock_dataloader.return_value.get_issues.return_value = [mock_issue_1, mock_issue_2]

        # Instantiating the class and run the method
        analysis = IssueLifecycleAnalysis()
        analysis.plot_lifecycle()

        # Validation
        mock_plot_chart.assert_called_once()
        mock_plot_trend.assert_called_once()
        mock_plot_timing.assert_called_once()

        gantt_data = mock_plot_chart.call_args[0][0]
        self.assertEqual(len(gantt_data), 1)  # Only 1 issue with reopened events
        self.assertEqual(gantt_data[0]['issue_number'], 1)
        self.assertIn("2024-01-01", gantt_data[0]['reopened_dates'])

        reopened_issues = mock_plot_trend.call_args[0][0]
        self.assertEqual(len(reopened_issues), 1)  # Only 1 reopened issue
        self.assertEqual(reopened_issues[0].number, 1)
    
    @patch('issue_lifecycle_analysis.plot_gantt_chart')
    @patch('issue_lifecycle_analysis.plot_reopening_trend')
    @patch('issue_lifecycle_analysis.plot_reopened_issue_timing')
    @patch('issue_lifecycle_analysis.DataLoader')
    @patch('issue_lifecycle_analysis.config')
    def test_issues_without_reopened_events(
        self, mock_config, mock_dataloader, mock_plot_timing, mock_plot_trend, mock_plot_chart
    ):
        # Mocking configuration parameters
        mock_config.get_parameter.side_effect = lambda key: f"mock_{key}"

        # Creating mock data for an issue without 'reopened' events
        mock_event_closed = MagicMock(event_type="closed", event_date="2024-02-01")
        mock_issue = MagicMock()
        mock_issue.number = 1
        mock_issue.created_date = "2023-12-01"
        mock_issue.updated_date = "2024-02-01"
        mock_issue.events = [mock_event_closed]

        # Mocking DataLoader to return the mock issue
        mock_dataloader.return_value.get_issues.return_value = [mock_issue]

        # Instantiating the class and run the method
        analysis = IssueLifecycleAnalysis()
        analysis.plot_lifecycle()

        # Validation
        mock_plot_chart.assert_called_once()
        mock_plot_trend.assert_called_once()
        mock_plot_timing.assert_called_once()

        gantt_data = mock_plot_chart.call_args[0][0]
        self.assertEqual(len(gantt_data), 0) 

        reopened_issues = mock_plot_trend.call_args[0][0]
        self.assertEqual(len(reopened_issues), 0) 
    

if __name__ == "__main__":
    unittest.main()
