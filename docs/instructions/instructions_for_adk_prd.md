# 🧩 ADK Task Planning Template

> 🚨 **Primary Constraints:** Before using this template you **must** reread `AGENTS.md` and `llms-full.txt`. Treat every **Hard rule** as non-negotiable. Do **not** modify ADK source code, add new framework primitives, or import from `refs/**`. Always reuse existing ADK components first. Use code in `refs/**` only to learn coding pattern. Do not reference the code from `refs/**`.

Use this template to produce a `task.md` plan **before writing any code**. The goal is to reason deliberately about architecture, reuse, safety, and validation so that implementation becomes a predictable final step.

---

## 1. Task Overview
- **Objective:** Restate the user goal in your own words, emphasizing desired outcomes over implementation hints.
- **Expected Deliverables:** Identify artifacts that must exist when done (code files, configs, docs, evaluations).
- **Dependencies & Prerequisites:** List credentials, environment setup, prior features, or approvals required.

🧠 **Ask Yourself**
- Have I separated the *business goal* from the *suggested method* so I can honor AGENTS.md reuse rules?
- Which existing agents, tools, docs, or specs relate to this request?

✅ **Do**
- Link to the originating ticket or prompt for traceability.
- Flag any assumptions that need confirmation before implementation.

⛔ **Don’t**
- Promise new components before proving that an ADK equivalent cannot be reused.

---

## 2. Project Analysis & Current State
- **Runtime & Dependencies:** Confirm Python version and key packages (`google-adk` version from `requirements.txt`).
- **Agent Inventory:** List existing agents under `agents/`, labeling root vs. sub-agents and summarizing their responsibilities.
- **Existing Tools & Callbacks:** Document reusable tools, `AgentTool` wrappers, `MCPTool`s, and registered callbacks.
- **Relevant Documentation:** Summarize active specs or progress docs in `docs/features/active/` that intersect this task.

🧠 **Ask Yourself**
- What reusable ADK classes (`LlmAgent`, `SequentialAgent`, `ParallelAgent`, `Runner`, etc.) already satisfy parts of this goal?
- Have I searched the repo (use `rg`) for similar implementations or patterns?
- Do current callbacks, session services, or state keys constrain how new logic must behave?
- Is there an existing Runner configuration or event pipeline this task must reuse?
- Which prompts, configs, or agent definitions are already under version control that I can extend?

✅ **Do**
- Record search keywords and files inspected to demonstrate diligent reuse checks.
- Note any overlapping efforts that require coordination.
- Identify current session or memory services (e.g., `VertexAiSessionService`) that should be reused.
- Reference the code-first assets (prompts/config files) related to this task.

⛔ **Don’t**
- Assume `refs/**` code can be imported at runtime; it is guidance only.
- Treat the current event-driven Runner as optional—understand and align with it.
- Ignore existing tests or monitoring hooks that may already validate this flow.

---

## 3. Strategy & Architecture Options
- **Option A (Preferred):** Describe the approach you will take, explicitly listing the ADK components to reuse.
- **Option B (Alternative):** Describe at least one viable alternative and explain why it is not chosen.
- **Trade-off Summary:** Compare cost, latency, complexity, and maintainability impacts of each option.

🧠 **Ask Yourself**
- Should this logic live in the existing root agent, a sub-agent, or as an `AgentTool`?
- Would a workflow agent (`SequentialAgent`, `ParallelAgent`, `LoopAgent`) satisfy the orchestration requirement better than custom code?
- Have I demonstrated that a custom agent (subclassing `BaseAgent`) is necessary, if proposed?
- Am I keeping agents narrowly scoped (no “mega-agents”) so responsibilities stay clear?
- Does the parent agent retain control and context through Agent-as-a-Tool instead of uncoordinated delegation?
- How will the Runner’s event-driven lifecycle and session state support this architecture?
- Are prompts, configs, and instructions managed as versioned code artifacts that align with this approach?

