import pytest
from services import legislators_support_oppose_count, bills_support_oppose_count
from models import Legislator, VoteResult, Bill, Vote, LegislatorVoteCount, BillVoteCount


class TestLegislatorsSupportOpposeCount:
    """Tests for legislators_support_oppose_count service"""
    
    def test_count_support_and_oppose_votes(self):
        """Test counting support and oppose votes for legislators"""
        legislators = [
            Legislator(id=1, name="John Doe"),
            Legislator(id=2, name="Jane Smith")
        ]
        vote_results = [
            VoteResult(id=1, legislator_id=1, vote_id=1, vote_type=1),  # support
            VoteResult(id=2, legislator_id=1, vote_id=2, vote_type=1),  # support
            VoteResult(id=3, legislator_id=1, vote_id=3, vote_type=2),  # oppose
            VoteResult(id=4, legislator_id=2, vote_id=1, vote_type=2),  # oppose
            VoteResult(id=5, legislator_id=2, vote_id=2, vote_type=2),  # oppose
        ]
        
        result = legislators_support_oppose_count(legislators, vote_results)
        
        assert len(result) == 2
        assert result[0].id == 1
        assert result[0].name == "John Doe"
        assert result[0].num_supported_bills == 2
        assert result[0].num_opposed_bills == 1
        
        assert result[1].id == 2
        assert result[1].name == "Jane Smith"
        assert result[1].num_supported_bills == 0
        assert result[1].num_opposed_bills == 2
    
    def test_legislator_with_no_votes(self):
        """Test legislator with no vote results"""
        legislators = [
            Legislator(id=1, name="John Doe"),
            Legislator(id=2, name="Jane Smith")
        ]
        vote_results = [
            VoteResult(id=1, legislator_id=1, vote_id=1, vote_type=1)
        ]
        
        result = legislators_support_oppose_count(legislators, vote_results)
        
        # Only legislator 1 should appear in results
        assert len(result) == 1
        assert result[0].id == 1
        assert result[0].num_supported_bills == 1
        assert result[0].num_opposed_bills == 0
    
    def test_unknown_legislator_id(self):
        """Test handling of vote results with unknown legislator ID"""
        legislators = [
            Legislator(id=1, name="John Doe")
        ]
        vote_results = [
            VoteResult(id=1, legislator_id=999, vote_id=1, vote_type=1)
        ]
        
        result = legislators_support_oppose_count(legislators, vote_results)
        
        assert len(result) == 1
        assert result[0].id == 999
        assert "Unknown" in result[0].name


class TestBillsSupportOpposeCount:
    """Tests for bills_support_oppose_count service"""
    
    def test_count_support_and_oppose_for_bills(self):
        """Test counting support and oppose votes for bills"""
        bills = [
            Bill(id=1, title="Bill 1", sponsor_id=1),
            Bill(id=2, title="Bill 2", sponsor_id=2)
        ]
        votes = [
            Vote(id=1, bill_id=1),
            Vote(id=2, bill_id=1),
            Vote(id=3, bill_id=2)
        ]
        vote_results = [
            VoteResult(id=1, legislator_id=1, vote_id=1, vote_type=1),  # support bill 1
            VoteResult(id=2, legislator_id=2, vote_id=1, vote_type=1),  # support bill 1
            VoteResult(id=3, legislator_id=3, vote_id=1, vote_type=2),  # oppose bill 1
            VoteResult(id=4, legislator_id=1, vote_id=2, vote_type=2),  # oppose bill 1 (vote 2)
            VoteResult(id=5, legislator_id=2, vote_id=3, vote_type=1),  # support bill 2
        ]
        legislators = [
            Legislator(id=1, name="John Doe"),
            Legislator(id=2, name="Jane Smith")
        ]
        
        result = bills_support_oppose_count(bills, votes, vote_results, legislators)
        
        assert len(result) == 2
        
        # Bill 1: 2 support, 2 oppose (across votes 1 and 2)
        bill1 = next(b for b in result if b.id == 1)
        assert bill1.title == "Bill 1"
        assert bill1.supporter_count == 2
        assert bill1.opposer_count == 2
        assert bill1.primary_sponsor == "John Doe"
        
        # Bill 2: 1 support, 0 oppose
        bill2 = next(b for b in result if b.id == 2)
        assert bill2.title == "Bill 2"
        assert bill2.supporter_count == 1
        assert bill2.opposer_count == 0
        assert bill2.primary_sponsor == "Jane Smith"
    
    def test_bill_with_no_votes(self):
        """Test bill with no associated votes"""
        bills = [
            Bill(id=1, title="Bill 1", sponsor_id=1)
        ]
        votes = []
        vote_results = []
        legislators = [
            Legislator(id=1, name="John Doe")
        ]
        
        result = bills_support_oppose_count(bills, votes, vote_results, legislators)
        
        assert len(result) == 1
        assert result[0].supporter_count == 0
        assert result[0].opposer_count == 0
    
    def test_unknown_sponsor_id(self):
        """Test handling of bill with unknown sponsor ID"""
        bills = [
            Bill(id=1, title="Bill 1", sponsor_id=999)
        ]
        votes = []
        vote_results = []
        legislators = [
            Legislator(id=1, name="John Doe")
        ]
        
        result = bills_support_oppose_count(bills, votes, vote_results, legislators)
        
        assert len(result) == 1
        assert result[0].primary_sponsor == "Unknown"
