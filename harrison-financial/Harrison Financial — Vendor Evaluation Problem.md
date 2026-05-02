# Harrison Financial — Vendor Evaluation Problem

## Executive Summary

Harrison Financial, a U.S.-based digital banking platform, is attempting to identify a fraud detection vendor that meets its operational, technical, and regulatory requirements.

Despite evaluating dozens of vendors, no solution fully satisfies all constraints without tradeoffs.

> The core bottleneck is not model capability, but vendor discovery and matching under strict constraints.

---

## Business Context

- ~3 million active users  
- ~4.2 million transactions per day  
- Real-time payment authorization system  

**Risk Exposure**
- Fraud loss (last quarter): ~$3.8M  
- False-positive decline rate: ~2.7%  

---

## Core Problem

Fraud detection must operate under multiple simultaneous constraints:

### Technical Requirements
- Real-time scoring (<100ms latency)  
- Integration with Kafka-based event streams  
- Compatibility with AWS + Python infrastructure  

### Compliance Requirements
- Support for KYC (Know Your Customer)  
- Support for AML (Anti-Money Laundering)  
- Full audit logs  
- Explainable decision outputs  

### Business Requirements
- Minimize false positives (user experience)  
- Minimize false negatives (financial loss)  

> These constraints drastically reduce the viable vendor pool.

---

## Vendor Evaluation Reality

- 100+ vendors identified  
- 38 vendors evaluated in detail  
- Only 2–3 considered viable  

### Typical Outcome

Most vendors fail in at least one critical dimension:

- Too slow (latency >100ms)  
- Not explainable (compliance risk)  
- Difficult to integrate  
- Incomplete regulatory support  

> “Almost compatible” solutions dominate the market.

---

## Key Challenges

### 1. Discovery Problem
- Vendor capabilities are unclear or overstated  
- Difficult to identify true technical fit  
- No standardized way to compare vendors  

---

### 2. Evaluation Cost
- Pilot testing requires significant setup  
- Cross-team coordination (engineering, compliance, legal)  
- Evaluation cycle: 6–12 months  

---

### 3. Integration Risk
- Poor fit may impact transaction latency  
- Risk of system instability  
- High cost of rollback or replacement  

---

### 4. Tradeoff Dilemma
- Speed vs accuracy vs explainability  
- No vendor optimizes all dimensions simultaneously  

---

## Structural Bottleneck

The problem is not lack of vendors.

> It is a **high-dimensional matching problem under strict constraints**

Traditional approach:
- Manual search  
- Static reports  
- Human-driven comparison  

Result:
- Slow  
- Incomplete  
- High uncertainty  

---

## Conclusion

Harrison Financial’s vendor selection process is fundamentally constrained by:

- Complex technical requirements  
- Strict regulatory obligations  
- High integration costs  
- Inefficient discovery mechanisms  

> Improving vendor matching—not model performance—is the key to solving this problem.