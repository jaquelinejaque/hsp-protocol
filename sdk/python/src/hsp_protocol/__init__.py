"""
HSP Protocol Python SDK

Human Supervision Protocol - Fail-Closed Execution Layer for AI

Patent Notice: PCT/US26/11908
Commercial use requires licensing. See PATENTS.md
"""

from .client import HSPClient
from .types import ActionStatus, ActionDetails, ProofOfSupervision, AgentInfo

__version__ = "1.0.0"
__all__ = [
    "HSPClient",
    "ActionStatus",
    "ActionDetails",
    "ProofOfSupervision",
    "AgentInfo",
]
