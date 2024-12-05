import unittest
from datetime import datetime
from dateutil import parser
from unittest.mock import MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model import Event, Issue, State

class TestDataModel(unittest.TestCase):

    def test_event_from_json(self):
        # Simulating input JSON data for Event
        event_data = {
            'event_type': 'opened',
            'author': 'user123',
            'event_date': '2024-12-05T12:00:00Z',
            'label': 'bug',
            'comment': 'Initial comment.'
        }
        
        # Creating an Event object from the JSON data
        event = Event(event_data)
        
        # Assertions
        self.assertEqual(event.event_type, 'opened')
        self.assertEqual(event.author, 'user123')
        self.assertEqual(event.label, 'bug')
        self.assertEqual(event.comment, 'Initial comment.')
        self.assertEqual(event.event_date, parser.parse('2024-12-05T12:00:00Z'))

    def test_event_from_json_invalid_date(self):
        # Simulating input JSON data with an invalid date
        event_data = {
            'event_type': 'closed',
            'author': 'user456',
            'event_date': 'invalid_date_format',
            'label': 'enhancement',
            'comment': 'Closed after review.'
        }
        
        # Creating an Event object from the JSON data
        event = Event(event_data)
        
        # Assertions
        self.assertEqual(event.event_type, 'closed')
        self.assertEqual(event.author, 'user456')
        self.assertEqual(event.label, 'enhancement')
        self.assertEqual(event.comment, 'Closed after review.')
        self.assertIsNone(event.event_date)  # Invalid date should result in None

    def test_issue_from_json(self):
        event_data = {
            'event_type': 'opened',
            'author': 'user123',
            'event_date': '2024-12-05T12:00:00Z',
            'label': 'bug',
            'comment': 'Initial comment.'
        }
        # Simulating input JSON data for Issue
        issue_data = {
            'url': 'https://example.com/issue/123',
            'creator': 'creator1',
            'labels': ['bug', 'high-priority'],
            'state': 'open',
            'assignees': ['user1', 'user2'],
            'title': 'Issue title',
            'text': 'Issue description text.',
            'number': '123',
            'created_date': '2024-12-05T12:00:00Z',
            'updated_date': '2024-12-06T12:00:00Z',
            'timeline_url': 'https://example.com/timeline/123',
            'events': [event_data]  # Add the event object from above
        }
        
        # Creating an Issue object from the JSON data
        issue = Issue(issue_data)
        
        # Assertions for Issue attributes
        self.assertEqual(issue.url, 'https://example.com/issue/123')
        self.assertEqual(issue.creator, 'creator1')
        self.assertEqual(issue.labels, ['bug', 'high-priority'])
        self.assertEqual(issue.state, State.open)
        self.assertEqual(issue.assignees, ['user1', 'user2'])
        self.assertEqual(issue.title, 'Issue title')
        self.assertEqual(issue.text, 'Issue description text.')
        self.assertEqual(issue.number, 123)
        self.assertEqual(issue.created_date, parser.parse('2024-12-05T12:00:00Z'))
        self.assertEqual(issue.updated_date, parser.parse('2024-12-06T12:00:00Z'))
        self.assertEqual(issue.timeline_url, 'https://example.com/timeline/123')
        self.assertEqual(len(issue.events), 1)  # Should contain 1 event

        # Assertions for the Event inside Issue
        event = issue.events[0]
        self.assertEqual(event.event_type, 'opened')  # Check if the event is correct
        self.assertEqual(event.author, 'user123')

    def test_issue_from_json_invalid_date(self):
        # Simulating input JSON data for Issue with invalid date
        issue_data = {
            'url': 'https://example.com/issue/456',
            'creator': 'creator2',
            'labels': ['enhancement'],
            'state': 'closed',
            'assignees': ['user3'],
            'title': 'Another issue title',
            'text': 'Another issue description.',
            'number': '456',
            'created_date': 'invalid_date_format',
            'updated_date': '2024-12-06T12:00:00Z',
            'timeline_url': 'https://example.com/timeline/456',
            'events': []
        }
        
        # Creating an Issue object from the JSON data
        issue = Issue(issue_data)
        
        # Assertions
        self.assertEqual(issue.url, 'https://example.com/issue/456')
        self.assertEqual(issue.creator, 'creator2')
        self.assertEqual(issue.labels, ['enhancement'])
        self.assertEqual(issue.state, State.closed)
        self.assertEqual(issue.assignees, ['user3'])
        self.assertEqual(issue.title, 'Another issue title')
        self.assertEqual(issue.text, 'Another issue description.')
        self.assertEqual(issue.number, 456)
        self.assertIsNone(issue.created_date)  # Invalid date should result in None
        self.assertEqual(issue.updated_date, parser.parse('2024-12-06T12:00:00Z'))
        self.assertEqual(issue.timeline_url, 'https://example.com/timeline/456')
        self.assertEqual(len(issue.events), 0)  # No events in this issue

if __name__ == '__main__':
    unittest.main()
