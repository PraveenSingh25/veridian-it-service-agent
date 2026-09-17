# Veridian Corp — Internal Service Agent (IT Support)
> **Candidate Assignment for Product Engineering / AI**  
> *Operating Context: Veridian Corp, Week of Monday, 21 September 2026 – Friday, 25 September 2026*  
> *Strict Grounding Mandate: Zero Hallucination | 100% Policy Grounded*

[![Tests](https://img.shields.io/badge/Tests-21%2F21%20Passed-brightgreen)](tests/)
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit%201.56-red)](https://streamlit.io)
[![Grounding](https://img.shields.io/badge/Grounding-100%25%20Verified-success)]()

---

## 🌟 Executive Summary

This project implements an autonomous, enterprise-grade **IT Support Service Agent** for **Veridian Corp**. Built for a **Product Engineering / AI** role evaluation, the system automates IT ticket triage, employee guidance, cross-department routing, and security containment while strictly adhering to organizational policies and historical ticket precedents.

### Key Highlights
1. **Strict Source Grounding & Anti-Hallucination**: The agent enforces the core constraint: *"Do not invent policies or information that isn't grounded in one of these sources."* Every response and routing cites specific policy IDs (`KB-01` to `KB-10`, `POL-ASSET-01`) and historical tickets (`TK-1042` to `TK-1051`).
2. **Policy Conflict Reconciliation**: Resolves the delicate interplay between `KB-03` (laptop replacement eligibility after 3 years) and the Finance `Asset Management Policy` (standard 4-year refresh cycle requiring Finance sign-off for early replacement) anchored in historical precedent `TK-1043`.
3. **Dual Queue Triage**:
   - **Section 2**: Complete triage and grounded response generation for all 15 Employee Requests (`REQ-01` to `REQ-15`).
   - **Section 3**: Autonomous routing and SLA tracking for the 4 Active Tickets (`TK-1043`, `TK-1044`, `TK-1047`, `TK-1048`), while referencing the 6 Closed Tickets as decision precedents.
4. **Active Security Intervention**: Proactively intercepts security hazards—such as an employee forwarding a phishing email internally (`REQ-08`)—and issues high-priority warnings per `KB-09`.
5. **Ambiguity & Clarification Engine**: When an inquiry is under-specified (`REQ-15: "hey can you help, its not working"`), the agent prompts for missing context instead of hallucinating instructions.
6. **One-Command Local Run**: Fully functional out of the box with zero external API key requirements.

---

## 🚀 One-Command Local Run for Reviewers

### 1. Launch the Interactive Web Dashboard (Streamlit)
```powershell
# Navigate to project directory
cd C:\Users\Praveen\.gemini\antigravity\scratch\veridian-it-service-agent

# Run the Streamlit web application
streamlit run app.py
```
> The dashboard will launch at `http://localhost:8501`.  
> Explore the **Live Agent Playground**, the **Employee Requests Queue**, the **Ticket Queue Manager**, the **Knowledge Base & Policy Conflict Matrix**, and run the **Automated Benchmark Scorecard** in 1 click.

### 2. Run the Automated CLI Benchmark
```powershell
python cli.py --eval
```
> Evaluates all 15 requests and 4 active tickets in the console, displays the structured triage table, and exports `evaluation_report.json`.

### 3. Launch Interactive Terminal Chat
```powershell
python cli.py --interactive
```
> Allows typing arbitrary IT queries or testing custom edge cases directly in the shell.

### 4. Run the Full Unit Test Suite
```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```
> Runs 21 test assertions across all requests, active tickets, and citation integrity checks (executed in ~0.005s).

---

## 🏛️ System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│               Interactive Layer (Streamlit App & CLI Runner)           │
│  - Live Agent Playground      - Request Queue (REQ-01 to REQ-15)       │
│  - Active Ticket Manager      - Knowledge Base & Policy Conflict Matrix│
│  - Benchmark Scorecard        - JSON Export Engine                     │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        Core Agent Engine                               │
│  ┌────────────────────────┐  ┌──────────────────────────────────────┐  │
│  │ Grounding Guardrails   │  │ Policy Conflict Resolver             │  │
│  │ (Anti-Hallucination)   │  │ (KB-03 vs Asset Management Policy)   │  │
│  └───────────┬────────────┘  └──────────────────┬───────────────────┘  │
│              │                                  │                      │
│              ▼                                  ▼                      │
│  ┌────────────────────────┐  ┌──────────────────────────────────────┐  │
│  │ Precedent Matcher      │  │ Triage & Routing Decision Engine     │  │
│  │ (TK-1042 to TK-1051)   │  │ (Direct / Route / Security / Escalate)│ │
│  └────────────────────────┘  └──────────────────────────────────────┘  │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                         Knowledge & Data Layer                         │
│  - data/policies.json: KB-01 to KB-10 + Asset Management Policy       │
│  - data/employee_requests.json: REQ-01 to REQ-15                       │
│  - data/ticket_history.json: TK-1042 to TK-1051                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ⚖️ Policy Conflict Resolution: KB-03 vs Finance Asset Policy

| Policy Source | Clause / Rule | Condition |
| :--- | :--- | :--- |
| **KB-03 (IT Hardware)** | Eligible for replacement after **3 years of service**, or earlier in case of verified hardware failure. | 2 weeks advance notice required. |
| **Asset Management Policy (Finance Extract Q2 2026)** | All company hardware follows a standard **4-year refresh cycle**. | Early replacement outside 4-year cycle requires **Finance sign-off** in addition to IT approval. |
| **Historical Precedent TK-1043** | S. Iyer: *Laptop replacement (3.2 yrs old)* | **Approved — pending fulfillment (active)**. Precedent confirms 3.2-year replacement is approved with Finance sign-off. |

### Reconciliation Applied by the Agent:
1. **Aditi Sharma (`REQ-01`, 3.5 yrs, completely dead):** Qualifies under `KB-03` (>3 years + verified hardware failure). Reconciled with Asset Management Policy by dispatching IT technician for failure verification and routing for Finance early-cycle sign-off matching `TK-1043` precedent (2-week fulfillment SLA).
2. **Aman Gupta (`REQ-13`, 2 yrs, flickering screen):** Under 3 years (`KB-03`) and 4 years (Finance policy). Because Aman suggested a fix and replacement requires verified unfixable failure + Finance approval, the agent routes for on-site diagnostic repair rather than replacement.

---

## 📊 Summary of Request Triage Decisions (REQ-01 to REQ-15)

| ID | Employee | Request Summary | Action Type | Department | Citations | Precedent |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **REQ-01** | Aditi Sharma | Dead laptop (3.5 yrs old) | `ROUTE_TO_HUMAN` | IT Hardware / Finance | KB-03, POL-ASSET-01 | TK-1043 |
| **REQ-02** | Vikram Chawla | Guest Wi-Fi tomorrow | `DIRECT_RESOLVE` | Employee Self-Service | KB-07 | TK-1051 |
| **REQ-03** | Karan Mehta | Locked out (6 attempts) | `ROUTE_TO_HUMAN` | IT Service Desk | KB-01 | TK-1049 |
| **REQ-04** | Ritu Bhatia | Non-catalog data tool | `REQUIRE_APPROVAL` | IT Security | KB-04 | TK-1044 |
| **REQ-05** | Sanjay Oberoi | Expired VPN credentials | `DIRECT_RESOLVE` | Employee Self-Service | KB-02 | TK-1042 |
| **REQ-06** | Meera Iyer | 3rd floor printer jam | `ROUTE_TO_HUMAN` | IT Service Desk | KB-05 | TK-1046 |
| **REQ-07** | Farhan Ali | WFH 4 days/week monitor | `REQUIRE_APPROVAL` | Finance / IT Logistics | KB-10, POL-ASSET-01 | TK-1047 |
| **REQ-08** | Ananya Reddy | Forwarding phishing email | `ESCALATE_SECURITY` | IT Security | KB-09 | TK-1048 |
| **REQ-09** | Rohit Desai | Mailbox full | `DIRECT_RESOLVE` | IT Service Desk | KB-06 | TK-1045 |
| **REQ-10** | Kavya Pillai | Admin access finance server | `REQUIRE_APPROVAL` | IT Security | KB-08, Access Precedent | TK-1050 |
| **REQ-11** | Nikhil Bansal | Contractor VPN access | `REQUIRE_APPROVAL` | IT Service Desk | KB-02 | TK-1042 |
| **REQ-12** | Sneha Kulkarni | Expense tool login error | `ROUTE_TO_HUMAN` | IT Service Desk / Finance | KB-08 | — |
| **REQ-13** | Aman Gupta | Screen flickering (2 yrs) | `ROUTE_TO_HUMAN` | IT Hardware Support | KB-03, POL-ASSET-01 | TK-1043 |
| **REQ-14** | Tanya Chopra | Browser extension | `REQUIRE_APPROVAL` | IT Security | KB-04 | TK-1044 |
| **REQ-15** | Rahul Menon | "hey can you help, its not working" | `REQUEST_CLARIFICATION` | IT Service Desk | *None (Underspecified)* | — |

---

## 🎫 Active Ticket Queue Triage (Section 3)

| Ticket ID | Employee | Initial Status | Recommended Action | Routed Department | SLA Tracking |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TK-1043** | S. Iyer | Approved — pending fulfillment (active) | `ROUTE_TO_HUMAN` | IT Hardware Support | Standard 2-week fulfillment window (`KB-03`). Device staging and data migration. |
| **TK-1044** | A. Khan | Pending Security review (active) | `REQUIRE_APPROVAL` | IT Security | 3–5 business days SLA tracking (`KB-04`). Follow up with SecOps queue. |
| **TK-1047** | K. Singh | Pending Finance (active) | `REQUIRE_APPROVAL` | Finance & Assets | Hold for Finance approval sign-off per `KB-10` before IT dispatches shipping. |
| **TK-1048** | T. Rao | Escalated to Security — under investigation (active) | `ESCALATE_SECURITY` | IT Security | Active perimeter quarantine (`KB-09`). Sweep internal mailboxes and block malicious domains. |

---

## 📁 Repository Structure

```
veridian-it-service-agent/
├── app.py                     # Streamlit web application (Interactive dashboard, chat, metrics)
├── cli.py                     # Command-line interface for eval & interactive chat
├── requirements.txt           # Python dependencies (streamlit, pydantic, rich, pandas)
├── README.md                  # System documentation & quickstart guide
├── EVALUATION_REPORT.md       # Comprehensive Product Engineering / AI report
├── evaluation_report.json     # Exported evaluation output from automated benchmark
├── data/
│   ├── policies.json          # Grounded KB-01..KB-10 + Asset Management Policy Extract
│   ├── employee_requests.json # REQ-01..REQ-15 dataset
│   └── ticket_history.json    # TK-1042..TK-1051 dataset (active + closed tickets)
├── engine/
│   ├── __init__.py
│   ├── models.py              # Pydantic schemas (Enums, Request, Ticket, TriageResult)
│   ├── kb_store.py            # Knowledge Base loader & strict semantic matcher
│   ├── precedent_engine.py    # Historical ticket precedent matching
│   ├── guardrails.py          # Grounding verifier, anti-hallucination, security alerts
│   └── agent.py               # Core decision engine & grounded response generator
└── tests/
    ├── __init__.py
    ├── test_agent.py          # Unit tests for all 15 requests + citation integrity
    └── test_ticket_queue.py   # Unit tests for active ticket routing & closed precedents
```

---

## 🧪 Evaluation & Test Results

```
test_grounding_citation_integrity ... ok
test_req_01_laptop_dead_aditi ... ok
test_req_02_guest_wifi_vikram ... ok
test_req_03_password_lockout_karan ... ok
test_req_04_software_catalog_ritu ... ok
test_req_05_vpn_expired_sanjay ... ok
test_req_06_printer_jam_meera ... ok
test_req_07_wfh_equipment_farhan ... ok
test_req_08_phishing_forwarding_ananya ... ok
test_req_09_mailbox_full_rohit ... ok
test_req_10_admin_access_kavya ... ok
test_req_11_contractor_vpn_nikhil ... ok
test_req_12_expense_tool_sneha ... ok
test_req_13_laptop_screen_flicker_aman ... ok
test_req_14_browser_extension_tanya ... ok
test_req_15_vague_input_rahul ... ok
test_closed_tickets_non_actionable ... ok
test_tk_1043_active_laptop_replacement ... ok
test_tk_1044_active_non_catalog_software ... ok
test_tk_1047_active_home_office_equipment ... ok
test_tk_1048_active_phishing_investigation ... ok

----------------------------------------------------------------------
Ran 21 tests in 0.005s

OK (100% Pass Rate)
```

---
*Developed for Veridian Corp IT Support Evaluation — Product Engineering / AI.*
