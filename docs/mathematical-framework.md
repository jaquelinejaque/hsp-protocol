# HSP Mathematical Framework

## Complete Formalization of the Human Supervision Protocol

**Version:** 1.0
**Patent Reference:** PCT/US26/11908

---

## 1. Variable Definitions

### 1.1 Input Variables

| Symbol | Name | Domain | Description |
|--------|------|--------|-------------|
| A | Autonomy Level | [0, 1] | Degree of AI system autonomy |
| I | Impact Severity | [0, 1] | Severity of decision impact |
| R | Reversibility | [0, 1] | Ability to reverse decisions |
| F | Frequency | ℝ⁺ | Decisions per time unit |
| C | Confidence | [0, 1] | Model confidence in predictions |
| H | Human Availability | [0, 1] | Availability of human supervisors |
| T | Time Criticality | [0, 1] | Temporal urgency of decisions |
| D | Data Sensitivity | [0, 1] | Sensitivity of processed data |

### 1.2 Output Variables

| Symbol | Name | Domain | Description |
|--------|------|--------|-------------|
| ρ | Risk Score | [0, 1] | Global risk score |
| σ | Supervision Intensity | [0, 1] | Required supervision intensity |
| τ | Intervention Threshold | [0, 1] | Threshold for human intervention |
| Ω | Compliance Score | [0, 100] | Regulatory compliance score |

### 1.3 Constants

| Symbol | Value | Origin | Description |
|--------|-------|--------|-------------|
| α | 0.618 | 1/φ (Golden Ratio) | Autonomy weight |
| β | 0.382 | 1/φ² | Impact weight |
| γ | 4.669 | Feigenbaum | Bifurcation constant |
| δ | 2.414 | Silver Ratio | Scale constant |

---

## 2. Core Formulas

### 2.1 Risk Score (ρ)

The risk of an AI system is a function of its autonomy, impact, and irreversibility:

```
ρ = α·A·I·(1-R) + β·(1-C)·D + (1-α-β)·T·F
```

**Expanded:**

```
ρ = 0.618·A·I·(1-R) + 0.382·(1-C)·D + 0.236·T·F
```

**Where:**
- First term: Autonomy risk (autonomous decisions with high irreversible impact)
- Second term: Uncertainty risk (low confidence with sensitive data)
- Third term: Temporal risk (frequent and urgent decisions)

**Properties:**
- ρ ∈ [0, 1]
- ρ = 0 → Minimum risk (safe system)
- ρ = 1 → Maximum risk (requires total supervision)

---

### 2.2 Supervision Intensity (σ)

Required supervision follows a sigmoidal curve based on risk:

```
σ = 1 / (1 + e^(-γ·(ρ - 0.5)))
```

**Where γ = 4.669 (Feigenbaum constant)**

This function:
- Grows slowly for low risks
- Transitions rapidly at ρ ≈ 0.5
- Saturates at 1 for high risks

**Supervision Curve:**

| ρ | σ | Interpretation |
|---|---|----------------|
| 0.1 | 0.06 | 6% supervision |
| 0.3 | 0.18 | 18% supervision |
| 0.5 | 0.50 | 50% supervision |
| 0.7 | 0.82 | 82% supervision |
| 0.9 | 0.94 | 94% supervision |

---

### 2.3 Intervention Threshold (τ)

The threshold for human intervention adjusts dynamically:

```
τ = C · R · H · (1 - σ/δ)
```

**Where:**
- C = Model confidence
- R = Reversibility
- H = Human availability
- δ = 2.414 (Silver Ratio)

**Interpretation:**
- If C·R·H is high (reliable model, reversible, humans available) → τ high (fewer interventions)
- If σ is high (much supervision needed) → τ low (more interventions)

**Decision Rule:**

```
IF current_confidence < τ THEN
    REQUIRE human intervention
ELSE
    ALLOW autonomous decision
END IF
```

---

### 2.4 Compliance Score (Ω)

Compliance score with EU AI Act:

