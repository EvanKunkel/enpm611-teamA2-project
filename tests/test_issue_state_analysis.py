import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from issue_state_analysis import IssueStateAnalysis
from model import Issue, State

class TestIssueStateAnalysis(unittest.TestCase):
    def setUp(self):
        self.analysis = IssueStateAnalysis()
        
    def test_empty_issues(self):
        issues = []
        expected_counts = {}
        counts = self.analysis.count_issue_states(issues)
        self.assertEqual(counts, expected_counts)
    
    def test_all_open(self):
        issues = [
            Issue({'state': 'open'}),
            Issue({'state': 'open'}),
            Issue({'state': 'open'}),
        ]
        expected_counts = {'open': 3}
        counts = self.analysis.count_issue_states(issues)
        self.assertEqual(counts, expected_counts)
    
    def test_all_closed(self):
        issues = [
            Issue({'state': 'closed'}),
            Issue({'state': 'closed'}),
            Issue({'state': 'closed'}),
        ]
        expected_counts = {'closed': 3}
        counts = self.analysis.count_issue_states(issues)
        self.assertEqual(counts, expected_counts)
    
    def test_mix_open_closed(self):
        issues = [
            Issue({'state': 'open'}),
            Issue({'state': 'closed'}),
            Issue({'state': 'open'}),
            Issue({'state': 'closed'}),
            Issue({'state': 'open'}),
        ]
        expected_counts = {'open': 3, 'closed': 2}
        counts = self.analysis.count_issue_states(issues)
        self.assertEqual(counts, expected_counts)

if __name__ == '__main__':
    unittest.main()
