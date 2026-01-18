# Legislators Challenge

A Python application that processes legislator voting data to calculate support and oppose counts for both legislators and bills.

## Overview

This project analyzes voting data from CSV files to generate two main reports:
1. **Legislator Vote Counts**: For each legislator, counts how many bills they supported and opposed
2. **Bill Vote Counts**: For each bill, counts how many legislators supported and opposed it, along with the primary sponsor information

## Project Structure

```
legislators-challenge/
├── datasets/
│   ├── input/          # Input CSV files
│   │   ├── bills.csv
│   │   ├── legislators.csv
│   │   ├── vote_results.csv
│   │   └── votes.csv
│   └── output/         # Generated output CSV files
│       ├── bills.csv
│       └── bills.csv
├── models/             # Data models (dataclasses)
│   ├── __init__.py
│   └── models.py
├── repositories/       # Data access layer
│   ├── __init__.py
│   └── legislators_orm.py
├── services/           # Business logic
│   ├── __init__.py
│   ├── legislators_support_oppose_count.py
│   └── bills_support_oppose_count.py
├── tests/              # Test suite
│   ├── __init__.py
│   ├── test_services.py
│   ├── test_repositories.py
│   └── test_main.py
└── main.py            # Entry point
```

## Requirements

- Python 3.7+ (uses dataclasses and type hints)
- No external dependencies for running the application (uses only Python standard library)
- pytest (optional, for running tests): `pip install pytest`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd legislators-challenge
```

2. Ensure you have Python 3.7 or higher installed:
```bash
python --version
```

3. (Optional) Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Usage

1. Ensure your input CSV files are in the `datasets/input/` directory:
   - `bills.csv` - Contains bill information (id, title, sponsor_id)
   - `legislators.csv` - Contains legislator information (id, name)
   - `votes.csv` - Contains vote information (id, bill_id)
   - `vote_results.csv` - Contains vote results (id, legislator_id, vote_id, vote_type)

2. Run the main script:
```bash
python main.py
```

3. The output CSV files will be generated in `datasets/output/`:
   - `bills.csv` - Contains legislator vote counts
   - `bills.csv` - Contains bill vote counts

## Architecture

The project follows a clean architecture pattern with clear separation of concerns:

- **Models** (`models/`): Data classes representing domain entities
  - `Bill`, `Legislator`, `Vote`, `VoteResult`
  - `LegislatorVoteCount`, `BillVoteCount` (result models)

- **Repositories** (`repositories/`): Data access layer
  - `LegislatorsRepository`: Handles reading from and writing to CSV files

- **Services** (`services/`): Business logic
  - `legislators_support_oppose_count()`: Calculates vote counts per legislator
  - `bills_support_oppose_count()`: Calculates vote counts per bill

- **Main** (`main.py`): Orchestrates the application flow

## How It Works

1. **Data Loading**: The repository reads all CSV files from `datasets/input/` and converts them into dataclass instances
2. **Legislator Analysis**: Counts how many times each legislator voted "Support" (vote_type=1) or "Oppose" (vote_type=2)
3. **Bill Analysis**: For each bill, counts total supporters and opposers across all votes, and identifies the primary sponsor
4. **Data Persistence**: Results are saved as CSV files in `datasets/output/`

## Example Output

When you run `main.py`, you'll see a summary like:

```
============================================================
SUMMARY
============================================================
Total Bills: 2
Total Legislators: 20
Total Votes: 2
Total Vote Results: 19
```

## Testing

The project includes comprehensive tests for all components. Tests are located in the `tests/` directory.

### Running Tests

1. Install pytest (if not already installed):
```bash
pip install pytest
```

2. Run all tests:
```bash
pytest tests/ -v
```

3. Run specific test files:
```bash
pytest tests/test_services.py -v
pytest tests/test_repositories.py -v
pytest tests/test_main.py -v
```

### Test Coverage

The test suite includes:

- **Service Tests** (`tests/test_services.py`):
  - `legislators_support_oppose_count()`: Tests vote counting logic, edge cases, and unknown legislator handling
  - `bills_support_oppose_count()`: Tests bill vote counting, sponsor identification, and edge cases

- **Repository Tests** (`tests/test_repositories.py`):
  - CSV reading operations: `get_all_bills()`, `get_all_legislators()`, `get_all_votes()`, `get_all_vote_results()`
  - CSV writing operations: `save_legislator_vote_counts()`, `save_bill_vote_counts()`
  - All tests use temporary directories to avoid modifying actual data files

- **Main Function Tests** (`tests/test_main.py`):
  - Verifies the complete execution flow
  - Tests that all repository and service methods are called correctly
  - Validates summary statistics display

All tests use mocking and temporary files to ensure isolation and avoid dependencies on actual CSV data.

## Development

The codebase uses:
- Type hints for better code clarity
- Dataclasses for clean data modeling
- CSV module from standard library for file I/O
- Pathlib for path handling
- pytest for testing
