"""
HSP Protocol Client

Main interface for interacting with the Human Supervision Protocol.
"""

import json
import time
from dataclasses import dataclass
from typing import Optional, Callable, Any
from web3 import Web3
from eth_account import Account
from eth_account.messages import encode_defunct

from .types import ActionStatus, ActionDetails, ProofOfSupervision, AgentInfo
from .abi import HSP_REGISTRY_ABI


# Deployed contract addresses
CONTRACTS = {
    "polygon": "0x1BCe4baE2E9e192EE906742a939FaFaec50A1B4e",
    "polygon_amoy": "",  # Coming soon
    "ethereum": "",      # Coming soon
}

# Default RPC endpoints
RPC_ENDPOINTS = {
    "polygon": "https://polygon-rpc.com",
    "polygon_amoy": "https://rpc-amoy.polygon.technology",
    "ethereum": "https://eth.llamarpc.com",
}


@dataclass
class ActionRequest:
    """Request for supervised action"""
    type: str
    data: dict
    justification: Optional[str] = None
    metadata: Optional[str] = None


class HSPClient:
    """
    HSP Client - Main interface for the Human Supervision Protocol

    Example:
        ```python
        from hsp_protocol import HSPClient

        hsp = HSPClient(
            network="polygon",
            private_key="0x..."
        )

        action = hsp.request_action(ActionRequest(
            type="FINANCIAL_TRANSFER",
            data={"amount": 50000, "recipient": "0x..."},
            justification="Quarterly vendor payment"
        ))
        ```
    """

    def __init__(
        self,
        network: str = "polygon",
        contract_address: Optional[str] = None,
        rpc_url: Optional[str] = None,
        private_key: Optional[str] = None
    ):
        """
        Initialize HSP Client

        Args:
            network: Network name (polygon, ethereum, etc.)
            contract_address: Override default contract address
            rpc_url: Override default RPC endpoint
            private_key: Private key for signing transactions
        """
        self.network = network
        self.contract_address = contract_address or CONTRACTS.get(network, "")

        if not self.contract_address:
            raise ValueError(f"Network {network} not yet supported")

        rpc = rpc_url or RPC_ENDPOINTS.get(network, "")
        if not rpc:
            raise ValueError(f"No RPC endpoint for network {network}")

        self.w3 = Web3(Web3.HTTPProvider(rpc))

        if private_key:
            self.account = Account.from_key(private_key)
        else:
            self.account = None

        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=HSP_REGISTRY_ABI
        )

    def request_action(self, request: ActionRequest) -> ActionDetails:
        """
        Request supervision for an action (FAIL-CLOSED)

        The action is blocked until a human supervisor approves it.

        Args:
            request: ActionRequest with type, data, and justification

        Returns:
            ActionDetails with status PENDING
        """
        if not self.account:
            raise ValueError("Private key required for write operations")

        # Create action hash
        action_data = json.dumps({
            "type": request.type,
            "data": request.data,
            "justification": request.justification,
            "timestamp": int(time.time() * 1000)
        }, sort_keys=True)
        action_hash = Web3.keccak(text=action_data)

        metadata = request.metadata or ""

        # Build transaction
        tx = self.contract.functions.requestAction(
            action_hash,
            metadata
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 200000,
            "gasPrice": self.w3.eth.gas_price
        })

        # Sign and send
        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        # Extract action ID from events
        logs = self.contract.events.ActionRequested().process_receipt(receipt)
        if not logs:
            raise ValueError("ActionRequested event not found")

        action_id = logs[0]["args"]["actionId"]
        return self.get_action(action_id.hex())

    def approve_action(self, action_id: str) -> ProofOfSupervision:
        """
        Approve a pending action (Human Supervisor)

        Args:
            action_id: ID of the action to approve

        Returns:
            ProofOfSupervision with cryptographic proof
        """
        if not self.account:
            raise ValueError("Private key required for approval")

        # Sign action ID as proof
        action_bytes = bytes.fromhex(action_id.replace("0x", ""))
        message = encode_defunct(action_bytes)
        signed = self.account.sign_message(message)
        signature = signed.signature

        # Build transaction
        tx = self.contract.functions.approveAction(
            bytes.fromhex(action_id.replace("0x", "")),
            signature
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 150000,
            "gasPrice": self.w3.eth.gas_price
        })

        # Sign and send
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return self.get_proof_of_supervision(action_id)

    def reject_action(self, action_id: str, reason: str) -> None:
        """
        Reject a pending action

        Args:
            action_id: ID of the action to reject
            reason: Reason for rejection
        """
        if not self.account:
            raise ValueError("Private key required for rejection")

        tx = self.contract.functions.rejectAction(
            bytes.fromhex(action_id.replace("0x", "")),
            reason
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 100000,
            "gasPrice": self.w3.eth.gas_price
        })

        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

    def execute_action(self, action_id: str) -> ActionDetails:
        """
        Execute an approved action

        Args:
            action_id: ID of the action to execute

        Returns:
            ActionDetails with status EXECUTED
        """
        if not self.account:
            raise ValueError("Private key required for execution")

        tx = self.contract.functions.executeAction(
            bytes.fromhex(action_id.replace("0x", ""))
        ).build_transaction({
            "from": self.account.address,
            "nonce": self.w3.eth.get_transaction_count(self.account.address),
            "gas": 100000,
            "gasPrice": self.w3.eth.gas_price
        })

        signed = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
        self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return self.get_action(action_id)

    def get_action(self, action_id: str) -> ActionDetails:
        """Get action details"""
        result = self.contract.functions.getAction(
            bytes.fromhex(action_id.replace("0x", ""))
        ).call()

        return ActionDetails(
            action_id=action_id,
            action_hash="0x" + result[0].hex(),
            agent=result[1],
            requested_at=result[2],
            approved_at=result[3] if result[3] > 0 else None,
            executed_at=result[4] if result[4] > 0 else None,
            supervisor=result[5] if result[5] != "0x" + "0" * 40 else None,
            proof_hash="0x" + result[6].hex() if result[6] != b"\x00" * 32 else None,
            status=ActionStatus(result[7])
        )

    def is_action_approved(self, action_id: str) -> bool:
        """Check if action is approved"""
        return self.contract.functions.isActionApproved(
            bytes.fromhex(action_id.replace("0x", ""))
        ).call()

    def get_proof_of_supervision(self, action_id: str) -> ProofOfSupervision:
        """Get proof of supervision for approved action"""
        result = self.contract.functions.getProofOfSupervision(
            bytes.fromhex(action_id.replace("0x", ""))
        ).call()

        return ProofOfSupervision(
            proof_hash="0x" + result[0].hex(),
            supervisor=result[1],
            approved_at=result[2],
            action_id=action_id
        )

    def get_agent(self, address: str) -> AgentInfo:
        """Get agent information"""
        result = self.contract.functions.agents(
            Web3.to_checksum_address(address)
        ).call()

        return AgentInfo(
            is_registered=result[0],
            policy_hash="0x" + result[1].hex(),
            registered_at=result[2],
            actions_requested=result[3],
            actions_approved=result[4],
            actions_rejected=result[5],
            is_active=result[6]
        )
