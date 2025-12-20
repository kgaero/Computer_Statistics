# 🧭 Google ADK Planning Playbook

This guide defines how AI coding agents must produce architecture plan before modifying the agents in Google ADK codebase. Follow every rule below to keep the multi-agent system coherent and observable.

---

## 1️⃣ 🎯 Objective

Generate a **single architecture plan** that explains how the requested changes will alter the agent hierarchy, tools, state, and orchestration. The plan must be saved as `docs/ai_docs/google-adk_PLAN.md`.

**Outcomes**
- No change is made without a peer-reviewable plan.
- Dependencies and state hand-offs remain sound.
- Future agents can reason about impact and testing without guesswork.

---

## 2️⃣ 📚 Mandatory Inputs (read every time)

| Input | Why it matters |
|-------|----------------|
| `AGENTS.md` | Source of truth for ADK usage rules, naming, and guardrails. |
| `llms-full.txt` | Canonical reference for valid models, tools, and constraints. |
| `docs/ai_docs/google-adk.md` | Current documented architecture; align plan updates with actual state (skip if missing). |
| `agents/**/agent.py` (read-only) | Confirms real wiring, tools, and callbacks you must preserve or modify. |

> Never edit the inputs above. Treat them as read-only data sources for your plan.

---

## 3️⃣ 🧪 When a Plan Is Required

- Any request that touches agent wiring, tools, callbacks, session state, or evaluation flow.
- When adding, removing, or renaming agents or tools.
- When code or documentation changes could desynchronize `docs/ai_docs/google-adk.md`, if present.
- When the latest plan does not already cover the proposed work.

If the work is purely editorial documentation or test updates with no architecture impact, confirm in writing that no plan is needed before proceeding.

---

## 5️⃣ 🛠️ End-to-End Planning Workflow

### Step 1 — Confirm Intent
- Restate the user request in your own words.
- Identify which agents, tools, or state keys could be affected.
- Clarify open questions before moving forward.

### Step 2 — Inventory Current Architecture
- Read `docs/ai_docs/google-adk.md` and the relevant `agents/**/agent.py` files.
- Capture existing agent responsibilities, sub-agent lists, tools, callbacks, and state interactions.
- Note any gaps or inconsistencies between docs and code that the plan must resolve.

### Step 3 — Map the Delta
- Decide which existing ADK components will be reused (e.g., `google.adk.agents.LlmAgent`, `AgentTool`, `StateTool`).
- Identify additions vs. modifications vs. removals.
- Record risks, constraints, compliance or guardrail impacts (budget caps, tool limits, privacy).

### Step 4 — Draft the Architecture Plan
- Use the required template (see Section 6) and fill in every field with concise, testable statements.
- Reference concrete file paths, agent names, state keys, and tool classes you will touch.
- Explain how the plan upholds `AGENTS.md` rules (reuse-first, no custom base classes, etc.).

### Step 5 — Validate Readiness
- Cross-check that each proposed change aligns with available ADK components in `llms-full.txt`.
- Ensure session state flows include read/write ownership and termination criteria.
- Double-check numbering, headings, and markdown lint (80 char lines when possible).

### Step 6 — Publish
- Save the final Markdown to `docs/ai_docs/google-adk_PLAN.md`.
- Avoid trailing whitespace or unfinished TODOs.
- Reference this plan in your subsequent PR/summary when executing the work.

---

## 6️⃣ 🧱 Required Plan format

The output format in `docs/ai_docs/google-adk_PLAN.md` must contain the multi agent architecture in the example format as specified in the appendix below.

---

## 7️⃣ ✅ Quality Checklist (run before finalizing)

- [ ] All required inputs were re-read this session (reference timestamps if possible).
- [ ] Every change references existing ADK classes/tools instead of custom builds unless explicitly justified.
- [ ] File paths and agent names match repo casing exactly.
- [ ] State transitions cover both success and failure paths.
- [ ] Plan aligns with constraints in `AGENTS.md` (no new base classes, sub-agent patterns honored).
- [ ] Plan is concise (prefer <800 words) yet complete—no vague placeholders.
- [ ] Example or appendix (Section 8) was used for formatting consistency.

Document in the plan that each checklist item was met. If something cannot be satisfied, explain why and flag for human review.

---

## 8️⃣ 📎 Appendix — Example Reference

Use the following example as a style and depth benchmark when authoring `docs/ai_docs/google-adk_PLAN.md`. Adapt the structure to your scenario while keeping the required sections above.

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
* **Model**: `gemini-2.5-flash`
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
* **Model**: `gemini-2.5-flash`

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
* **Model**: `gemini-2.5-flash`

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
* **Model**: `gemini-2.5-flash`

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
* **Model**: `gemini-2.5-pro`

---

### **Enhanced Search Executor Agent** ✅ IMPLEMENTED

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
* **Model**: `gemini-2.5-flash`

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
* **Model**: `gemini-2.5-pro`

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
