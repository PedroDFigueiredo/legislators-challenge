from repositories import LegislatorsRepository
from services import legislators_support_oppose_count


def main():
    """Main function to demonstrate repository usage"""
    # Initialize the repository
    repository = LegislatorsRepository()
    
    # Get all data from CSV files
    bills = repository.get_all_bills()
    legislators = repository.get_all_legislators()
    vote_results = repository.get_all_vote_results()
    votes = repository.get_all_votes()
    

    # Display summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Bills: {len(bills)}")
    print(f"Total Legislators: {len(legislators)}")
    print(f"Total Votes: {len(votes)}")
    print(f"Total Vote Results: {len(vote_results)}")


    # execute the support count operation
    legislators_count = legislators_support_oppose_count(legislators, vote_results)

    # persist the support count data
    repository.save_legislator_vote_counts(legislators_count)

    print(legislators_count)

    


if __name__ == "__main__":
    main()
