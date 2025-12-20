# 🧭 instruction_for_google-adk.md  
**ALWAYS → Follow the instruction in the file below and create or update the docs/ai_docs/google-adk.md based on the code for AI agents in the agents folder**


**Purpose:**  
Define the standard operating procedure for creating and maintaining `docs/ai_docs/google-adk.md` — the **digital twin** of all AI agents implemented with **Google ADK** in this repository.

---

## 1️⃣ 🎯 Objective  

`docs/ai_docs/google-adk.md` acts as a **live mirror** of the multi-agent system defined in code.  
It ensures human developers and coding agents understand **the current AI agent architecture**, preventing changes that break dependencies or create circular failures.

Update it **immediately after any code modification** to AI agents.

**Outcome:**  
- No changes are made in isolation.  
- Relationships among agents remain coherent.  
- Coding agents can reason safely about downstream effects.

**Before every update, re-read and honor:**  
- `AGENTS.md` → framework rules & ADK-reuse policy.  
- `llms-full.txt` → model and API parameters (never invent).  
- `docs/instructions/instructions_for_docs.md` → documentation quality and structure requirements.

---

## 2️⃣ 📚 Reference Inputs (Read-Only)

| File | Purpose |
|------|----------|
| **`AGENTS.md`** | ADK usage policy, naming conventions, and repo-wide rules. |
| **`llms-full.txt`** | Canonical list of valid ADK models, APIs, and agent types. |
| **`docs/instructions/instructions_for_docs.md`** | Documentation structure and example format. |
| **Project code (`agents/**/agent.py`)** | Source for actual agent wiring, tools, callbacks, and session state (read-only). |

> Never modify any of the files above. Treat them strictly as inputs to generate `docs/ai_docs/google-adk.md`.

---

## 3️⃣ 🧩 Scope of `docs/ai_docs/google-adk.md`

Your `docs/ai_docs/google-adk.md` must contain the following, **in order**:

1. 🧭 **Agent Hierarchy Overview**  (root → all descendants)
2. 🧠 **Root Agent Section**  (purpose, sub-agents, tools, callbacks, session state I/O, model, budget/policy)
3. ⚙️ **Sub-Agent Sections** (recursively)  
4. 🔗 **Agent Connection Mapping**  (text tree diagram)
5. 🧱 **Canonical Session State Keys**  (YAML summary across the whole system)
6. 🔄 **Update Protocol & Consistency Checks** (how to keep it in sync)

Together, these sections form a **complete digital twin** — a markdown-based mirror of your ADK architecture.

---

## 4️⃣ ✍️ Authoring Rules

- Document **what exists in code only** — no speculation or future intent.  
- Match all names **exactly** as in Python (`LlmAgent`, `SequentialAgent`, `LoopAgent`, etc.).  
- Prefer **lists and short phrases** to long paragraphs.  
- Use icons: **✅ implemented**, **🚧 in progress**, **❌ deprecated**.  
- When an agent is renamed, moved, or removed, **update every occurrence**.  
- Each section should read like a declarative system specification — **not** prose.

---

## 5️⃣ 📑 Canonical Structure

Follow this structure exactly whenever you rebuild or update `docs/ai_docs/google-adk.md`.

---

### 5.1 🧭 Agent Hierarchy Overview

```
<root_agent_name> (<AgentType>) ✅
├─ <child_agent_1> (<AgentType>)
│  ├─ <grandchild_a> (<AgentType>)
│  └─ <grandchild_b> (<AgentType>)
└─ <child_agent_2> (<AgentType>) 🚧
```

**Tips:**  
- Order agents as they appear in code (`sub_agents=[...]`).  
- Show only **active** agents. Move removed ones to a **Deprecated** section if needed.  

---

### 5.2 🧠 Root Agent

* **Agent Name:** `<root_agent_name>`  
* **Type:** `LlmAgent | SequentialAgent | ParallelAgent | LoopAgent | BaseAgent (custom)`  
* **Purpose:** Concise one-line summary of its role.  
* **Sub-agents:** `[<sub_agent_1>, <sub_agent_2>, ...]`  
* **Tools:** `tool_name (params) — purpose`  
* **Callbacks:** `callback_name — when triggered / why`  
* **Session State:**  
  - **reads:** `[state_key_1, state_key_2, …]`  
  - **writes:** `[state_key_3, state_key_4, …]`  
