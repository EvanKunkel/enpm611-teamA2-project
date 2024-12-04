from typing import List
from plotting import plotList, plotSeries, plotLabelOverTime

from data_loader import DataLoader
from model import Issue
import config

class LabelAnalysis:
    """
    Implements a label analysis of the Github issues
    Includes the following subroutines:
        - simpleLabelAnalysis
            - Calculates the total number of labels amongst all issues
            - Finds the number of issues with the user inputted label (all by default)
        - plotTopLabels
            - Plots the top 20 most used labels and the number of issues with those labels
        - simpleUnlabelingAnalysis
            - Calculates the average number of unlabeling events per issue
            - Plots the number of issues by the number of unlabeling events in those issues
        - plotIssuesOverTimeForLabel
            - Plots the number of new issues created with a user inputted label by time (does nothing if no label is input)
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
        
        # Store the labels in a list, call subroutines
        all_labels = [label for issue in issues for label in issue.labels]
        self.simpleLabelAnalysis(issues, all_labels)
        self.plotTopLabels(all_labels)
        self.simpleUnlabelingAnalysis(issues)
        self.plotIssuesOverTimeForLabel(issues)
        
    def simpleLabelAnalysis(self, issues:List[Issue], all_labels:List[str]):
        # Using a set, get the number of unique labels
        unique_labels = set(all_labels)
        print('\nNumber of unique labels:', len(unique_labels), '\n')
        
        # Count the number of issues with a specific label
        total_issues:int = len([issue for issue in issues if self.LABEL is None or self.LABEL in issue.labels])
            
        output:str = f'Found {total_issues} issues across {len(issues)} issues'
        output += f' with label {self.LABEL}.' if self.LABEL is not None else '.'
        print(output + '\n')
        
    def plotTopLabels(self, all_labels:List[str]):
         # Display a graph of the top 20 labels
        top_num:int = 20
        column:str = "label"
        title:str  = f"Top {top_num} labels"
        xlabel:str = "Issue Labels"
        ylabel:str = "# of Issues"
        plotList(all_labels, column, top_num, title, xlabel, ylabel)
        
    def simpleUnlabelingAnalysis(self, issues:List[Issue]):
        # Count the number of unlabeling events per issue
        unlabeling_counts = []
        for issue in issues:
            unlabel_count = sum(1 for event in issue.events if event.event_type == "unlabeled")
            unlabeling_counts.append(unlabel_count)

        print(f"Average number of unlabeling events per issue: {sum(unlabeling_counts)/len(issues):.3f}\n")

        # Plot the issues by number of unlabeling events
        title:str  = "Distribution of Issues by Number of Unlabeling Events"
        xlabel:str = "# of Unlabeling Events per Issue"
        ylabel:str = "# of Issues"
        plotSeries(unlabeling_counts, title, xlabel, ylabel)
        
    def plotIssuesOverTimeForLabel(self, issues:List[Issue]):
        # Show creation trends over time for user inputted parameter label
        if self.LABEL is None:
            exit()
        
        label_list = [{"date": issue.created_date, "label": label} for issue in issues for label in issue.labels if label == self.LABEL]
        
        title:str  = f"Trends Over Time For Label: {self.LABEL}"
        xlabel:str = "Month"
        ylabel:str = "# of Issues"
        plotLabelOverTime(label_list, title, xlabel, ylabel)
        
if __name__ == '__main__':
    # Invoke run method when running this module directly
    LabelAnalysis().run()