✅ **Do**
- Tie your decision back to AGENTS.md guidance (e.g., agent-as-tool vs. delegation).
- Highlight how the chosen option preserves or improves observability, state hygiene, and callbacks.
- Prefer workflow agents for deterministic pipelines and document why they fit the process.
- Emphasize modular, specialized agents that compose cleanly within ADK’s Runner.
- Keep configuration/prompt changes in source control as part of the code-first workflow.

⛔ **Don’t**
- Introduce bespoke orchestrators or runners when ADK provides equivalents.
- Collapse multiple domains into one agent or hand off control without oversight.
- Create hidden side channels outside ADK’s event system.

---

## 4. Context & Problem Definition
- **User / Business Need:** Why is this task valuable?
- **Scope & Boundaries:** What is included and explicitly excluded?
- **Success Metrics:** Define measurable outcomes (latency targets, accuracy thresholds, user journeys satisfied).
- **Risks & Assumptions:** Capture unknowns, external dependencies, and mitigations.

🧠 **Ask Yourself**
- How will stakeholders verify success?
- Are there compliance, privacy, or safety considerations that must be reflected in the plan?

✅ **Do**
- Reference any contractual or SLA requirements.

⛔ **Don’t**
- Leave acceptance criteria implicit or subjective.

---

## 5. Technical Requirements
- **Functional Requirements:** Enumerate required capabilities, tool calls, state mutations, and data transformations.
- **Non-Functional Requirements:** Performance, reliability, cost ceilings, observability, accessibility, or localization needs.
- **Callback Plan:** List required callbacks by exact ADK name and explain their purpose.
- **Session State & Artifacts:** Define keys written to `session.state`, artifact expectations, cleanup rules.

🧠 **Ask Yourself**
- Do callbacks already exist that should be extended instead of replaced?
- Could state collisions occur with current keys?
- Is the planned session service persistent enough for the deployment target (avoid default in-memory in prod)?
- Am I using ADK’s state prefixes (`user:`, `app:`, `temp:`) correctly to isolate data?
- Do tools or callbacks need rate limiting, retries, or circuit breakers to stay reliable?
- How will outputs be validated (schema checks, policy filters) before they reach users?
- Will new Python components follow the project standards (type annotations, Google-style docstrings, Ruff formatting, structured logging)?
- Are async patterns required to avoid blocking operations in Python 3.10+?

✅ **Do**
- Include a compliant callback example if one is required:

```python
from google.adk.agents.callback_context import CallbackContext

def before_agent_callback(ctx: CallbackContext) -> None:
    """Ensure required session keys exist before the agent runs."""
    state = ctx.invocation_context.session.state
    state.setdefault("analysis_log", [])
```

- Confirm allowed callback names: `before_agent_callback`, `after_agent_callback`, `before_tool_callback`, `after_tool_callback`, `before_model_callback`, `after_model_callback`.
- Add schema validation or guardrails so outputs meet agreed formats before returning to users.
- Plan for comprehensive pytest coverage (including edge cases) when new code is introduced.
- Specify logging expectations for new logic (levels, key events).

⛔ **Don’t**
- Invent new callback hooks or mutate session state with non-serializable objects.
- Allow long-running synchronous operations to block the Runner; prefer async tools or background jobs.
- Store sensitive or large payloads outside approved state/artifact patterns.
- Return raw external responses without wrapping them in structured, validated payloads.
- Add untyped or undocumented Python functions; keep readability and maintainability high.

---

## 6. ADK Architecture Rules & Compliance
- **Folder & Naming Compliance:** Specify the exact `agents/<agent_name>/agent.py` files affected and confirm `root_agent` export.
- **Reuse Commitments:** Enumerate the ADK modules you will import (e.g., `google.adk.agents.LlmAgent`, `google.adk.tools.AgentTool`, `google.adk.tools.mcp_tool.MCPTool`).
- **Policy Alignment:** Note how you will satisfy AGENTS.md directives on security, memory usage, artifacts, and tool scope.
- **Lint/Test Expectations:** Mention required gates (e.g., `ADKReuseRule`, formatting commands).
- **Runner & Session Strategy:** Explain how the existing event-driven Runner, session service, and memory configuration will be reused or extended safely.

