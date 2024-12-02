from typing import List
import pandas as pd

from data_loader import DataLoader
from model import Issue
import config
import plotting

class IssueStateAnalysis:
    """
    Analyzes issue activity by state (open vs. closed).
    """
    
    def __init__(self):
        """
        Constructor
        """
        
    def run(self):
        """
        Runs the analysis.
        """
        issues:List[Issue] = DataLoader().get_issues()
        
        # Optionally filter issues by user and/or label
        if self.USER:
            issues = [issue for issue in issues if issue.creator == self.USER]
        if self.LABEL:
            issues = [issue for issue in issues if self.LABEL in issue.labels]
        
        # Count issues by state
        state_counts = self.count_issue_states(issues)
        
        # Print the counts
        print(f'\nIssue counts by state: {state_counts}\n')
        
        # Plot the issue states using the generic pie_chart function
        plotting.pie_chart(state_counts, title='Issue States')
    
    def count_issue_states(self, issues: List[Issue]):
        """
        Counts the number of issues per state.
        
        Parameters:
        - issues: List of Issue objects.
        
        Returns:
        - A dictionary with states as keys and counts as values.
        """
        state_counts = {}
        for issue in issues:
            state = issue.state.value  # Assuming issue.state is an Enum
            state_counts[state] = state_counts.get(state, 0) + 1
        return state_counts

if __name__ == '__main__':
    IssueStateAnalysis().run()
