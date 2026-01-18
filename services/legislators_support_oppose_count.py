from typing import List, Dict

from models import Legislator, VoteResult, LegislatorVoteCount


def legislators_support_oppose_count(
    legislators: List[Legislator],
    vote_results: List[VoteResult]
) -> List[LegislatorVoteCount]:
    """
    Count support and oppose votes for each legislator
    
    Args:
        legislators: List of Legislator instances
        vote_results: List of VoteResult instances
        
    Returns:
        List of LegislatorVoteCount instances with support/oppose counts
        for each legislator
        
    Note:
        vote_type 1 = Support
        vote_type 2 = Oppose
    """
    # Create a dictionary to map legislator_id to legislator name
    legislator_map = {legislator.id: legislator.name for legislator in legislators}
    
    # Initialize vote counts for each legislator
    vote_counts: Dict[int, Dict[str, int]] = {}
    
    # Count votes for each legislator
    for vote_result in vote_results:
        legislator_id = vote_result.legislator_id
        
        # Initialize if not exists
        if legislator_id not in vote_counts:
            vote_counts[legislator_id] = {
                'supported': 0,
                'opposed': 0
            }
        
        # Count based on vote_type
        if vote_result.vote_type == 1:
            vote_counts[legislator_id]['supported'] += 1
        elif vote_result.vote_type == 2:
            vote_counts[legislator_id]['opposed'] += 1
    
    # Build result list
    result = []
    for legislator_id, counts in vote_counts.items():
        legislator_name = legislator_map.get(legislator_id, f"Unknown (ID: {legislator_id})")
        result.append(
            LegislatorVoteCount(
                id=legislator_id,
                name=legislator_name,
                num_supported_bills=counts['supported'],
                num_opposed_bills=counts['opposed']
            )
        )
    
    return result
