import csv
from pathlib import Path
from typing import List

from models import Bill, Legislator, VoteResult, Vote


class LegislatorsRepository:
    """Repository class to read CSV data and return dataclass instances"""
    
    def __init__(self, datasets_path: str = "datasets"):
        """
        Initialize the repository with the path to the datasets folder
        
        Args:
            datasets_path: Path to the folder containing CSV files
        """
        self.datasets_path = Path(datasets_path)
    
    def get_all_bills(self) -> List[Bill]:
        """Read bills.csv and return a list of Bill instances"""
        bills = []
        bills_file = self.datasets_path / "bills.csv"
        
        with open(bills_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                bill = Bill(
                    id=int(row['id']),
                    title=row['title'],
                    sponsor_id=int(row['sponsor_id'])
                )
                bills.append(bill)
        
        return bills
    
    def get_all_legislators(self) -> List[Legislator]:
        """Read legislators.csv and return a list of Legislator instances"""
        legislators = []
        legislators_file = self.datasets_path / "legislators.csv"
        
        with open(legislators_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                legislator = Legislator(
                    id=int(row['id']),
                    name=row['name']
                )
                legislators.append(legislator)
        
        return legislators
    
    def get_all_vote_results(self) -> List[VoteResult]:
        """Read vote_results.csv and return a list of VoteResult instances"""
        vote_results = []
        vote_results_file = self.datasets_path / "vote_results.csv"
        
        with open(vote_results_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vote_result = VoteResult(
                    id=int(row['id']),
                    legislator_id=int(row['legislator_id']),
                    vote_id=int(row['vote_id']),
                    vote_type=int(row['vote_type'])
                )
                vote_results.append(vote_result)
        
        return vote_results
    
    def get_all_votes(self) -> List[Vote]:
        """Read votes.csv and return a list of Vote instances"""
        votes = []
        votes_file = self.datasets_path / "votes.csv"
        
        with open(votes_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vote = Vote(
                    id=int(row['id']),
                    bill_id=int(row['bill_id'])
                )
                votes.append(vote)
        
        return votes
