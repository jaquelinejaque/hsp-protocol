# HSP: Human Supervision Protocol

> **The Fail-Closed Execution Layer for Autonomous AI**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Patent](https://img.shields.io/badge/Patent-PCT%2FUS26%2F11908-green.svg)](PATENTS.md)
[![Mainnet](https://img.shields.io/badge/Polygon-Mainnet-purple.svg)](https://polygonscan.com/address/0x1BCe4baE2E9e192EE906742a939FaFaec50A1B4e)
[![EU AI Act](https://img.shields.io/badge/EU%20AI%20Act-Compliant-yellow.svg)](docs/compliance.md)

---

## The Problem

AI Agents are moving from "chatbots" to "autonomous workflows" in Finance, Legal, and Healthcare. But there's a critical blocker: **Liability.**

- A 99.9% success rate means **1 in 1,000 transactions is a lawsuit**
- Enterprises cannot deploy agents that rely solely on probabilistic safety filters (RLHF)
- The EU AI Act (Regulation 2024/1689) mandates human oversight for high-risk AI systems

**Current solutions are soft. HSP is hard.**

---

## The Solution: Proof of Supervision

HSP is not a filter. It is an **Interceptor**.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   AI Agent  │────▶│  HSP Layer  │────▶│   Human     │────▶│  Execution  │
│  (Request)  │     │ (Intercept) │     │ (Approval)  │     │  (Action)   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  Blocked    │
                    │ (No Bypass) │
                    └─────────────┘
```

**Key Properties:**
- **Fail-Closed**: Actions are blocked by default until explicitly approved
- **Non-Bypassable**: The AI cannot circumvent the supervision layer
- **Cryptographic Proof**: Every approval is signed and immutable on-chain

---

## Quick Start

### Installation

```bash
# JavaScript/TypeScript
npm install @hsp-protocol/sdk

# Python
pip install hsp-protocol
```

### Basic Usage

```javascript
import { HSPClient } from '@hsp-protocol/sdk';

const hsp = new HSPClient({
  contractAddress: '0x1BCe4baE2E9e192EE906742a939FaFaec50A1B4e',
  network: 'polygon'
});

// Request supervised action
const action = await hsp.requestAction({
  type: 'FINANCIAL_TRANSFER',
  amount: 50000,
  recipient: '0x...',
  justification: 'Quarterly vendor payment'
});

// Action is pending until human approves
console.log(action.status); // 'PENDING_SUPERVISION'

// After human approval (signed cryptographically)
console.log(action.status); // 'APPROVED'
console.log(action.proofHash); // '0x7f3a...'
```

---

## Mathematical Framework

HSP uses a rigorous mathematical model to calculate supervision requirements:

### Risk Score (ρ)

```
ρ = α·A·I·(1-R) + β·(1-C)·D + (1-α-β)·T·F
```

Where:
- `A` = Autonomy Level [0,1]
- `I` = Impact Severity [0,1]
- `R` = Reversibility [0,1]
- `C` = Model Confidence [0,1]
- `D` = Data Sensitivity [0,1]
- `T` = Time Criticality [0,1]
- `F` = Frequency (normalized)
- `α = 0.618` (Golden Ratio inverse)
- `β = 0.382` (φ⁻²)

### Supervision Intensity (σ)

```
σ = 1 / (1 + e^(-γ·(ρ - 0.5)))
```

Where `γ = 4.669` (Feigenbaum constant)

[Full Mathematical Framework →](docs/mathematical-framework.md)

---

## EU AI Act Compliance

HSP maps directly to EU AI Act requirements:

| EU AI Act Article | HSP Implementation |
|-------------------|-------------------|
| Article 14 (Human Oversight) | Fail-closed approval mechanism |
| Article 12 (Record-Keeping) | Immutable blockchain audit trail |
| Article 9 (Risk Management) | Mathematical risk scoring |
| Annex IV (Documentation) | Automated compliance reports |

[Compliance Documentation →](docs/compliance.md)

---

## Architecture

```
┌────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                      │
│            (Your AI Agent / LLM / Autonomous System)        │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                       HSP SDK LAYER                         │
│    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│    │   Observer   │  │   Validator  │  │  Supervisor  │    │
│    │    Layer     │  │    Layer     │  │    Layer     │    │
│    └──────────────┘  └──────────────┘  └──────────────┘    │
└─────────────────────────────┬──────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────┐
│                   BLOCKCHAIN LAYER (Polygon)                │
│              Contract: 0x1BCe4baE2E9e192EE906742a939FaFaec  │
└────────────────────────────────────────────────────────────┘
```

---

## Deployed Contracts

| Network | Address | Status |
|---------|---------|--------|
| Polygon Mainnet | `0x1BCe4baE2E9e192EE906742a939FaFaec50A1B4e` | Live |
| Polygon Amoy (Testnet) | Coming Soon | - |
| Ethereum Mainnet | Coming Soon | - |

---

## Documentation

- [Technical Whitepaper](docs/whitepaper.md)
- [Mathematical Framework](docs/mathematical-framework.md)
- [Integration Guide](docs/integration-guide.md)
- [API Reference](docs/api-reference.md)
- [Compliance Guide](docs/compliance.md)

---

## Use Cases

### Financial Services
Autonomous trading agents with mandatory human approval for transactions above threshold.

### Healthcare AI
Diagnostic AI systems with physician sign-off requirements.

### Legal Tech
Contract analysis AI with lawyer supervision for binding decisions.

### Enterprise Automation
RPA bots with escalation paths for edge cases.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License & Patents

This project is licensed under the Apache License 2.0 - see [LICENSE](LICENSE).

**Important:** The HSP Protocol is covered by international patent application **PCT/US26/11908**. Commercial use requires a license. See [PATENTS.md](PATENTS.md) for details.

---

## Contact

- **Website:** [hsp-protocol.org](https://hsp-protocol.org)
- **Email:** contact@hsp-protocol.org
- **Twitter/X:** [@HSPProtocol](https://twitter.com/HSPProtocol)

---

*Building the trust layer for autonomous AI.*