* **Model:** from `llms-full.txt` (e.g., `gemma-3-27b-it`)  
* **Budget / Policy:** `{ max_tokens, max_cost_usd, allow_web, max_iterations, … }`  

---

### 5.3 ⚙️ Sub-Agent Sections (repeat per agent)

* **Agent Name:** `<agent_name>`  
* **Type:** `<AgentType>`  
* **Purpose:** One-liner describing the agent’s specific task.  
* **Sub-agents:** `[ ... ]` (if any)  
* **Tools:** `[ ... ]` (if any)  
* **Callbacks:** `[ ... ]` (if any)  
* **Session State:** **reads** `[ ... ]`, **writes** `[ ... ]`  
* **Model:** `<model or N/A>`  
* **Special Notes:** (optional) conditional logic, iteration, or I/O considerations.

---

### 5.4 🔗 Agent Connection Mapping

```
<root_agent> (<Type>)
├─ <child_agent_A> (<Type>) + key callbacks/tools
│  ├─ <grandchild_A1> (<Type>)
│  └─ <grandchild_A2> (<Type>)
└─ <child_agent_B> (<Type>)
```

Keep it **readable in 5–10 seconds**.  
Avoid descriptions — list names, hierarchy, and essentials only.

---

### 5.5 🧱 Session State (Canonical Keys)

Summarize all session variables across the system:

```yaml
user_request: { description: "...", producer: "root_agent", consumers: ["..."] }
research_plan: { description: "...", producer: "plan_generator", consumers: ["research_pipeline"] }
evaluation_result: { description: "...", producer: "research_evaluator", consumers: ["iterative_refinement_loop"] }
final_report: { description: "...", producer: "report_composer", consumers: [] }
controls: { max_cost_usd: number, max_tokens: number, allow_web: boolean }
telemetry: { token_usage: number, cost: number, tool_calls: [] }
```

> **Rule:** If any agent changes its read/write keys, update this section and its references.

---

## 6️⃣ 🔄 Update Protocol (Run After Every Agent Change)

### Step 1 — Detect  
Monitor for any change to:
- `agents/**/agent.py`
- Agent imports, wiring, or sub-agent composition
- `output_key` / session I/O definitions
- Model configuration or callback registration

### Step 2 — Rebuild  
Regenerate:
- Hierarchy overview  
- Root + sub-agent sections  
- Connection map  
- Session state keys  

### Step 3 — Validate  
Confirm:
- All names match code **exactly** (case-sensitive).  
- Parent `sub_agents` lists mirror code order.  
- Tools and callbacks exist and are spelled correctly.  
- Models are valid per `llms-full.txt`.  
- Implementation adheres to ADK reuse rules in `AGENTS.md`.

### Step 4 — Commit  
Add or update footer:

```
<!-- Updated on YYYY-MM-DD by AI Coding Agent -->
```

Commit doc and code **together** in the same PR.

---

## 7️⃣ ✅ Pre-Merge Validation Checklist

- [ ] `docs/ai_docs/google-adk.md` updated in same PR as code.  
- [ ] All agent names/types/models/tools/callbacks verified.  
- [ ] Session-state table matches reads/writes.  
- [ ] No stale or deprecated agents referenced.  
- [ ] ADK reuse compliance confirmed.  

---

## 8️⃣ 📎 Appendix — Example Structure

Use the following as your **reference example** for clarity, structure, and level of detail expected in `docs/ai_docs/google-adk.md`.

---

#### 🧩 Agent Architecture Overview

This document provides a complete implementation of a sophisticated **competitor analysis** workflow with iterative QA, budget control, and auditable sourcing, designed using **Google ADK** best practices. 

---

#### **Workflow Summary**

* **Planning Phase**: Interactive plan generation and refinement with human-in-the-loop checkpoints
* **Research Execution**: Deterministic pipeline with sectionized search + collection + grounding
* **Quality Assurance**: Loop with evaluation, targeted re-search, and hallucination checks
  ✅ **Enhanced Search Executor Callback Implemented** (rank/merge/dedup + cost/budget guard)
