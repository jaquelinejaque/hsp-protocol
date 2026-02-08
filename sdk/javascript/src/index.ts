/**
 * HSP Protocol JavaScript SDK
 *
 * Human Supervision Protocol - Fail-Closed Execution Layer for AI
 *
 * Patent Notice: PCT/US26/11908
 * Commercial use requires licensing. See PATENTS.md
 *
 * @packageDocumentation
 */

import { ethers, Contract, Signer, Provider } from 'ethers';

// Contract ABI (simplified for SDK)
const HSP_REGISTRY_ABI = [
  "function registerAgent(address agent, bytes32 policyHash) external",
  "function revokeAgent(address agent, string reason) external",
  "function requestAction(bytes32 actionHash, string metadata) external returns (bytes32)",
  "function approveAction(bytes32 actionId, bytes signature) external",
  "function rejectAction(bytes32 actionId, string reason) external",
  "function executeAction(bytes32 actionId) external",
  "function isActionApproved(bytes32 actionId) external view returns (bool)",
  "function getAction(bytes32 actionId) external view returns (bytes32, address, uint256, uint256, uint256, address, bytes32, uint8)",
  "function getProofOfSupervision(bytes32 actionId) external view returns (bytes32, address, uint256)",
  "function agents(address) external view returns (bool, bytes32, uint256, uint256, uint256, uint256, bool)",
  "event ActionRequested(bytes32 indexed actionId, address indexed agent, bytes32 actionHash)",
  "event ActionApproved(bytes32 indexed actionId, address indexed supervisor, bytes32 proofHash)",
  "event ActionRejected(bytes32 indexed actionId, address indexed supervisor, string reason)",
  "event ActionExecuted(bytes32 indexed actionId, uint256 timestamp)"
];

// Deployed contract addresses
export const CONTRACTS = {
  polygon: '0x1BCe4baE2E9e192EE906742a939FaFaec50A1B4e',
  polygonAmoy: '', // Coming soon
  ethereum: ''     // Coming soon
} as const;

export type NetworkName = keyof typeof CONTRACTS;

export enum ActionStatus {
  Pending = 0,
  Approved = 1,
  Rejected = 2,
  Executed = 3,
  Expired = 4
}

export interface HSPConfig {
  contractAddress?: string;
  network?: NetworkName;
  provider?: Provider;
  signer?: Signer;
}

export interface ActionRequest {
  type: string;
  data: Record<string, unknown>;
  justification?: string;
  metadata?: string;
}

export interface ActionDetails {
  actionId: string;
  actionHash: string;
  agent: string;
  requestedAt: Date;
  approvedAt: Date | null;
  executedAt: Date | null;
  supervisor: string | null;
  proofHash: string | null;
  status: ActionStatus;
}

export interface ProofOfSupervision {
  proofHash: string;
  supervisor: string;
  approvedAt: Date;
  actionId: string;
}

export interface AgentInfo {
  isRegistered: boolean;
  policyHash: string;
  registeredAt: Date;
  actionsRequested: number;
  actionsApproved: number;
  actionsRejected: number;
  isActive: boolean;
}

/**
 * HSP Client - Main interface for interacting with the Human Supervision Protocol
 *
 * @example
 * ```typescript
 * import { HSPClient } from '@hsp-protocol/sdk';
 *
 * const hsp = new HSPClient({
 *   network: 'polygon',
 *   signer: yourSigner
 * });
 *
 * const action = await hsp.requestAction({
 *   type: 'FINANCIAL_TRANSFER',
 *   data: { amount: 50000, recipient: '0x...' },
 *   justification: 'Quarterly vendor payment'
 * });
 * ```
 */
export class HSPClient {
  private contract: Contract;
  private provider: Provider;
  private signer?: Signer;
  private contractAddress: string;

  constructor(config: HSPConfig) {
    if (config.contractAddress) {
      this.contractAddress = config.contractAddress;
    } else if (config.network) {
      this.contractAddress = CONTRACTS[config.network];
      if (!this.contractAddress) {
        throw new Error(`Network ${config.network} not yet supported`);
      }
    } else {
      this.contractAddress = CONTRACTS.polygon;
    }

    if (config.signer) {
      this.signer = config.signer;
      this.provider = config.signer.provider!;
      this.contract = new Contract(this.contractAddress, HSP_REGISTRY_ABI, this.signer);
    } else if (config.provider) {
      this.provider = config.provider;
      this.contract = new Contract(this.contractAddress, HSP_REGISTRY_ABI, this.provider);
    } else {
      // Default to Polygon public RPC
      this.provider = new ethers.JsonRpcProvider('https://polygon-rpc.com');
      this.contract = new Contract(this.contractAddress, HSP_REGISTRY_ABI, this.provider);
    }
  }