🧠 **Ask Yourself**
- Does any planned change risk violating the project’s folder hierarchy or naming conventions?
- Are there repo-specific lint rules triggered by this change?
- Does the session service choice (e.g., `InMemorySessionService` vs. `VertexAiSessionService`) align with environment needs?
- Do observability hooks (events, logs, metrics) remain intact?

✅ **Do**
- Reference the exact Hard rule you are honoring when relevant.
- Document impacts on event flow, Runner coordination, and state persistence.

⛔ **Don’t**
- Plan to edit ADK internals or bypass reuse heuristics.
- Reconfigure core infrastructure (Runner, session, artifact services) without aligning with existing patterns.

---

## 7. Design Plan
- **Component Breakdown:** Describe each new or modified agent, tool, callback, or helper and how it reuses existing classes.
- **Control & Data Flow:** Outline step-by-step interactions (textually or via diagram) showing delegation, tool usage, and data passing.
- **Error Handling & Recovery:** Define how failures are detected, retried, or surfaced.
- **Observability:** Identify logs, metrics, or traces to add or extend.

🧠 **Ask Yourself**
- Are responsibilities clearly partitioned between root agent, sub-agents, and tools?
- Where do shared resources (state keys, artifacts) need guards to avoid conflicts?
- Am I leveraging workflow agents for structured phases instead of ad-hoc logic?
- How will the Runner’s events, callbacks, or retries surface failures or trigger fallbacks?
- Do I have observability (logs/metrics/traces) at each critical hand-off to support debugging?
- What automated validation or guardrail steps ensure responses meet policy or format requirements?
- How will I enforce single-responsibility design for any new modules or tools?
- Are asynchronous operations and resource usage monitored to avoid bottlenecks?

✅ **Do**
- Reference concrete files or functions that will be extended (e.g., “augment `agents/research_agent/agent.py` to reuse existing summarization tool”).
- Show how session state keys follow ADK prefixes and avoid leaks between agents.
- Include backoff, circuit breaker, or fallback strategies when tools/services fail.
- Outline health checks or synthetic probes that verify the workflow end-to-end.
- Document how new functions will use type hints, docstrings, logging, and comments sparingly yet effectively.

⛔ **Don’t**
- Leave control flow ambiguous or omit failure paths.
- Transfer control to sub-agents without ensuring the root agent can resume orchestration.
- Ship designs without instrumentation or alerting for critical steps.
- Over-engineer or fragment modules beyond what the ADK structure requires.

---

## 8. Tool Integration Plan
- **Tool Inventory:** List every tool involved, noting whether it is built-in (`google.adk.tools.google_search`), an existing FunctionTool, or a new definition.
- **Configuration & Wiring:** Explain how each tool will be configured (parameters, docstrings, return schema) and where it is registered.
- **Authentication & Secrets:** Document required `.env` keys or secret manager references; confirm they already exist or specify setup steps.
- **External Dependencies:** Note MCP servers, APIs, or SDKs to reuse.

🧠 **Ask Yourself**
- Does an existing tool already cover the required functionality?
- Are there rate limits or safety constraints from `llms-full.txt` that affect tool usage?
- Should the tool be `async` due to I/O?
- Do the return types follow a predictable schema (e.g., `{"status": "...", "data": ...}`) that LLMs can reason about?
- Have I handled exceptions internally so the agent receives structured errors?
- Are retries, backoffs, and circuit breakers needed to protect external dependencies?
- How will tool activity be logged for observability without leaking sensitive data?
- Do planned FunctionTools include type annotations and Google-style docstrings?
- Should I provide usage examples or tests demonstrating tool behavior?

