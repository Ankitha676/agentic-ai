# agentic-ai

#  ComplianceIQ  
### Agentic AI System for Multi-Source Enterprise Analysis



##  Overview

**ComplianceIQ** is an AI-powered agent designed to analyze and answer questions across **multi-format enterprise datasets** including PDFs, Word documents, and tabular data (CSV/Excel).

The system simulates real-world enterprise scenarios where information is scattered across different sources and requires **cross-document reasoning** to identify compliance issues, violations, and missing information.

---

##  Key Features

-  **Multi-format ingestion**
  - PDF (via PyMuPDF4LLM)
  - DOCX
  - CSV / Excel

-  **Hybrid Retrieval**
  - Vector search (Qdrant)
  - Keyword search (BM25)

-  **Agentic Reasoning (LangGraph)**
  - Multi-step reasoning across documents
  - Combines structured + unstructured data

-  **Compliance Analysis**
  - Detects violations
  - Maps issues to policies
  - Provides supporting evidence

-  **Missing Information Detection**
  - Identifies gaps required for decision-making

---

##  Architecture

User Query
↓
Hybrid Retrieval
→ Vector Search (Qdrant)
→ Keyword Search (BM25)
↓
Re-ranking (LLM-based)
↓
LangGraph Agent (Reasoning)
↓
Final Answer + Evidence + Missing Info


---

##  Tech Stack

| Component | Technology |
|----------|------------|
| LLM | Groq (LLaMA / GPT OSS) |
| Agent Framework | LangGraph |
| Vector DB | Qdrant (local mode) |
| Embeddings | Sentence Transformers |
| Document Parsing | PyMuPDF4LLM |
| Structured Data | Pandas |
| Keyword Search | BM25 |

---

##  Project Structure

│
├── data/ # Provided Input dataset 
├── src/
│ ├── config.py
│ ├── ingest.py
│ ├── build_index.py
│ ├── retriever.py
│ └── agent.py
│
├── main.py
├── requirements.txt
├── README.md
├── .env  (saving groq API)
└── .gitignore


---

##  Setup Instructions

1. Install Dependencies

```bash
pip install -r requirements.txt

2. Configure API Key

Create a .env file in the root directory:
GROQ_API_KEY=your_api_key_here

3. Build Index

python -m src.build_index
This will:

-Ingest all documents
-Generate embeddings
-Store vectors in Qdrant
-Prepare BM25 corpus

4. Run the Agent

python main.py


---

##  Example Queries

Try asking:

1. What compliance issues exist?
2. Which records violate policies?


Output: 

 Ask your question (or type 'exit'): why it’s a compliance problem

 Answer:

**Final Answer**  
The documents reveal a clear compliance breach: candidates are being cleared to start work (or to be onboarded) without satisfying the mandatory evidence requirements set out in the UK right‑to‑work, identity, and criminality policies. The approvals in the emails rely on verbal confirmation or assumptions rather than documented proof, and the candidate packs themselves lack essential evidence (expired visas, missing address proof, absent criminality checks). This violates the company’s statutory and internal compliance obligations and exposes the organization to legal, financial, and reputational risk.

---

### Violations

| # | Policy / Regulation | Specific Violation |
|---|---------------------|--------------------|
| 1 | UK Immigration (Right‑to‑Work) | Candidate CAND‑105’s Skilled Worker visa BRP expired 2024‑12‑31; no replacement share code or new visa evidence provided. |
| 2 | Identity Verification | No address proof for CAND‑105; only passport copy present. |
| 3 | Criminality / Background Checks | No criminality/basic disclosure file for CAND‑105; policy requires a result for all non‑intern roles. |
| 4 | Clearance Process | Email 1 authorises provisional start before BPSS closure; Email 2 clears Liam O’Connor based solely on verbal confirmation. |
| 5 | Contractor Compliance | Email 3 assumes no RTW needed for a contractor billing through a UK limited company; contractors still require valid right‑to‑work evidence. |
| 6 | Documentation Integrity | Analyst cover notes for CAND‑104 and CAND‑105 rely on unverified claims (“updated visa emailed separately”) rather than documented evidence. |

---

### Evidence

| Document | Key Evidence |
|----------|--------------|
| **CAND‑105 Candidate Pack** | • Passport copy present; no address proof.<br>• Skilled Worker visa BRP expired 2024‑12‑31; no replacement share code.<br>• Employment history only from 2024‑06 onward; prior 18 months not evidenced.<br>• No criminality/basic disclosure file. |
| **CAND‑104 Candidate Pack** | • Address proof missing; noted only in analyst note.<br>• Irish passport noted but no supporting evidence.<br>• Only one referee covering 2024‑08 onward; prior employer did not respond. |
| **CAND‑103 Candidate Pack** | • Passport expired 2025‑11‑01; only university ID provided.<br>• Criminality/basic disclosure not required for INTERN role (policy‑specific). |
| **Email 1 (Hiring Director)** | “Approved for provisional start on 2026‑02‑10 … do not treat this email as BPSS closure.” |
| **Email 2 (Hiring Manager)** | “I spoke with Liam’s previous team lead and am comfortable with his background. Please clear him so onboarding is not delayed.” |
| **Email 3 (Recruiter)** | “Since he bills through his own UK limited company, I assume RTW is not needed. Can screening accept that?” |

---

### Missing Information

| Candidate | Missing Evidence | Why It Matters |
|-----------|------------------|----------------|
| **CAND‑105** | • Current right‑to‑work share code or new visa documentation.<br>• Address proof (e.g., utility bill, bank statement).<br>• Criminality/basic disclosure result. | Required to satisfy UK immigration law and internal clearance policy. |
| **CAND‑104** | • Address proof (not in pack).<br>• Formal written confirmation of Irish passport status.<br>• Employment verification from prior employer. | Needed for identity verification and employment history confirmation. |
| **CAND‑103** | • None (policy exempts interns). | No missing evidence. |
| **Contractor (Email 3)** | • Right‑to‑work evidence for the contractor (e.g., share code, visa). | Contractors must also meet RTW requirements. |

---

**Bottom line:** The approvals and candidate packs lack the mandatory documentation required by UK law and company policy. The emails effectively bypass the standard clearance process, creating a compliance risk that could lead to fines, legal action, or reputational damage. All missing evidence must be obtained and documented before any candidate can be legally onboarded.

