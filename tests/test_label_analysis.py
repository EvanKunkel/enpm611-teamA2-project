import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from label_analysis import LabelAnalysis
from model import Issue
from datetime import datetime

class TestLabelAnalysis(unittest.TestCase):
    def setUp(self):
        # Create fake data
        self.issues = [
            Issue({
                "labels": ["Bug", "Needs Triage"],
                "state": "open",
                "created_date": "2023-01-01",
                "events": [
                    {"event_type": "labeled"},
                    {"event_type": "unlabeled"},
                    {"event_type": "labeled"},
                    {"event_type": "labeled"},
                ]
            }),
            Issue({
                "labels": ["Bug"],
                "state": "open",
                "created_date": "2023-01-02",
                "events": [
                    {"event_type": "labeled"},
                    {"event_type": "unlabeled"},
                    {"event_type": "labeled"},
                ]
            }),
            Issue({
                "labels": ["New Feature"],
                "state": "open",
                "created_date": "2023-01-03",
                "events": [
                    {"event_type": "labeled"}
                ]
            })
        ]
        self.all_labels = ["Bug", "Needs Triage", "Bug", "New Feature"]

    def test_simpleLabelAnalysis(self):
        # Test with a specific label
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.issues, self.all_labels, label="Bug")
        self.assertEqual(unique_labels, 3)
        self.assertEqual(matching_issues, 2)

        # Test with no specific label
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.issues, self.all_labels)
        self.assertEqual(unique_labels, 3)
        self.assertEqual(matching_issues, 3)

        # Test with invalid inputs
        # None
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(None, self.all_labels)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.issues, None)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(None, None)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        # Empty lists
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis([], self.all_labels)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.issues, [])
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis([], [])
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        # Not lists
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis("String", self.all_labels)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.issues, "String")
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis("String", "String")
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        # Incorrect list types
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.all_labels, self.all_labels)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.issues, self.issues)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)
        unique_labels, matching_issues = LabelAnalysis().simpleLabelAnalysis(self.all_labels, self.issues)
        self.assertEqual(unique_labels, 0)
        self.assertEqual(matching_issues, 0)

    def test_simpleUnlabelingAnalysis(self):
        # Test unlabeling analysis
        unlabeling_counts, total_unlabels = LabelAnalysis().simpleUnlabelingAnalysis(self.issues)
        self.assertEqual(unlabeling_counts, [1, 1, 0])
        self.assertEqual(total_unlabels, 2)

        # Test with invalid input
        # None
        unlabeling_counts, total_unlabels = LabelAnalysis().simpleUnlabelingAnalysis(None)
        self.assertEqual(unlabeling_counts, [])
        self.assertEqual(total_unlabels, 0)
        # Empty lists
        unlabeling_counts, total_unlabels = LabelAnalysis().simpleUnlabelingAnalysis([])
        self.assertEqual(unlabeling_counts, [])
        self.assertEqual(total_unlabels, 0)
        # Not lists
        unlabeling_counts, total_unlabels = LabelAnalysis().simpleUnlabelingAnalysis("String")
        self.assertEqual(unlabeling_counts, [])
        self.assertEqual(total_unlabels, 0)
        # Incorrect list types
        unlabeling_counts, total_unlabels = LabelAnalysis().simpleUnlabelingAnalysis(["String"])
        self.assertEqual(unlabeling_counts, [])
        self.assertEqual(total_unlabels, 0)

    def test_getNewIssueDatesWithLabel(self):
        # Test with a label that exists
        results = LabelAnalysis().getNewIssueDatesWithLabel(self.issues, "Bug")
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["label"], "Bug")
        self.assertEqual(results[0]["date"], datetime(2023, 1, 1))

        # Test with a label that doesn't exist
        results = LabelAnalysis().getNewIssueDatesWithLabel(self.issues, "Nonexistent")
        self.assertEqual(len(results), 0)

        # Test with invalid input
        results = LabelAnalysis().getNewIssueDatesWithLabel(None, "Bug")
        self.assertEqual(results, [])
        
        # Test with invalid inputs
        # None
        results = LabelAnalysis().getNewIssueDatesWithLabel(None, "Bug")
        self.assertEqual(results, [])
        results = LabelAnalysis().getNewIssueDatesWithLabel(self.issues, None)
        self.assertEqual(results, [])
        # Empty list
        results = LabelAnalysis().getNewIssueDatesWithLabel([], "Bug")
        self.assertEqual(results, [])
        # Incorrect types
        results = LabelAnalysis().getNewIssueDatesWithLabel("String", "Bug")
        self.assertEqual(results, [])
        results = LabelAnalysis().getNewIssueDatesWithLabel(["String"], "Bug")
        self.assertEqual(results, [])
        results = LabelAnalysis().getNewIssueDatesWithLabel(self.issues, [])
        self.assertEqual(results, [])
        
if __name__ == '__main__':
    unittest.main()