```
Ω = 100 · (1 - |σ_actual - σ_required| / σ_required) · Q
```

**Where:**
- σ_actual = Actually implemented supervision
- σ_required = Supervision calculated by formula 2.2
- Q = Documentation quality factor [0, 1]

**Interpretation:**
- Ω = 100 → Perfect compliance
- Ω ≥ 80 → Adequate compliance (EU AI Act)
- Ω < 80 → Requires adjustments
- Ω < 50 → Non-compliant

---

## 3. EU AI Act Classification

### 3.1 Risk Category Mapping

| ρ (Risk Score) | EU AI Act Category | Supervision |
|----------------|-------------------|-------------|
| 0.00 - 0.25 | Minimal Risk | Optional |
| 0.25 - 0.50 | Limited Risk | Recommended |
| 0.50 - 0.75 | High Risk | Mandatory |
| 0.75 - 1.00 | Unacceptable Risk | Prohibited/Maximum |

### 3.2 Category Formula

```
Category = ⌊4·ρ⌋ + 1
```

Where ⌊x⌋ is the floor function.

---

## 4. Dynamic Model

### 4.1 Temporal Update

Risk evolves over time:

```
ρ(t+1) = ρ(t) + η·(ρ_observed - ρ(t)) - λ·Δσ
```

**Where:**
- η = 0.1 (learning rate)
- λ = 0.05 (damping factor)
- Δσ = σ(t) - σ(t-1) (supervision change)

### 4.2 Feedback Loop

System adjusts based on incidents:

```
ρ_adjusted = ρ · (1 + ε·N_incidents)
```

**Where:**
- ε = 0.1 (incident weight)
- N_incidents = Number of incidents in last 30 days

---

## 5. Performance Metrics

### 5.1 HSP Efficiency Index (HEI)

```
HEI = (Correct_decisions · σ) / (Human_interventions · Average_time)
```

**Interpretation:**
- High HEI → Efficient system (good supervision with low overhead)
- Low HEI → Excess interventions or frequent errors

### 5.2 Human-AI Collaboration Score (HACS)

```
HACS = √(σ · H · (1-ρ) · Ω/100)
```

**Interpretation:**
- HACS ∈ [0, 1]
- HACS > 0.7 → Excellent collaboration
- HACS < 0.4 → Requires optimization

---

## 6. Practical Example

### Case: AI Recruitment System

**Inputs:**
- A = 0.7 (high autonomy - automatically filters CVs)
- I = 0.8 (high impact - affects careers)
- R = 0.6 (moderately reversible)
- F = 100 (100 decisions/day)
- C = 0.85 (85% average confidence)
- H = 0.5 (50% human availability)
- T = 0.3 (low urgency)
- D = 0.9 (sensitive personal data)

**Calculations:**

1. **Risk Score:**
```
ρ = 0.618·0.7·0.8·(1-0.6) + 0.382·(1-0.85)·0.9 + 0.236·0.3·0.01
ρ = 0.138 + 0.052 + 0.001
ρ = 0.191
```

2. **Supervision Intensity:**
```
σ = 1 / (1 + e^(-4.669·(0.191 - 0.5)))
σ = 0.191 (19.1% supervision)
```

3. **Intervention Threshold:**
```
τ = 0.85 · 0.6 · 0.5 · (1 - 0.191/2.414)
τ = 0.235
```

4. **EU AI Act Category:**
```
Category = ⌊4·0.191⌋ + 1 = 1 → Minimal Risk
```

**Recommendation:** Human supervision on ~19% of decisions, intervention when confidence < 23.5%.

---

## 7. Implementation

Reference implementation: See `sdk/` directory.

---

## 8. References

1. EU AI Act - Regulation (EU) 2024/1689
2. Feigenbaum, M. (1978). Quantitative universality for nonlinear transformations
3. ISO/IEC 42001:2023 - AI Management Systems
4. NIST AI Risk Management Framework

---

**Patent Notice:** PCT/US26/11908
Commercial use requires licensing.
