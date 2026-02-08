"""
HSP Registry Contract ABI
"""

HSP_REGISTRY_ABI = [
    {
        "inputs": [{"name": "agent", "type": "address"}, {"name": "policyHash", "type": "bytes32"}],
        "name": "registerAgent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "agent", "type": "address"}, {"name": "reason", "type": "string"}],
        "name": "revokeAgent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "actionHash", "type": "bytes32"}, {"name": "metadata", "type": "string"}],
        "name": "requestAction",
        "outputs": [{"name": "", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "actionId", "type": "bytes32"}, {"name": "signature", "type": "bytes"}],
        "name": "approveAction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "actionId", "type": "bytes32"}, {"name": "reason", "type": "string"}],
        "name": "rejectAction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "actionId", "type": "bytes32"}],
        "name": "executeAction",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"name": "actionId", "type": "bytes32"}],
        "name": "isActionApproved",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "actionId", "type": "bytes32"}],
        "name": "getAction",
        "outputs": [
            {"name": "", "type": "bytes32"},
            {"name": "", "type": "address"},
            {"name": "", "type": "uint256"},
            {"name": "", "type": "uint256"},
            {"name": "", "type": "uint256"},
            {"name": "", "type": "address"},
            {"name": "", "type": "bytes32"},
            {"name": "", "type": "uint8"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "actionId", "type": "bytes32"}],
        "name": "getProofOfSupervision",
        "outputs": [
            {"name": "", "type": "bytes32"},
            {"name": "", "type": "address"},
            {"name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"name": "", "type": "address"}],
        "name": "agents",
        "outputs": [
            {"name": "", "type": "bool"},
            {"name": "", "type": "bytes32"},
            {"name": "", "type": "uint256"},
            {"name": "", "type": "uint256"},
            {"name": "", "type": "uint256"},
            {"name": "", "type": "uint256"},
            {"name": "", "type": "bool"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "actionId", "type": "bytes32"},
            {"indexed": True, "name": "agent", "type": "address"},
            {"indexed": False, "name": "actionHash", "type": "bytes32"}
        ],
        "name": "ActionRequested",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "actionId", "type": "bytes32"},
            {"indexed": True, "name": "supervisor", "type": "address"},
            {"indexed": False, "name": "proofHash", "type": "bytes32"}
        ],
        "name": "ActionApproved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "actionId", "type": "bytes32"},
            {"indexed": True, "name": "supervisor", "type": "address"},
            {"indexed": False, "name": "reason", "type": "string"}
        ],
        "name": "ActionRejected",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "actionId", "type": "bytes32"},
            {"indexed": False, "name": "timestamp", "type": "uint256"}
        ],
        "name": "ActionExecuted",
        "type": "event"
    }
]
