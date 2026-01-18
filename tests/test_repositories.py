import csv
import tempfile
import pytest
from pathlib import Path
from repositories import LegislatorsRepository
from models import Bill, Legislator, VoteResult, Vote, LegislatorVoteCount, BillVoteCount


class TestLegislatorsRepository:
    """Tests for LegislatorsRepository"""
    
    def test_get_all_bills(self):
        """Test reading bills from CSV"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / "input"
            input_dir.mkdir()
            
            bills_file = input_dir / "bills.csv"
            with open(bills_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'title', 'sponsor_id'])
                writer.writeheader()
                writer.writerow({'id': '1', 'title': 'Test Bill 1', 'sponsor_id': '10'})
                writer.writerow({'id': '2', 'title': 'Test Bill 2', 'sponsor_id': '20'})
            
            repo = LegislatorsRepository(
                datasets_path=tmpdir,
                datasets_input_path=str(input_dir),
                datasets_output_path=str(Path(tmpdir) / "output")
            )
            
            bills = repo.get_all_bills()
            
            assert len(bills) == 2
            assert bills[0].id == 1
            assert bills[0].title == "Test Bill 1"
            assert bills[0].sponsor_id == 10
            assert bills[1].id == 2
            assert bills[1].title == "Test Bill 2"
            assert bills[1].sponsor_id == 20
    
    def test_get_all_legislators(self):
        """Test reading legislators from CSV"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / "input"
            input_dir.mkdir()
            
            legislators_file = input_dir / "legislators.csv"
            with open(legislators_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'name'])
                writer.writeheader()
                writer.writerow({'id': '1', 'name': 'John Doe'})
                writer.writerow({'id': '2', 'name': 'Jane Smith'})
            
            repo = LegislatorsRepository(
                datasets_path=tmpdir,
                datasets_input_path=str(input_dir),
                datasets_output_path=str(Path(tmpdir) / "output")
            )
            
            legislators = repo.get_all_legislators()
            
            assert len(legislators) == 2
            assert legislators[0].id == 1
            assert legislators[0].name == "John Doe"
            assert legislators[1].id == 2
            assert legislators[1].name == "Jane Smith"
    
    def test_get_all_vote_results(self):
        """Test reading vote results from CSV"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / "input"
            input_dir.mkdir()
            
            vote_results_file = input_dir / "vote_results.csv"
            with open(vote_results_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'legislator_id', 'vote_id', 'vote_type'])
                writer.writeheader()
                writer.writerow({'id': '1', 'legislator_id': '10', 'vote_id': '100', 'vote_type': '1'})
                writer.writerow({'id': '2', 'legislator_id': '20', 'vote_id': '100', 'vote_type': '2'})
            
            repo = LegislatorsRepository(
                datasets_path=tmpdir,
                datasets_input_path=str(input_dir),
                datasets_output_path=str(Path(tmpdir) / "output")
            )
            
            vote_results = repo.get_all_vote_results()
            
            assert len(vote_results) == 2
            assert vote_results[0].id == 1
            assert vote_results[0].legislator_id == 10
            assert vote_results[0].vote_id == 100
            assert vote_results[0].vote_type == 1
            assert vote_results[1].vote_type == 2
    
    def test_get_all_votes(self):
        """Test reading votes from CSV"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / "input"
            input_dir.mkdir()
            
            votes_file = input_dir / "votes.csv"
            with open(votes_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['id', 'bill_id'])
                writer.writeheader()
                writer.writerow({'id': '1', 'bill_id': '10'})
                writer.writerow({'id': '2', 'bill_id': '20'})
            
            repo = LegislatorsRepository(
                datasets_path=tmpdir,
                datasets_input_path=str(input_dir),
                datasets_output_path=str(Path(tmpdir) / "output")
            )
            
            votes = repo.get_all_votes()
            
            assert len(votes) == 2
            assert votes[0].id == 1
            assert votes[0].bill_id == 10
            assert votes[1].id == 2
            assert votes[1].bill_id == 20
    
    def test_save_legislator_vote_counts(self):
        """Test saving legislator vote counts to CSV"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            
            repo = LegislatorsRepository(
                datasets_path=tmpdir,
                datasets_input_path=str(Path(tmpdir) / "input"),
                datasets_output_path=str(output_dir)
            )
            
            vote_counts = [
                LegislatorVoteCount(id=1, name="John Doe", num_supported_bills=5, num_opposed_bills=3),
                LegislatorVoteCount(id=2, name="Jane Smith", num_supported_bills=2, num_opposed_bills=1)
            ]
            
            repo.save_legislator_vote_counts(vote_counts, "legislators-support-oppose-count.csv")
            
            output_file = output_dir / "legislators-support-oppose-count.csv"
            assert output_file.exists()
            
            with open(output_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                assert len(rows) == 2
                assert rows[0]['id'] == '1'
                assert rows[0]['name'] == 'John Doe'
                assert rows[0]['num_supported_bills'] == '5'
                assert rows[0]['num_opposed_bills'] == '3'
                assert rows[1]['id'] == '2'
                assert rows[1]['name'] == 'Jane Smith'
    
    def test_save_bill_vote_counts(self):
        """Test saving bill vote counts to CSV"""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "output"
            
            repo = LegislatorsRepository(
                datasets_path=tmpdir,
                datasets_input_path=str(Path(tmpdir) / "input"),
                datasets_output_path=str(output_dir)
            )
            
            bill_counts = [
                BillVoteCount(
                    id=1, 
                    title="Test Bill 1", 
                    supporter_count=10, 
                    opposer_count=5, 
                    primary_sponsor="John Doe"
                ),
                BillVoteCount(
                    id=2, 
                    title="Test Bill 2", 
                    supporter_count=8, 
                    opposer_count=12, 
                    primary_sponsor="Jane Smith"
                )
            ]
            
            repo.save_bill_vote_counts(bill_counts, "bills.csv")
            
            output_file = output_dir / "bills.csv"
            assert output_file.exists()
            
            with open(output_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                
                assert len(rows) == 2
                assert rows[0]['id'] == '1'
                assert rows[0]['title'] == 'Test Bill 1'
                assert rows[0]['supporter_count'] == '10'
                assert rows[0]['opposer_count'] == '5'
                assert rows[0]['primary_sponsor'] == 'John Doe'
                assert rows[1]['id'] == '2'
                assert rows[1]['title'] == 'Test Bill 2'