* **Final Output**: Publication-ready Markdown report + Zotero/CSL JSON citations + appendix of sources


---

## 🧭 Agent Hierarchy & Configuration

### **Root Agent: Interactive Planner**

* **Agent Name**: `competitor_analysis_agent`
* **Agent Type**: `LlmAgent`
* **Purpose**: Human-facing orchestrator for scope, acceptance criteria, and plan approval
* **Sub-agents**: `research_pipeline`, `report_composer`
* **Tools**:

  * `AgentTool(plan_generator)` (only when `research_plan.status == "draft"`)
  * `StateTool(export_state_snapshot)` (one-click audit/export)
* **Callbacks**:

  * `initialize_research_state` (seed keys, budgets, guardrails)
  * `checkpoint_gate` (requires user approval on plan & scope changes)
* **Session State**: reads `user_request`; writes `research_context`, `research_plan`, `controls`
* **Model**: `gemma-3-27b-it`
* **Budget/Policy**:

  * `controls.max_cost_usd = 12.00`
  * `controls.max_tokens = 180k`
  * `controls.allow_web = true`


---

### **Plan Generator Agent**

* **Agent Name**: `plan_generator`
* **Agent Type**: `LlmAgent`
* **Purpose**: Produce a machine-actionable plan with tasks, hypotheses, and evidence targets
* **Sub-agents**: None
* **Tools**: `google_search (topic sanity only; 3 calls max)`
* **Callbacks**: `validate_plan_schema` (JSON schema enforcement)
* **Session State**: reads `user_request`, `research_context`; writes `research_plan`
* **Model**: `gemma-3-27b-it`


---

### **Research Pipeline**

* **Agent Name**: `research_pipeline`
* **Agent Type**: `SequentialAgent`
* **Purpose**: Execute the approved plan deterministically
* **Sub-agents**: `section_planner`, `section_researcher`, `iterative_refinement_loop`
* **Tools**: none (delegates)
* **Callbacks**: `pipeline_progress_logger`
* **Session State**: processes `research_plan` → `research_sections` → `research_findings`
* **Model**: N/A


---

### **Section Planner Agent**

* **Agent Name**: `section_planner`
* **Agent Type**: `LlmAgent`
* **Purpose**: Expand each plan section into granular steps & evidence contracts
* **Sub-agents**: None
* **Tools**: None
* **Callbacks**: `token_budget_guard`
* **Session State**: reads `research_plan`; writes `research_sections` (with step DAG)
* **Model**: `gemma-3-27b-it`


---

### **Section Researcher Agent**

* **Agent Name**: `section_researcher`
* **Agent Type**: `LlmAgent`
* **Purpose**: Execute step DAG with structured search, extraction, grounding
* **Sub-agents**: None
* **Tools**:

  * `google_search`
  * `web_fetch` (HTML/PDF fetcher with boilerplate pruning)
  * `pdf_screenshot_ocr` (for tables/figures)
  * `table_extractor` (HTML → normalized CSV blocks)
* **Callbacks**:

  * `collect_research_sources_callback` (append to `sources_log`)
  * `source_dedup_normalizer` (canonicalize URLs, strip tracking params)
* **Session State**: reads `research_sections`; writes `research_findings` (per section: facts, quotes, tables, `source_ids`)
* **Model**: `gemma-3-27b-it`


---

### **Iterative Refinement Loop**

* **Agent Name**: `iterative_refinement_loop`
* **Agent Type**: `LoopAgent`
* **Purpose**: Evaluate findings vs. criteria, repair gaps, enforce precision
* **Sub-agents**: `research_evaluator`, `enhanced_search_executor`, `escalation_checker`
* **Tools**: none
* **Callbacks**: `loop_budget_guard`, `loop_telemetry_logger`
* **Session State**: manages `evaluation_result`, `repair_actions`, updates `research_findings`
* **Stop Conditions**:

  * All `success_criteria` met **AND** no critical `unresolved_questions`
  * OR budget/time/iteration ceilings (`controls.max_iterations = 3`)


---

### **Research Evaluator Agent**

