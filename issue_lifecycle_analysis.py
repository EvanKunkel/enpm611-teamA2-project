import config
from data_loader import DataLoader
from model import Issue,Event
from typing import List

class IssueLifecycleAnalysis:
    
    def __init__(self):
        self.USER:str = config.get_parameter('user')
        self.FEATURE:str = config.get_parameter('feature')
    
    def run(self):
        issues_list:List[Issue] = DataLoader().get_issues()
        
        reopened_events:int = 0
        
        reopened_issues_list: List[Issue] = []
        
        
        for i in issues_list:
            for e in i.events:
                if e.event_type == 'reopened':
                    reopened_events+=1
                    reopened_issues_list.append(i)
        

if __name__ == '__main__':
    IssueLifecycleAnalysis().run()