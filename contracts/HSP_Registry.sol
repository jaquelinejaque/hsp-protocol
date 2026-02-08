// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.19;

/**
 * @title HSP Registry - Human Supervision Protocol
 * @author HSP Protocol Team
 * @notice Core registry contract for the Human Supervision Protocol
 * @dev Implements fail-closed execution and proof of supervision
 *
 * Patent Notice: PCT/US26/11908
 * Commercial use requires licensing. See PATENTS.md
 */

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract HSPRegistry is Ownable, ReentrancyGuard {
    using ECDSA for bytes32;

    // ============ Events ============

    event AgentRegistered(address indexed agent, bytes32 policyHash, uint256 timestamp);
    event AgentRevoked(address indexed agent, string reason, uint256 timestamp);
    event ActionRequested(bytes32 indexed actionId, address indexed agent, bytes32 actionHash);
    event ActionApproved(bytes32 indexed actionId, address indexed supervisor, bytes32 proofHash);
    event ActionRejected(bytes32 indexed actionId, address indexed supervisor, string reason);
    event ActionExecuted(bytes32 indexed actionId, uint256 timestamp);
    event SupervisorAdded(address indexed supervisor, uint8 level);
    event SupervisorRemoved(address indexed supervisor);
    event PolicyUpdated(address indexed agent, bytes32 newPolicyHash);

    // ============ Structs ============

    struct Agent {
        bool isRegistered;
        bytes32 policyHash;
        uint256 registeredAt;
        uint256 actionsRequested;
        uint256 actionsApproved;
        uint256 actionsRejected;
        bool isActive;
    }

    struct Action {
        bytes32 actionHash;
        address agent;
        uint256 requestedAt;
        uint256 approvedAt;
        uint256 executedAt;
        address supervisor;
        bytes32 proofHash;
        ActionStatus status;
        string metadata;
    }

    struct Supervisor {
        bool isActive;
        uint8 level; // 1-5, higher = more authority
        uint256 actionsApproved;
        uint256 actionsRejected;
    }

    // ============ Enums ============

    enum ActionStatus {
        Pending,
        Approved,
        Rejected,
        Executed,
        Expired
    }

    // ============ State Variables ============

    mapping(address => Agent) public agents;
    mapping(bytes32 => Action) public actions;
    mapping(address => Supervisor) public supervisors;

    uint256 public actionTimeout = 24 hours;
    uint256 public totalActions;
    uint256 public protocolFeeRate = 10; // 0.1% = 10 basis points
    address public treasury;

    bytes32[] public actionHistory;

    // ============ Modifiers ============

    modifier onlyRegisteredAgent() {
        require(agents[msg.sender].isRegistered && agents[msg.sender].isActive,
            "HSP: Not a registered active agent");
        _;
    }

    modifier onlySupervisor() {
        require(supervisors[msg.sender].isActive, "HSP: Not an active supervisor");
        _;
    }

    modifier onlySupervisorLevel(uint8 minLevel) {
        require(supervisors[msg.sender].isActive, "HSP: Not an active supervisor");
        require(supervisors[msg.sender].level >= minLevel, "HSP: Insufficient supervisor level");
        _;
    }

    // ============ Constructor ============

    constructor(address _treasury) {
        treasury = _treasury;
        // Owner is default Level 5 supervisor
        supervisors[msg.sender] = Supervisor({
            isActive: true,
            level: 5,
            actionsApproved: 0,
            actionsRejected: 0
        });
        emit SupervisorAdded(msg.sender, 5);
    }

    // ============ Agent Management ============

    /**
     * @notice Register a new AI agent in the HSP system
     * @param agent Address of the agent to register
     * @param policyHash Hash of the agent's policy document (stored off-chain)
     */
    function registerAgent(address agent, bytes32 policyHash) external onlyOwner {
        require(!agents[agent].isRegistered, "HSP: Agent already registered");
        require(agent != address(0), "HSP: Invalid agent address");

        agents[agent] = Agent({
            isRegistered: true,
            policyHash: policyHash,
            registeredAt: block.timestamp,
            actionsRequested: 0,
            actionsApproved: 0,
            actionsRejected: 0,
            isActive: true
        });

        emit AgentRegistered(agent, policyHash, block.timestamp);
    }

    /**
     * @notice Revoke an agent's registration
     * @param agent Address of the agent to revoke
     * @param reason Reason for revocation
     */
    function revokeAgent(address agent, string calldata reason) external onlyOwner {
        require(agents[agent].isRegistered, "HSP: Agent not registered");
        agents[agent].isActive = false;
        emit AgentRevoked(agent, reason, block.timestamp);
    }

    /**
     * @notice Update an agent's policy
     * @param agent Address of the agent
     * @param newPolicyHash New policy hash
     */
    function updatePolicy(address agent, bytes32 newPolicyHash) external onlyOwner {
        require(agents[agent].isRegistered, "HSP: Agent not registered");
        agents[agent].policyHash = newPolicyHash;
        emit PolicyUpdated(agent, newPolicyHash);
    }

    // ============ Action Workflow (Core HSP Logic) ============

    /**
     * @notice Request supervision for an action (FAIL-CLOSED: action is blocked until approved)
     * @param actionHash Hash of the action details (stored off-chain)
     * @param metadata Optional metadata string
     * @return actionId Unique identifier for this action request
     */
    function requestAction(bytes32 actionHash, string calldata metadata)
        external
        onlyRegisteredAgent
        returns (bytes32 actionId)
    {
        actionId = keccak256(abi.encodePacked(
            msg.sender,
            actionHash,
            block.timestamp,
            totalActions
        ));

        require(actions[actionId].requestedAt == 0, "HSP: Action ID collision");

        actions[actionId] = Action({
            actionHash: actionHash,
            agent: msg.sender,
            requestedAt: block.timestamp,
            approvedAt: 0,
            executedAt: 0,
            supervisor: address(0),
            proofHash: bytes32(0),
            status: ActionStatus.Pending,
            metadata: metadata
        });

        agents[msg.sender].actionsRequested++;
        totalActions++;
        actionHistory.push(actionId);

        emit ActionRequested(actionId, msg.sender, actionHash);
        return actionId;
    }

    /**
     * @notice Approve a pending action (Human Supervisor signs off)
     * @param actionId ID of the action to approve
     * @param signature Supervisor's ECDSA signature of the actionId
     */
    function approveAction(bytes32 actionId, bytes calldata signature)
        external
        onlySupervisor
        nonReentrant
    {
        Action storage action = actions[actionId];

        require(action.requestedAt != 0, "HSP: Action does not exist");
        require(action.status == ActionStatus.Pending, "HSP: Action not pending");
        require(block.timestamp <= action.requestedAt + actionTimeout, "HSP: Action expired");

        // Verify signature (proof of human supervision)
        bytes32 messageHash = keccak256(abi.encodePacked(
            "\x19Ethereum Signed Message:\n32",
            actionId
        ));
        address signer = messageHash.recover(signature);
        require(signer == msg.sender, "HSP: Invalid signature");

        // Generate proof hash (immutable audit trail)
        bytes32 proofHash = keccak256(abi.encodePacked(
            actionId,
            msg.sender,
            block.timestamp,
            signature
        ));

        action.status = ActionStatus.Approved;
        action.approvedAt = block.timestamp;
        action.supervisor = msg.sender;
        action.proofHash = proofHash;

        agents[action.agent].actionsApproved++;
        supervisors[msg.sender].actionsApproved++;

        emit ActionApproved(actionId, msg.sender, proofHash);
    }

    /**
     * @notice Reject a pending action
     * @param actionId ID of the action to reject
     * @param reason Reason for rejection
     */
    function rejectAction(bytes32 actionId, string calldata reason)
        external
        onlySupervisor
    {
        Action storage action = actions[actionId];

        require(action.requestedAt != 0, "HSP: Action does not exist");
        require(action.status == ActionStatus.Pending, "HSP: Action not pending");

        action.status = ActionStatus.Rejected;
        action.supervisor = msg.sender;

        agents[action.agent].actionsRejected++;
        supervisors[msg.sender].actionsRejected++;

        emit ActionRejected(actionId, msg.sender, reason);
    }

    /**
     * @notice Execute an approved action
     * @param actionId ID of the action to execute
     */
    function executeAction(bytes32 actionId) external nonReentrant {
        Action storage action = actions[actionId];

        require(action.status == ActionStatus.Approved, "HSP: Action not approved");
        require(msg.sender == action.agent || msg.sender == owner(),
            "HSP: Only agent or owner can execute");

        action.status = ActionStatus.Executed;
        action.executedAt = block.timestamp;

        emit ActionExecuted(actionId, block.timestamp);
    }

    // ============ Supervisor Management ============

    /**
     * @notice Add a new supervisor
     * @param supervisor Address to add as supervisor
     * @param level Supervision authority level (1-5)
     */
    function addSupervisor(address supervisor, uint8 level) external onlyOwner {
        require(level >= 1 && level <= 5, "HSP: Level must be 1-5");
        require(!supervisors[supervisor].isActive, "HSP: Already a supervisor");

        supervisors[supervisor] = Supervisor({
            isActive: true,
            level: level,
            actionsApproved: 0,
            actionsRejected: 0
        });

        emit SupervisorAdded(supervisor, level);
    }

    /**
     * @notice Remove a supervisor
     * @param supervisor Address to remove
     */
    function removeSupervisor(address supervisor) external onlyOwner {
        require(supervisors[supervisor].isActive, "HSP: Not a supervisor");
        supervisors[supervisor].isActive = false;
        emit SupervisorRemoved(supervisor);
    }

    // ============ View Functions ============

    /**
     * @notice Get action details
     * @param actionId Action ID to query
     */
    function getAction(bytes32 actionId) external view returns (
        bytes32 actionHash,
        address agent,
        uint256 requestedAt,
        uint256 approvedAt,
        uint256 executedAt,
        address supervisor,
        bytes32 proofHash,
        ActionStatus status
    ) {
        Action storage action = actions[actionId];
        return (
            action.actionHash,
            action.agent,
            action.requestedAt,
            action.approvedAt,
            action.executedAt,
            action.supervisor,
            action.proofHash,
            action.status
        );
    }

    /**
     * @notice Check if an action is approved and ready for execution
     * @param actionId Action ID to check
     */
    function isActionApproved(bytes32 actionId) external view returns (bool) {
        return actions[actionId].status == ActionStatus.Approved;
    }

    /**
     * @notice Get proof of supervision for an action
     * @param actionId Action ID to query
     */
    function getProofOfSupervision(bytes32 actionId) external view returns (
        bytes32 proofHash,
        address supervisor,
        uint256 approvedAt
    ) {
        Action storage action = actions[actionId];
        require(action.status == ActionStatus.Approved || action.status == ActionStatus.Executed,
            "HSP: Action not approved");
        return (action.proofHash, action.supervisor, action.approvedAt);
    }

    /**
     * @notice Get agent statistics
     * @param agent Agent address to query
     */
    function getAgentStats(address agent) external view returns (
        uint256 requested,
        uint256 approved,
        uint256 rejected,
        uint256 approvalRate
    ) {
        Agent storage a = agents[agent];
        uint256 total = a.actionsApproved + a.actionsRejected;
        uint256 rate = total > 0 ? (a.actionsApproved * 10000) / total : 0;
        return (a.actionsRequested, a.actionsApproved, a.actionsRejected, rate);
    }

    // ============ Admin Functions ============

    /**
     * @notice Update action timeout
     * @param newTimeout New timeout in seconds
     */
    function setActionTimeout(uint256 newTimeout) external onlyOwner {
        require(newTimeout >= 1 hours && newTimeout <= 7 days, "HSP: Invalid timeout");
        actionTimeout = newTimeout;
    }

    /**
     * @notice Update treasury address
     * @param newTreasury New treasury address
     */
    function setTreasury(address newTreasury) external onlyOwner {
        require(newTreasury != address(0), "HSP: Invalid treasury");
        treasury = newTreasury;
    }

    /**
     * @notice Update protocol fee rate
     * @param newRate New rate in basis points (100 = 1%)
     */
    function setProtocolFeeRate(uint256 newRate) external onlyOwner {
        require(newRate <= 100, "HSP: Fee too high"); // Max 1%
        protocolFeeRate = newRate;
    }
}