* **Agent Name**: `research_evaluator`
* **Agent Type**: `LlmAgent`
* **Purpose**: Score coverage, credibility, recency, contradiction risk
* **Sub-agents**: None
* **Tools**: None
* **Callbacks**: `hallucination_check` (flags unverifiable claims)
* **Session State**: reads `research_findings`; writes `evaluation_result`
* **Model**: `gemma-3-27b-it`


---

### **Enhanced Search Executor Agent**  ✅ IMPLEMENTED

* **Agent Name**: `enhanced_search_executor`
* **Agent Type**: `LlmAgent`
* **Purpose**: Targeted follow-ups from evaluator’s `repair_actions`
* **Sub-agents**: None
* **Tools**:

  * `google_search` (with **query expansion** + **site:** constraints)
  * `web_fetch`, `pdf_screenshot_ocr`, `table_extractor`
* **Callbacks**:

  * `collect_research_sources_callback` (append & tag as `phase:"repair"`)
  * `rank_merge_dedup_callback` (**NEW**: reciprocal-rank fusion + domain diversity)
  * `budget_checkpoint_callback` (deny over-budget expansions)
* **Session State**: reads `repair_actions`, `research_findings`; writes `enhanced_research_findings`
* **Model**: `gemma-3-27b-it`


---

### **Escalation Checker Agent**

* **Agent Name**: `escalation_checker`
* **Agent Type**: `BaseAgent` (custom)
* **Purpose**: Decide loop termination / human escalation
* **Session State**: reads `evaluation_result`; writes `escalation_decision`
* **Model**: N/A


---

### **Report Composer Agent**

* **Agent Name**: `report_composer`
* **Agent Type**: `LlmAgent`
* **Purpose**: Produce final Markdown with inline citations and CSL JSON
* **Sub-agents**: None
* **Tools**: `citation_formatter (CSL-JSON)`, `table_renderer (Markdown)`, `image_manifest_builder`
* **Callbacks**:

  * `citation_replacement_callback` (`[1]` style → `(Author, Year)` or footnotes)
  * `appendix_builder_callback` (Sources log → Appendix A)
* **Session State**: reads `research_findings`, `sources_log`; writes `final_report`, `citations_csl_json`
* **Model**: `gemma-3-27b-it`


---

## 🔗 Agent Connection Mapping (Example)

```
competitor_analysis_agent (LlmAgent – Root)
├─ Tools: [AgentTool(plan_generator), StateTool(export_state_snapshot)]
├─ Callbacks: [initialize_research_state, checkpoint_gate]
├─ Sub-agents: [research_pipeline, report_composer]
│  └─ research_pipeline (SequentialAgent)
│     ├─ section_planner (LlmAgent) 
│     ├─ section_researcher (LlmAgent + google_search, web_fetch, pdf_screenshot_ocr, table_extractor)
│     └─ iterative_refinement_loop (LoopAgent)
│        ├─ research_evaluator (LlmAgent + hallucination_check)
│        ├─ enhanced_search_executor (LlmAgent + google_search)  ✅ rank_merge_dedup_callback
│        └─ escalation_checker (Custom BaseAgent)
└─ report_composer (LlmAgent + citation_formatter, appendix_builder)
```



---

## 🧱 Session State (Canonical Keys — Example)

```yaml
user_request: { objective, constraints, target_competitors, timebox_days }
research_context: { industry, glossary, assumed_knowledge }
research_plan: { status, sections[], success_criteria[], risks[] }
research_sections: { sections: [{ id, steps[], evidence_contract }] }
research_findings: { sections: [{ id, facts[], tables[], quotes[], source_ids[] }] }
enhanced_research_findings: { patches: [{ section_id, diffs[] }] }
evaluation_result: { coverage, credibility, recency, gaps[], repair_actions[] }
sources_log: [{ id, url, title, domain, published_at, accessed_at, phase, hash }]
citations_csl_json: [{ id, type, author[], issued, title, URL, accessed }]
final_report: "### Title...\n"
controls: { max_cost_usd, max_tokens, max_iterations, allow_web, policy_flags }
telemetry: { token_usage, cost, tool_calls[], warnings[] }
```

---

```
<!-- Auto-updated by ADK AgentDoc Generator v1.x -->
```
