import pytest
from unittest.mock import Mock, patch
from main import main
from repositories import LegislatorsRepository
from models import Bill, Legislator, VoteResult, Vote, LegislatorVoteCount, BillVoteCount


class TestMain:
    """Tests for main function"""
    
    @patch('main.LegislatorsRepository')
    @patch('main.legislators_support_oppose_count')
    @patch('main.bills_support_oppose_count')
    def test_main_execution_flow(self, mock_bills_count, mock_legislators_count, mock_repo_class):
        """Test that main function executes the complete flow"""
        # Setup mock repository
        mock_repo = Mock(spec=LegislatorsRepository)
        mock_repo_class.return_value = mock_repo
        
        # Setup mock data
        mock_bills = [Bill(id=1, title="Test Bill", sponsor_id=1)]
        mock_legislators = [Legislator(id=1, name="John Doe")]
        mock_vote_results = [VoteResult(id=1, legislator_id=1, vote_id=1, vote_type=1)]
        mock_votes = [Vote(id=1, bill_id=1)]
        
        mock_repo.get_all_bills.return_value = mock_bills
        mock_repo.get_all_legislators.return_value = mock_legislators
        mock_repo.get_all_vote_results.return_value = mock_vote_results
        mock_repo.get_all_votes.return_value = mock_votes
        
        # Setup mock service results
        mock_legislator_counts = [
            LegislatorVoteCount(id=1, name="John Doe", num_supported_bills=5, num_opposed_bills=3)
        ]
        mock_bill_counts = [
            BillVoteCount(id=1, title="Test Bill", supporter_count=10, opposer_count=5, primary_sponsor="John Doe")
        ]
        
        mock_legislators_count.return_value = mock_legislator_counts
        mock_bills_count.return_value = mock_bill_counts
        
        # Execute main
        main()
        
        # Verify repository methods were called
        mock_repo.get_all_bills.assert_called_once()
        mock_repo.get_all_legislators.assert_called_once()
        mock_repo.get_all_vote_results.assert_called_once()
        mock_repo.get_all_votes.assert_called_once()
        
        # Verify service functions were called with correct arguments
        mock_legislators_count.assert_called_once_with(mock_legislators, mock_vote_results)
        mock_bills_count.assert_called_once_with(mock_bills, mock_votes, mock_vote_results, mock_legislators)
        
        # Verify save methods were called
        mock_repo.save_legislator_vote_counts.assert_called_once_with(mock_legislator_counts)
        mock_repo.save_bill_vote_counts.assert_called_once_with(mock_bill_counts)
    
    @patch('main.LegislatorsRepository')
    @patch('main.legislators_support_oppose_count')
    @patch('main.bills_support_oppose_count')
    @patch('builtins.print')
    def test_main_displays_summary(self, mock_print, mock_bills_count, mock_legislators_count, mock_repo_class):
        """Test that main function displays summary statistics"""
        # Setup mock repository
        mock_repo = Mock(spec=LegislatorsRepository)
        mock_repo_class.return_value = mock_repo
        
        # Setup mock data
        mock_bills = [Bill(id=1, title="Bill 1", sponsor_id=1), Bill(id=2, title="Bill 2", sponsor_id=2)]
        mock_legislators = [Legislator(id=1, name="John Doe")]
        mock_vote_results = [VoteResult(id=1, legislator_id=1, vote_id=1, vote_type=1)]
        mock_votes = [Vote(id=1, bill_id=1)]
        
        mock_repo.get_all_bills.return_value = mock_bills
        mock_repo.get_all_legislators.return_value = mock_legislators
        mock_repo.get_all_vote_results.return_value = mock_vote_results
        mock_repo.get_all_votes.return_value = mock_votes
        
        mock_legislators_count.return_value = []
        mock_bills_count.return_value = []
        
        # Execute main
        main()
        
        # Verify summary was printed
        print_calls = [str(call) for call in mock_print.call_args_list]
        summary_printed = any("SUMMARY" in str(call) for call in print_calls)
        assert summary_printed, "Summary should be printed"
        
        # Verify counts are displayed
        total_bills_printed = any("Total Bills: 2" in str(call) for call in print_calls)
        assert total_bills_printed, "Total bills count should be printed"
