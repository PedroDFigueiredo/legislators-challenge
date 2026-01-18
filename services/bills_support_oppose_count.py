from typing import List, Dict

from models import Bill, Vote, VoteResult, Legislator, BillVoteCount


def bills_support_oppose_count(
    bills: List[Bill],
    votes: List[Vote],
    vote_results: List[VoteResult],
    legislators: List[Legislator]
) -> List[BillVoteCount]:
    """
    Count support and oppose votes for each bill and identify primary sponsor
    
    Args:
        bills: List of Bill instances
        votes: List of Vote instances
        vote_results: List of VoteResult instances
        legislators: List of Legislator instances
        
    Returns:
        List of BillVoteCount instances with support/oppose counts
        and primary sponsor for each bill
        
    Note:
        vote_type 1 = Support
        vote_type 2 = Oppose
    """
    # Create maps for efficient lookups
    legislator_map = {legislator.id: legislator.name for legislator in legislators}
    vote_map: Dict[int, List[int]] = {}  # bill_id -> list of vote_ids
    
    # Build map of bill_id to vote_ids
    for vote in votes:
        if vote.bill_id not in vote_map:
            vote_map[vote.bill_id] = []
        vote_map[vote.bill_id].append(vote.id)
    
    # Create map of vote_id to vote results for efficient lookup
    vote_results_map: Dict[int, List[VoteResult]] = {}
    for vote_result in vote_results:
        if vote_result.vote_id not in vote_results_map:
            vote_results_map[vote_result.vote_id] = []
        vote_results_map[vote_result.vote_id].append(vote_result)
    
    # Process each bill
    result = []
    for bill in bills:
        supporter_count = 0
        opposer_count = 0
        
        # Get all votes for this bill
        bill_vote_ids = vote_map.get(bill.id, [])
        
        # Count support and oppose votes across all votes for this bill
        for vote_id in bill_vote_ids:
            vote_result_list = vote_results_map.get(vote_id, [])
            for vote_result in vote_result_list:
                if vote_result.vote_type == 1:
                    supporter_count += 1
                elif vote_result.vote_type == 2:
                    opposer_count += 1
        
        # Get primary sponsor name
        primary_sponsor = legislator_map.get(
            bill.sponsor_id, 
            f"Unknown (ID: {bill.sponsor_id})"
        )
        
        result.append(
            BillVoteCount(
                id=bill.id,
                title=bill.title,
                supporter_count=supporter_count,
                opposer_count=opposer_count,
                primary_sponsor=primary_sponsor
            )
        )
    
    # Sort by id for consistent output
    result.sort(key=lambda x: x.id)
    
    return result
