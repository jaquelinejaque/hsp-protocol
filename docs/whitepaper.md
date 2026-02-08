# HSP: The Human Supervision Protocol
## Technical Whitepaper v1.0

**Authors:** HSP Protocol Team
**Date:** February 2026
**Patent:** PCT/US26/11908

---

## Abstract

The Human Supervision Protocol (HSP) is a decentralized infrastructure layer designed to enforce mandatory human oversight on autonomous AI agents. Unlike probabilistic safety measures (RLHF, Constitutional AI), HSP provides **cryptographic guarantees** that no AI action can execute without explicit human approval.

This document describes the technical architecture, mathematical foundations, and implementation details of the protocol.

---

## 1. Introduction

### 1.1 The Problem

As AI agents transition from "chatbots" to "autonomous workflows," a critical gap emerges: **Liability.**

Current AI safety measures are probabilistic:
- RLHF achieves ~99.9% alignment
- This means 1 in 1,000 actions may be harmful
- For high-stakes domains (finance, healthcare, legal), this is unacceptable

**The core issue:** Enterprises cannot deploy autonomous agents that might execute unauthorized actions.

### 1.2 The Solution: Fail-Closed Execution

HSP introduces the concept of **Fail-Closed Execution**:

```
Traditional AI: Action executes → Safety check → Maybe blocked
HSP:            Action blocked → Human approval → Then executes
```

The default state is **blocked**, not **allowed**.

---

## 2. Core Principles

### 2.1 The Three Axioms

1. **Universal Interception**
   Every AI action that affects external systems must pass through HSP.

2. **Sovereignty of Audit**
   Every approval generates an immutable, cryptographic proof.

3. **Non-Bypassable**
   The AI cannot circumvent the supervision layer.

### 2.2 Proof of Supervision

Unlike Proof of Work (computational) or Proof of Stake (economic), HSP introduces **Proof of Supervision** (PoS):

- A human supervisor cryptographically signs each action
- The signature is recorded on-chain
- The action cannot execute without a valid signature
- The signature is permanently auditable

---

## 3. Architecture

### 3.1 Layer Model

```
┌─────────────────────────────────────────────┐
│          APPLICATION LAYER                   │
│     (AI Agent / LLM / Autonomous System)     │
└─────────────────────┬───────────────────────┘
                      │ Action Request
                      ▼
┌─────────────────────────────────────────────┐
│           OBSERVER LAYER                     │
│  • Captures intent                           │
│  • Classifies action type                    │
│  • Calculates risk score (ρ)                 │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│          VALIDATOR LAYER                     │
│  • Checks policy compliance                  │
│  • Determines supervision requirements (σ)   │
│  • Routes to appropriate supervisor          │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│          SUPERVISOR LAYER                    │
│  • Human reviews action                      │
│  • Signs approval (ECDSA)                    │
│  • Generates Proof of Supervision            │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│         BLOCKCHAIN LAYER                     │
│  • Records proof on-chain                    │
│  • Executes action atomically                │
│  • Immutable audit trail                     │
└─────────────────────────────────────────────┘
```

### 3.2 The Interceptor Pattern

The key innovation is the **Interceptor Pattern**:

```solidity
function executeAction(bytes32 actionId) external {
    // FAIL-CLOSED: Action must be explicitly approved
    require(actions[actionId].status == ActionStatus.Approved,
        "HSP: Action not approved");

    // Verify human signature exists
    require(actions[actionId].proofHash != bytes32(0),
        "HSP: Missing proof of supervision");

    // Only then execute
    _performAction(actionId);
}
```

---

## 4. Mathematical Framework

### 4.1 Risk Scoring

The Risk Score (ρ) quantifies the danger level of an AI action:

```
ρ = α·A·I·(1-R) + β·(1-C)·D + (1-α-β)·T·F
```

Where:
- A = Autonomy Level [0,1]
- I = Impact Severity [0,1]
- R = Reversibility [0,1]
- C = Model Confidence [0,1]
- D = Data Sensitivity [0,1]
- T = Time Criticality [0,1]
- F = Frequency (normalized)
- α = 0.618 (1/φ, Golden Ratio inverse)
- β = 0.382 (1/φ²)

### 4.2 Supervision Intensity

The required supervision follows a sigmoid curve:

```
σ = 1 / (1 + e^(-γ·(ρ - 0.5)))
```

Where γ = 4.669 (Feigenbaum constant)

This creates:
- Gradual increase for low-risk actions
- Sharp transition around ρ = 0.5
- Saturation to 100% for high-risk actions

### 4.3 Intervention Threshold

Dynamic threshold for automatic vs. supervised execution:

```
τ = C · R · H · (1 - σ/δ)
```

Where:
- H = Human Availability [0,1]
- δ = 2.414 (Silver Ratio)

---

## 5. Smart Contract Design

### 5.1 Core Contract: HSP_Registry.sol

The registry manages:
- Agent registration and policy storage
- Action lifecycle (request → approve/reject → execute)
- Supervisor authorization levels
- Proof generation and verification

### 5.2 Action Lifecycle

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│ PENDING  │────▶│ APPROVED │────▶│ EXECUTED │     │ REJECTED │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
     │                                                   ▲
     └───────────────────────────────────────────────────┘
```

### 5.3 Proof Structure

Each approval generates:

```solidity
proofHash = keccak256(abi.encodePacked(
    actionId,
    supervisor,
    block.timestamp,
    signature
));
```

This creates an unforgeable, timestamped proof of human authorization.

---

## 6. EU AI Act Compliance

HSP directly implements EU AI Act requirements:

| Article | Requirement | HSP Implementation |
|---------|-------------|-------------------|
| Art. 14 | Human oversight | Fail-closed approval mechanism |
| Art. 12 | Record-keeping | On-chain audit trail |
| Art. 9  | Risk management | Mathematical risk scoring |
| Annex IV | Documentation | Automated compliance reports |

---

## 7. Security Model

### 7.1 Threat Model

HSP protects against:
- **AI Bypass**: Cryptographic signatures prevent spoofing
- **Replay Attacks**: Unique action IDs and nonces
- **Collusion**: Multi-signature requirements for high-risk actions
- **Data Tampering**: Blockchain immutability

### 7.2 Key Management

- Supervisors control their own private keys
- No central authority can forge approvals
- Hardware wallet integration supported

---

## 8. Deployment

### 8.1 Current Status

| Network | Contract | Status |
|---------|----------|--------|
| Polygon Mainnet | `0x1BCe4baE2E9e192EE906742a939FaFaec50A1B4e` | Live |
| Polygon Amoy | Coming Soon | Testnet |
| Ethereum | Coming Soon | Planned |

### 8.2 Gas Optimization

- Optimistic execution paths for pre-approved patterns
- Batch processing for multiple actions
- Layer 2 scaling for high-frequency use cases

---

## 9. Conclusion

HSP represents a paradigm shift in AI safety: from probabilistic filters to cryptographic guarantees. By making human oversight **mandatory** and **verifiable**, HSP enables the deployment of autonomous AI in regulated industries while maintaining full accountability.

---

## References

1. EU AI Act - Regulation (EU) 2024/1689
2. ISO/IEC 42001:2023 - AI Management Systems
3. Feigenbaum, M. (1978). Quantitative universality for nonlinear transformations
4. NIST AI Risk Management Framework (AI RMF 1.0)

---

**Patent Notice:** PCT/US26/11908
**License:** Apache 2.0 (Commercial use requires licensing)
