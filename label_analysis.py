from typing import List
from plotting import plotList, plotSeries, plotLabelOverTime

from data_loader import DataLoader
from model import Issue
import config

class LabelAnalysis:
    """
    Implements a label analysis of the Github issues
    Performs the following subroutines:
        - Simple Label Analysis
            - Calculates the total number of labels amongst all issues
            - Finds the number of issues with the user input label (all by default)
        - Plot Top Labels
            - Plots the top 20 most used labels and the number of issues with those labels
        - Simple Unlabeling Analysis
            - Calculates the average number of unlabeling events per issue
            - Plots the number of issues by the number of unlabeling events in those issues
        - Plot Issues Over Time For Label
            - Plots the number of new issues created with a user input label by time (does nothing if no label is input)
    """
    
    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--label)
        self.LABEL:str = config.get_parameter('label')
        
    def run(self):
        """
        Run the label analysis
        """
        issues:List[Issue] = DataLoader().get_issues()
        numIssues:int = len(issues)
        
        # Store the labels in a list, run subroutines
        all_labels = [label for issue in issues for label in issue.labels]
        
        # Calculate number of unique labels, total number of issues with an input label (all by default)
        numUniqueLabels, numIssuesWithLabel = self.simpleLabelAnalysis(issues, all_labels, self.LABEL)
        # Create output string
        output:str = f'\nNumber of unique labels: {numUniqueLabels}\n'
        output += f'\nFound {numIssuesWithLabel} issues across {numIssues} issues'
        if self.LABEL is not None:
            output += f' with label {self.LABEL}'
        output += f'.\n'
        print(output)
        
        # Display a graph of the top 20 labels
        top_num:int = 20
        column:str = "label"
        title:str  = f"Top {top_num} labels"
        xlabel:str = "Issue Labels"
        ylabel:str = "# of Issues"
        plotList(all_labels, column, top_num, title, xlabel, ylabel)
        
        # Get the average number of unlabeling events per issue, plot distribution of unlabeling events per issue
        unlabeling_counts, numUnlabelEvents = self.simpleUnlabelingAnalysis(issues)
        output:str = f'Average number of unlabeling events per issue: {numUnlabelEvents/numIssues:.3f}\n'
        print(output)
        title:str  = "Distribution of Issues by Number of Unlabeling Events"
        xlabel:str = "# of Unlabeling Events per Issue"
        ylabel:str = "# of Issues"
        plotSeries(unlabeling_counts, title, xlabel, ylabel)
        
        # Stop here if there was no user inputted label
        if self.LABEL is None:
            exit()
        
        # Show creation trends over time for user inputted parameter label
        newIssueDatesWithLabel = self.getNewIssueDatesWithLabel(issues, self.LABEL)
        title:str  = f"Trends Over Time For Label: {self.LABEL}"
        xlabel:str = "Month"
        ylabel:str = "# of Issues"
        plotLabelOverTime(newIssueDatesWithLabel, title, xlabel, ylabel)
        
    def simpleLabelAnalysis(self, issues:List[Issue], all_labels:List[str], label:str=None):
        """
        Performs simple label analysis of issues.
        
        Parameters:
        - issues: List of Issue objects.
        - all_labels: List labels from each issue.
        - label: Label with which to search for issues.
        
        Returns:
        - The number of unique labels amongst all of the issues.
        - The number of issues that contain the label (all issues if label is None).
        """
        # Type checking
        if issues is None or all_labels is None:
            return 0, 0
        if not isinstance(issues, List) or not isinstance(all_labels, List):
            return 0, 0
        if len(issues) == 0 or len(all_labels) == 0:
            return 0, 0
        if not isinstance(issues[0], Issue) or not isinstance(all_labels[0], str):
            return 0, 0
        return len(set(all_labels)), len([issue for issue in issues if label is None or label in issue.labels])
        
    def simpleUnlabelingAnalysis(self, issues:List[Issue]):
        """
        Performs simple unlabeling analysis of issues.
        
        Parameters:
        - issues: List of Issue objects.
        
        Returns:
        - A list of the number of unlabeling events per issue.
        - The total number of unlabeling events amongst all of the issues.
        """
        if not isinstance(issues, List) or len(issues) == 0 or not isinstance(issues[0], Issue):
            return [], 0
        # Count the number of unlabeling events per issue
        unlabeling_counts = [sum(1 for event in issue.events if event.event_type == "unlabeled") for issue in issues]
        return unlabeling_counts, sum(unlabeling_counts)
        
    def getNewIssueDatesWithLabel(self, issues:List[Issue], labelIn:str):
        """
        Gets creation dates of issues with the input label.
        
        Parameters:
        - issues: List of Issue objects.
        - labelIn: Label with which to search for issues.
        
        Returns:
        - A list of dictionaries with label & created_date values.
        """
        if not isinstance(issues, List) or len(issues) == 0 or not isinstance(issues[0], Issue):
            return []
        # Create a list of dictionaries with label & created_date values
        return [{"date": issue.created_date, "label": label} for issue in issues for label in issue.labels if label == labelIn]
        
if __name__ == '__main__':
    # Invoke run method when running this module directly
    LabelAnalysis().run()
