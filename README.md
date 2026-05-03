# Fake Companies
A fake banking company and a fake AI risk infrastructure startup's websites.

## Companies

### Harrison Financial (`harrison-financial/`)
A fictional digital-first neobank offering checking, savings, lending, and card products. Built to represent a modern financial institution with real-time payment infrastructure and strict compliance requirements (AML/KYC).

### SecureStar (`securestar/`)
A fictional AI risk infrastructure startup (~50 employees) founded by ex-fintech and ML engineers. Specializes in real-time fraud detection for high-throughput financial systems.

**Pages:**
- `index.html` — Landing page with API demo, capabilities overview, and integration highlights
- `platform.html` — Deep-dive into the five platform pillars (latency, explainability, hybrid engine, custom tuning, compliance)
- `solutions.html` — Solutions for digital banking, payments, lending, and AML/KYC programs
- `developers.html` — Developer documentation: REST API reference, Kafka connector, Python SDK
- `company.html` — Founding story, team, mission, and values

**Why SecureStar fits Harrison Financial:**
SecureStar's platform is purpose-built for companies like Harrison Financial — it delivers sub-80ms real-time transaction scoring, native Kafka/AWS/Python integration, explainable AI decisions (satisfying AML/KYC compliance), and a hybrid ML + rule-based engine with custom model tuning.

### Mike's HVAC & Air (`HVAC/` · `HVAC-mobile/`)
A fictional residential and commercial HVAC company run by a solo owner-operator. Demonstrates an "agentic HVAC business" — an AI agent handles leads, quoting, scheduling, and field coordination on the owner's behalf.

**`HVAC/` — 6-page company website (intro site):**
- `index.html` — Landing page with services overview and call-to-action
- `services.html` — Full services catalog (repair, install, maintenance, pricing tiers)
- `dashboard.html` — Owner-facing agent dashboard with activity feed and voice button
- `leads.html` — Incoming leads list with agent-to-agent transcript view
- `field.html` — Field mode: voice input, parallel agent tasks, supplier pricing
- `jobs.html` — Active and completed jobs with permit flow and wrap-up

**`HVAC-mobile/` — Interactive phone-only prototype (4 pages, 12 screens total):**
- `index.html` — App home dashboard: status cards (tappable), activity feed (expandable), voice button with state cycling
- `leads.html` — 3 screens: leads list → per-lead detail with inline actions → agent-to-agent chat transcript
- `field.html` — 3 screens: voice/listening mode with waveform → 4 background agent tasks (tappable) → supplier pricing with Approve/Override
- `jobs.html` — 3 screens: jobs list → permit filing with animated confirmation → job close-out with Send Invoice flow