✅ **Do**
- Provide example snippets for registering or reusing the tool if necessary.
- Write descriptive docstrings that clarify inputs, outputs, and side effects.
- Favor async implementations for network-bound or long-running tasks to avoid blocking the event loop.
- Document rate limiting, timeout, and fallback behavior for each tool.
- Include type hints for all tool parameters/returns and note pytest coverage expectations.

⛔ **Don’t**
- Duplicate tools or forget to document cleanup/error handling expectations.
- Let tools mutate shared state without coordination or leak credentials in logs.
- Create unbounded retry loops that can saturate external services.
- Omit docstrings or logging that help the LLM and humans understand tool usage.

---

## 9. Implementation Roadmap
Create a sequenced plan that keeps reasoning and validation explicit.

1. **Preparation:** (e.g., verify environment, confirm credentials, align with stakeholders.)
2. **Analysis Updates:** (Capture repository inspections, decisions on reuse, design sign-off.)
3. **Implementation Steps:** (For each step, note the existing files/functions to modify and the ADK components reused.)
4. **Validation Activities:** (List formats/lints/tests to run after relevant steps.)
5. **Documentation & Review:** (Record updates to docs, PR notes, or demos.)
6. **Operational Readiness:** (Configure monitoring, canary tests, rate limits, and alerting before rollout.)

🧠 **Ask Yourself**
- Can steps be safely parallelized, or do dependencies require strict ordering?
- What rollback or mitigation actions exist if a step fails?
- Have I planned timeouts, watchdogs, or circuit breakers for long-running tasks?
- Do stakeholders need updated runbooks or on-call procedures?
- Have I allocated work for updating type hints, docstrings, logging, and pytest coverage?

✅ **Do**
- Include checkpoints for stakeholder review or code review syncs if required.
- Schedule synthetic queries or canary workflows before and after deployment.
- Note when to run `pytest --maxfail=1 --disable-warnings --cov` (or project-appropriate command) to maintain coverage targets.

⛔ **Don’t**
- Skip validation steps even if the code change seems minor.
- Deploy without verifying observability and alerting paths.

---

## 10. Validation & Compliance Checklist
- **Quality Gates**
  - [ ] Planned formatting (`./autoformat.sh`) and linting (`ruff`, `pylint`, etc.) are scheduled.
  - [ ] Unit/integration/eval tests identified with expected coverage (target ≥ agreed pytest coverage).
  - [ ] Manual QA (e.g., `adk web`, `adk api_server`) defined if applicable.
- **Policy Confirmation**
  - [ ] All AGENTS.md Hard rules addressed explicitly.
  - [ ] `llms-full.txt` model, parameter, and rate-limit guidance honored.
  - [ ] No runtime imports from `refs/**`; patterns only referenced.
  - [ ] Only approved callbacks (`before/after` agent/tool/model) are used.
  - [ ] Workflow agents, Runner configuration, and session services validated to support the new flow.
  - [ ] Rate limiting, retry, timeout, and circuit-breaker strategies documented for each external dependency.
- **Documentation**
  - [ ] “ADK search summary” placeholder prepared for future PR notes.
  - [ ] Runbooks, monitoring dashboards, and synthetic test plans updated.
- **Open Risks**
  - [ ] Remaining risks, unknowns, or follow-ups documented for reviewers.

🧠 **Ask Yourself**
- What evidence will I provide to reviewers to prove compliance?
- Are there outstanding approvals or sign-offs needed?
- How will this feature be monitored post-deployment and who responds to alerts?

✅ **Do**
- Capture links to logs, traces, or test artifacts you plan to share.
- Provide references to canary/synthetic run results and alert configurations.

⛔ **Don’t**
- Mark the checklist complete without concrete proof.
- Leave monitoring gaps for critical user journeys.

---

### 📌 Final Reflection (Optional but Recommended)
> Summarize the most important design decisions, remaining risks, and how the plan enforces ADK reuse, safety, and compliance (agent specialization, workflow orchestration, state hygiene, tool safety, event-driven Runner alignment). Limit to 3–5 sentences for quick reviewer consumption.
