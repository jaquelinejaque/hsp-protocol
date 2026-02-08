"""
HSP Protocol Types
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import Optional


class ActionStatus(IntEnum):
    """Status of an action in the HSP system"""
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    EXECUTED = 3
    EXPIRED = 4


@dataclass
class ActionDetails:
    """Details of an action"""
    action_id: str
    action_hash: str
    agent: str
    requested_at: int
    approved_at: Optional[int]
    executed_at: Optional[int]
    supervisor: Optional[str]
    proof_hash: Optional[str]
    status: ActionStatus


@dataclass
class ProofOfSupervision:
    """Cryptographic proof of human supervision"""
    proof_hash: str
    supervisor: str
    approved_at: int
    action_id: str


@dataclass
class AgentInfo:
    """Information about a registered agent"""
    is_registered: bool
    policy_hash: str
    registered_at: int
    actions_requested: int
    actions_approved: int
    actions_rejected: int
    is_active: bool
