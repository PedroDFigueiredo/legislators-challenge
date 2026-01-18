from dataclasses import dataclass


@dataclass
class Bill:
    """Represents a bill"""
    id: int
    title: str
    sponsor_id: int


@dataclass
class Legislator:
    """Represents a legislator"""
    id: int
    name: str


@dataclass
class VoteResult:
    """Represents a vote result"""
    id: int
    legislator_id: int
    vote_id: int
    vote_type: int


@dataclass
class Vote:
    """Represents a vote"""
    id: int
    bill_id: int


@dataclass
class LegislatorVoteCount:
    """Represents vote counts for a legislator"""
    id: int
    name: str
    num_supported_bills: int
    num_opposed_bills: int