  /**
   * Request supervision for an action (FAIL-CLOSED)
   * The action is blocked until a human supervisor approves it
   */
  async requestAction(request: ActionRequest): Promise<ActionDetails> {
    if (!this.signer) {
      throw new Error('Signer required for write operations');
    }

    // Create action hash from request data
    const actionData = JSON.stringify({
      type: request.type,
      data: request.data,
      justification: request.justification,
      timestamp: Date.now()
    });
    const actionHash = ethers.keccak256(ethers.toUtf8Bytes(actionData));

    const metadata = request.metadata || '';

    const tx = await this.contract.requestAction(actionHash, metadata);
    const receipt = await tx.wait();

    // Extract actionId from event
    const event = receipt.logs.find((log: any) => {
      try {
        const parsed = this.contract.interface.parseLog(log);
        return parsed?.name === 'ActionRequested';
      } catch {
        return false;
      }
    });

    if (!event) {
      throw new Error('ActionRequested event not found');
    }

    const parsed = this.contract.interface.parseLog(event);
    const actionId = parsed!.args[0];

    return this.getAction(actionId);
  }

  /**
   * Approve a pending action (Human Supervisor)
   */
  async approveAction(actionId: string): Promise<ProofOfSupervision> {
    if (!this.signer) {
      throw new Error('Signer required for approval');
    }

    // Sign the actionId as proof of human supervision
    const signature = await this.signer.signMessage(ethers.getBytes(actionId));

    const tx = await this.contract.approveAction(actionId, signature);
    await tx.wait();

    return this.getProofOfSupervision(actionId);
  }

  /**
   * Reject a pending action
   */
  async rejectAction(actionId: string, reason: string): Promise<void> {
    if (!this.signer) {
      throw new Error('Signer required for rejection');
    }

    const tx = await this.contract.rejectAction(actionId, reason);
    await tx.wait();
  }

  /**
   * Execute an approved action
   */
  async executeAction(actionId: string): Promise<ActionDetails> {
    if (!this.signer) {
      throw new Error('Signer required for execution');
    }

    const tx = await this.contract.executeAction(actionId);
    await tx.wait();

    return this.getAction(actionId);
  }

  /**
   * Get action details
   */
  async getAction(actionId: string): Promise<ActionDetails> {
    const result = await this.contract.getAction(actionId);

    return {
      actionId,
      actionHash: result[0],
      agent: result[1],
      requestedAt: new Date(Number(result[2]) * 1000),
      approvedAt: result[3] > 0 ? new Date(Number(result[3]) * 1000) : null,
      executedAt: result[4] > 0 ? new Date(Number(result[4]) * 1000) : null,
      supervisor: result[5] !== ethers.ZeroAddress ? result[5] : null,
      proofHash: result[6] !== ethers.ZeroHash ? result[6] : null,
      status: result[7] as ActionStatus
    };
  }

  /**
   * Check if an action is approved
   */
  async isActionApproved(actionId: string): Promise<boolean> {
    return this.contract.isActionApproved(actionId);
  }

  /**
   * Get proof of supervision for an approved action
   */
  async getProofOfSupervision(actionId: string): Promise<ProofOfSupervision> {
    const result = await this.contract.getProofOfSupervision(actionId);

    return {
      proofHash: result[0],
      supervisor: result[1],
      approvedAt: new Date(Number(result[2]) * 1000),
      actionId
    };
  }

  /**
   * Get agent information
   */
  async getAgent(address: string): Promise<AgentInfo> {
    const result = await this.contract.agents(address);

    return {
      isRegistered: result[0],
      policyHash: result[1],
      registeredAt: new Date(Number(result[2]) * 1000),
      actionsRequested: Number(result[3]),
      actionsApproved: Number(result[4]),
      actionsRejected: Number(result[5]),
      isActive: result[6]
    };
  }

  /**
   * Listen for action events
   */
  onActionRequested(callback: (actionId: string, agent: string, actionHash: string) => void): void {
    this.contract.on('ActionRequested', callback);
  }

  onActionApproved(callback: (actionId: string, supervisor: string, proofHash: string) => void): void {
    this.contract.on('ActionApproved', callback);
  }

  onActionRejected(callback: (actionId: string, supervisor: string, reason: string) => void): void {
    this.contract.on('ActionRejected', callback);
  }

  onActionExecuted(callback: (actionId: string, timestamp: number) => void): void {
    this.contract.on('ActionExecuted', callback);
  }

  /**
   * Remove all event listeners
   */
  removeAllListeners(): void {
    this.contract.removeAllListeners();
  }
}

// Export utilities
export { ethers } from 'ethers';

export default HSPClient;
