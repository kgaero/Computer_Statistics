**ALWAYS → Follow the instruction in the file below and create or update the documentation/Improvement_ideas.md based on the code for AI agents in the src folder**

**Purpose:** After **every** code or docs change, propose and record improvement ideas so we continuously enhance quality, reliability, and developer experience.

## What to add each time

For the current change, add **at least 1 idea** in each of the applicable buckets below along with a justification for the change. (skip only if truly N/A, and say why):

1. **New Features** – capabilities users or internal devs are missing
2. **Improvements** – refactors, UX/DX polish, performance, reliability, cost, maintainability
3. **Testing Ideas** – unit/integration/e2e/property/fuzz tests, determinism & flake reduction
4. **Bugs** – known defects, repro notes, suspected root causes
5. **Security & Compliance** – authZ/authN, secrets, PII handling, logging, model-safety rails
6. **Observability** – logs, metrics, traces, red/black box evals, dashboards, SLOs
7. **Tooling & DX** – lint/format, pre-commit hooks, task runners, CI speedups, templates
8. **Docs & Examples** – gaps, runnable examples, ADRs, READMEs, agent diagrams
9. **ADK/Agentic-Specific** – sub-agent contracts, state keys, tool/callback hygiene, cost/token guardrails, loop termination, delegation strategies

> If none apply for a bucket, add “*No changes; N/A for this commit*” so reviewers know you considered it.

---

## How to propose ideas (multi-angle prompts)

When brainstorming, consider:

* **Performance/Cost:** hot paths, LLM token usage, caching, batch calls, streaming, pagination
* **Reliability:** retries, idempotency, timeouts, backoff, circuit breakers, dead-letter queues
* **Safety:** tool-call constraints, input validation, red-team prompts, jailbreaking mitigations
* **Maintainability:** coupling, cohesion, cyclomatic complexity, module boundaries, naming
* **ADK Architecture:** `sub_agents` correctness, state read/write keys, callback side effects, loop stop conditions
* **Testing Depth:** golden files, fixtures, seed control, hypothesis tests, chaos tests
* **Observability:** structured logs, span attributes, correlation ids, P99 latency, cost per task
* **DX:** dev container, `make`/`taskfile`, pre-commit, codegen, scaffolds, one-click run scripts
* **Docs:** runnable snippets, architecture charts, failure modes, FAQ, troubleshooting

---

## Required metadata per idea (keep it short but precise)

Each idea must have:

* **Title**: concise, imperative
* **Category**: one of the buckets above
* **Problem**: 1–2 lines (what’s painful or risky?)
* **Proposal**: 2–6 lines (how to fix; alternatives if any)
* **Impact / Effort**: use **RICE** or **ICE**

  * `RICE: Reach(1–5), Impact(1–5), Confidence(1–5), Effort(1–5)` → **Score = (R*I*C)/E**
  * or `ICE: Impact(1–5), Confidence(1–5), Effort(1–5)` → **Score = (I*C)/E**
* **Risk**: low/med/high + brief note
* **Dependencies**: files, services, agents, state keys
* **Links**: PRs, issues, logs, traces, benchmarks
* **Acceptance Criteria**: bullet list; testable and binary
* **Owner** (optional) & **Target Release** (optional)

---

## File structure & ordering

* Append new ideas at the **top** under “🆕 This Cycle” so they’re visible.
* Keep “📚 Backlog” for lower-priority items (sorted by score desc).
* Move items from “🆕 This Cycle” to “📚 Backlog” if deprioritized, or to “✅ Done (Changelog)” when completed (with PR link).

---

## Markdown template (paste into `documentation/Improvement_ideas.md`)

```markdown
# Improvement Ideas

## 🆕 This Cycle

### [Title]
- **Category:** New Features | Improvements | Testing | Bugs | Security & Compliance | Observability | Tooling & DX | Docs & Examples | ADK/Agentic-Specific
- **Problem:** <one-liner>
- **Proposal:** 
  - <approach 1>
  - <approach 2 (alternative, optional)>
- **RICE:** R=<1–5> I=<1–5> C=<1–5> E=<1–5> → **Score = (R*I*C)/E**
  - *(or)* **ICE:** I=<1–5> C=<1–5> E=<1–5> → **Score = (I*C)/E**
- **Risk:** low|med|high — <why>
- **Dependencies:** <files, agents, tools, state keys>
- **Links:** <PRs/issues/logs/benchmarks>
- **Acceptance Criteria:**
  - [ ] <criterion 1>
  - [ ] <criterion 2>
  - [ ] <criterion 3>

---

## 📚 Backlog (scored, descending)
<!-- Move lower-priority items here; keep sorted by score -->

## ✅ Done (Changelog)
- YYYY-MM-DD — [Title] — PR #123 — Result: <1-line outcome>
```

---

## Example ideas (short but useful)

**Example 1 – ADK/Agentic-Specific**

* **Title:** Add loop termination guard for `iterative_refinement_loop`
* **Category:** ADK/Agentic-Specific
* **Problem:** Loop sometimes runs 4–5 iterations without new evidence; token & cost waste.
* **Proposal:** Add `controls.max_iterations=3` and stop when `evaluation_result.success_criteria_met=true`.
* **ICE:** I=5 C=4 E=2 → **10**
* **Risk:** low — config-only
* **Dependencies:** `LoopAgent` config, `evaluation_result` key, runner config
* **Links:** N/A
* **Acceptance Criteria:**

  * [ ] Loop ends ≤ 3 iterations when criteria met
  * [ ] Token usage ↓ ≥ 25% in regression run
  * [ ] No change in final report quality

**Example 2 – Testing**

* **Title:** Property tests for tool-call argument validation
* **Category:** Testing
* **Problem:** Tool-call failures on unexpected inputs; brittle unit tests.
* **Proposal:** Add Hypothesis tests over tool schemas; fuzz invalid types & ranges.
* **ICE:** I=4 C=4 E=2 → **8**
* **Risk:** low
* **Dependencies:** tool schemas, CI runner
* **Links:** failing run IDs #abc123
* **Acceptance Criteria:**

  * [ ] ≥ 90% schema branches covered
  * [ ] No runtime value errors for valid inputs
  * [ ] Meaningful errors for invalid inputs

**Example 3 – Observability/Cost**

* **Title:** Per-agent token/cost metrics with P95/P99
* **Category:** Observability
* **Problem:** Cost spikes with multi-agent tasks; no per-agent visibility.
* **Proposal:** Emit `tokens_in/out` and `$` per agent; dashboard with P95/P99.
* **RICE:** R=4 I=4 C=3 E=3 → **16**
* **Risk:** med — dashboard wiring
* **Dependencies:** logging, metrics backend
* **Acceptance Criteria:**

  * [ ] Dashboard shows per-agent token & cost P95/P99
  * [ ] Alerts on 2× baseline cost for 24h
  * [ ] PR includes example screenshots

---

## Workflow (enforcement)

1. **On every PR** touching code/docs, update `documentation/Improvement_ideas.md` using the template above.
2. If no ideas are relevant, add “*No new ideas for this change*” under **🆕 This Cycle** and explain why.
3. Reviewers must **block** PRs that skip this section or lack scoring/criteria.
4. When an idea ships, **move it to “✅ Done (Changelog)”** with PR link and one-line result.

---

## Quality bar (what reviewers check)

* Problem is real & specific (not vague).
* Proposal is actionable, with at least one alternative considered (when relevant).
* Scoring is present (RICE or ICE) and roughly sane.
* Risks, deps, and acceptance criteria are listed.
* Category is chosen appropriately.

---