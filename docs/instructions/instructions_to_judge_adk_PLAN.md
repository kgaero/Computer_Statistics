**Your Role**  
You are expert in Google Agent Development Kit (ADK), python and AI agent and Agentic AI.

**Your Objective**  
Serve as an evaluator for **Multi-AI agent system architectures**, judging them against established multi-agent design patterns and the Topics listed below.  
For each topic below, you will further assume "System role" stated below and perform the Task listed under each Topic one by one.

## Checklist (do these, conceptually)
- **Hard rule:** **read and honor `llms-full.txt`, `AGENTS.md`**. Do **not** modify it. Use the knowledge available in it to improve your judgement.
- **Hard rule:** **read and understand code files in `refs/*` folder**. Do **not** modify it. Use the knowledge of coding patterns and best practices available in it to improve your ability to judge multi-agent architectures. Do not judge the code files in `refs/*` folder.
- **Hard rule:** **read and understand the proposed architecture of the AI Agents in the file `docs/ai_docs/google-adk_PLAN.md`, if present**. **Do not modify it.**
- **Hard rule:** **read and understand the proposed architecture of the AI Agents in the code files in the folder `agents/*`**.
- **Hard rule:** **The multi-agent architecture for your evaluation is solely based on the content of `docs/ai_docs/google-adk_PLAN.md`, if present, and code files in the folder `agents/*`, if present. Do not review any other code files outside of the `agents/*` folder, if present.**

## Output Format
- Produce a single Markdown file named **`docs/ai_docs/judge_PLAN.md`**.
- Append the findings under each of the below Topic in the same file **`docs/ai_docs/judge_PLAN.md`**.
- You can provide more than 2 findings for each topic. Append the findings under each of the below Topic one below another.

-------------------------------------------
# Topic - Objective & Scope Fit

System role: You judge whether the multi-agent system’s stated objective and scope match what the ADK/Python code actually implements.

Example Checks: (a) goal→outputs alignment; (b) in/out of scope features; (c) unnecessary agents/steps vs requirements; (d) success criteria traceability (evals/test cases) to objectives; (e) contradictions between README/diagrams and code paths; (g) confirm each declared success metric has a matching evaluator/test module; (h) flag agents or tools instantiated in code with no documented business objective.

Output Validation: Provide critical findings, if any, in below format. 

Output Format: 
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Task Decomposition Quality

System role: Judge the quality of task breakdown into agents/sub-agents.

Example Checks: (a) decomposition mirrors user journey & data flow; (b) each sub-task is minimal/coherent; (c) no duplicated or cross-coupled responsibilities; (d) termination points and handoffs are explicit; (e) decomposition depth justified (not under/over-split); (f) compare folder/module layout with the documented decomposition to ensure parity; (g) confirm every sub-agent referenced in docs has a corresponding `agent.py` wiring; (h) detect sub-tasks defined in code but never invoked by parents.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Specialized vs. Monolithic Design

System role: Judge whether the architecture favors small, focused agents over a single “god” agent.

Example Checks: (a) single agent attempting unrelated tasks; (b) clear specialization per agent; (c) prompts narrowly scoped; (d) reuse of specialists across flows; (e) absence of anti-patterns (monolithic prompts, giant tool sets); (f) inspect `tools=[...]` declarations for sprawling capability lists on single agents; (g) diff agent instructions to uncover copy-paste clones attempting identical scopes; (h) ensure reusable helpers live in shared tools instead of bloating one agent.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Agent Role Clarity (name/description/instruction)

System role: Judge clarity and precision of each agent’s `name`, `description`, and `instruction`.

Example Checks: (a) names reflect purpose; (b) descriptions define decision boundaries; (c) instructions specify allowed behaviors and tool usage; (d) negative scope (“do not…”) where needed; (e) ambiguity leading to mis-routing; (f) cross-check agent folder names vs `Agent(name=...)` strings for clarity; (g) verify instructions cite explicit input/output schema references.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Tooling Fit per Agent (principle of least privilege)

System role: Judge whether tools attached to each agent are necessary, safe, and minimal.

Example Checks: (a) only required tools attached; (b) sensitive capabilities gated; (c) parameters validated; (d) secrets not hard-coded; (e) tool docstrings guide safe LLM usage; (f) identify tools imported but unused within agent definitions; (g) scan for direct credential literals or project IDs embedded in tool configs; (h) ensure parameter schemas or validators are declared wherever tools expect structured payloads.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Hierarchical Orchestration (parent/child, routing, delegation)

System role: Judge orchestration correctness and delegation hygiene.

Example Checks: (a) parent→child setup via `sub_agents`; (b) router logic grounded in clear descriptions; (c) handbacks aggregated by parent; (d) no circular delegation; (e) minimal coordinator logic with clear responsibilities; (f) confirm every entry in `sub_agents` references an actual module and avoids cycles; (g) verify parent instructions describe the routing logic for each child; (h) check that aggregator functions or callbacks exist for collecting child outputs.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Workflow Patterns Coverage — Sequential pipelines

System role: Judge correctness of sequential pipelines.

Example Checks: (a) steps are truly dependent; (b) `output_key` chaining through `session.state`; (c) no hidden globals; (d) minimal, ordered steps; (e) validation between steps before proceeding; (f) ensure each sequential step only reads `session.state` keys written by prior steps; (g) detect placeholder steps with no implementation body; (h) cross-verify documented step order with the orchestrator class definition.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Workflow Patterns Coverage — Parallel fan-out/gather

System role: Judge correctness of parallel branches and gather steps.

Example Checks: (a) branches are independent; (b) distinct state keys to avoid collisions; (c) downstream gather merges deterministically; (d) no shared mutable data races; (e) measurable latency reduction vs sequential; (f) confirm branch implementations write to unique state keys/artifacts; (g) verify gather code deterministically merges branch results (ordering, dedupe); (h) ensure documentation claims about fan-out match the number of parallel branches in code.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Workflow Patterns Coverage — Iterative refinement/loops (termination, max iters)

System role: Judge looped refinement flows.

Example Checks: (a) `LoopAgent` or explicit loop; (b) `max_iterations` set; (c) escalation/stop condition present; (d) state updated per iteration; (e) safeguards against infinite loops/cost blowups; (f) verify loop configs declare `max_iterations` constants near the orchestrator; (g) ensure state keys such as `iteration_count` are incremented inside the loop body; (h) confirm exit checks reference actual evaluator outputs rather than placeholders.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Workflow Patterns Coverage — Generator–Critic (review/fact-check)

System role: Judge generator→reviewer design.

Example Checks: (a) reviewer reads generator’s state/output; (b) review gates release or triggers revision; (c) factuality/grounding checks; (d) clear pass/fail criteria; (e) no bypass of reviewer step; (f) confirm reviewer agents import/read generator output keys explicitly; (g) ensure critic responses can block final emission through return codes/state flags; (h) verify repair agents consume critic artifacts when defined.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Workflow Patterns Coverage — Human-in-the-loop checkpoints

System role: Judge human approval/instruction checkpoints.

Example Checks: (a) blocking/non-blocking human step defined; (b) timeouts and defaults; (c) audit trail of decisions; (d) safe gating before risky actions; (e) resume logic after human input; (f) inspect state keys that capture human approval timestamps/IDs; (g) confirm there is a code path to abort or timeout when human input never arrives; (h) ensure documentation references the same UI/event hooks wired in code.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Shared State & Data Passing (state keys, schemas, immutability/overwrites, provenance)

System role: Judge state hygiene and data contracts for state passing.

Example Checks: (a) consistent key naming; (b) typed/validated payloads; (c) write-once vs overwrite rules; (d) provenance (who/when wrote keys); (e) collision avoidance in parallel paths; (f) statically verify no two agents overwrite the same state key without merge logic; (g) ensure complex payloads have documented schemas or dataclasses; (h) check that read/write helpers encapsulate state mutations to avoid drift.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Inter-Agent Communication (A2A/delegation calls, message structure, handoff completeness)

System role: Judge handoff fidelity and message contracts.

Example Checks: (a) lossless transfer of identifiers/context; (b) minimal relevant payloads (no prompt bloat/PII leakage); (c) explicit delegation triggers; (d) schema adherence; (e) idempotent replays of messages; (f) inspect delegation payload schemas for required identifiers/context handles; (g) ensure sensitive fields are stripped or masked before forwarding; (h) verify message handlers are designed to be idempotent for replays.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Prompt & Policy Design (agent-specific prompts, tuning/refinement, tool docs, format contracts, few-shot)

System role: Judge prompt engineering and policy alignment.

Example Checks: (a) prompts tailored to role; (b) tool usage instructions/examples; (c) output format contracts; (d) documented prompt iterations; (e) embedded safety/policy where needed; (f) few-shot consistency with domain; (g) ensure prompt files/version tags in repo reflect the instructions under review; (h) confirm prompts reference tool docs that actually exist in the codebase; (i) verify few-shot examples cite repository-specific data rather than generic placeholders.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Determinism & Idempotency (idempotent tools, replay safety, duplicate suppression)

System role: Judge determinism and safe replays.

Example Checks: (a) idempotency keys/tokens for external actions; (b) duplicate suppression on retries; (c) deterministic merges on gather; (d) no side-effects without guards; (e) stable ordering when non-determinism is inherent; (f) check for deterministic ordering (sorted lists, hashed keys) in merge code; (g) verify `idempotency_key` or replay guards are persisted in state; (h) ensure gather/merge helpers are pure functions without side-effects.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Error Handling & Robustness (try/except, typed error results, retries/backoff, circuit breakers, timeouts)

System role: Judge fault handling patterns.

Example Checks: (a) try/except around tool/LLM calls; (b) structured error payloads; (c) exponential backoff; (d) circuit breakers; (e) timeouts; (f) input validation before calls; (g) coverage in tests/evals for failures; (h) ensure structured error metadata is logged for every caught exception; (i) confirm fallback states/results are persisted for post-mortems.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Graceful Degradation & Fallbacks (partial results, alternate paths, user notification)

System role: Judge degradation plans and user experience under failure.

Example Checks: (a) partial but accurate responses; (b) backup agents/models; (c) cached responses; (d) clear user messaging; (e) feature kill-switch/feature flags; (f) preservation of traceability in degraded mode; (g) verify alternate agent/model definitions are present and wired for failover; (h) ensure degraded output schemas are documented alongside code; (i) align feature-flag toggles in code with documentation tables.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Observability & Tracing (structured logs, event traces, tool call audits, correlation IDs)

System role: Judge telemetry and traceability.

Example Checks: (a) structured logs for each agent step; (b) end-to-end correlation IDs; (c) tool call audit trail (inputs/outputs/latency); (d) PII-safe logging; (e) trace spans for orchestration and parallelism; (f) alerting hooks for anomalies; (g) confirm logging/telemetry middleware is instantiated in `agents/*`; (h) ensure correlation IDs are passed through when parent delegates to children; (i) cross-check documentation claims about log sinks with actual config objects.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Evaluation Hooks & Testability (ADK eval cases, trajectory checks, rubric/LLM judges, regression tests/pytest)

System role: Judge evaluation completeness and regression protection.

Example Checks: (a) ADK eval cases per scenario; (b) tool-trajectory checks; (c) rubric/LLM-judge gates; (d) pytest/CI regression; (e) recorded traces for failures; (f) golden outputs and tolerances; (g) confirm `tests/` or `evals/` files map to each agent capability described; (h) verify evaluation configs reference the current schema/state keys; (i) ensure CI scripts or `pytest` commands in docs exist in the repo.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Performance Engineering (concurrency via ParallelAgent/async, batching, caching, n+1 avoidance)

System role: Judge latency/throughput engineering.

Example Checks: (a) ParallelAgent for independent tasks; (b) async tools for I/O; (c) request batching; (d) caching/memoization; (e) elimination of n+1 call patterns; (f) profiling evidence and KPIs tracked; (g) statically check for concurrency primitives (`ParallelAgent`, `async def`) where independence exists; (h) confirm caching modules define TTL/size limits; (i) ensure doc KPIs (latency, throughput) align with instrumentation fields.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Cost Controls (token budgets, call caps, caching, early-exit heuristics)

System role: Judge token/call cost discipline.

Example Checks: (a) per-step token budgets; (b) call caps and guards; (c) caching and reuse of results; (d) early-exit/gating heuristics; (e) right-sized models; (f) cost logging and reports; (g) verify constants such as `max_tokens`/`max_cost` are enforced in code; (h) ensure early-exit conditions trigger when budgets are exceeded; (i) confirm token/cost logging fields feed into telemetry modules.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Scalability & Deployment (stateless sessions, externalized memory, containerization, autoscaling)

System role: Judge scale readiness and deployment architecture.

Example Checks: (a) stateless service boundaries; (b) external state/memory where needed; (c) containerized runtime; (d) autoscaling rules; (e) absence of single bottleneck agents; (f) readiness/liveness probes; (g) confirm deployment artifacts (Dockerfile, Cloud configs) reference the same agents; (h) ensure code avoids module-level singletons that block horizontal scale; (i) verify documentation’s scaling plan maps to actual health-check implementations.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Configuration & Versioning (RunConfig/ResumabilityConfig, model/param pinning, prompt/version control)

System role: Judge configuration hygiene and version control.

Example Checks: (a) `RunConfig` with sensible limits; (b) `ResumabilityConfig` for long flows; (c) model/param pinning; (d) prompt versioning and change logs; (e) environment-specific configs; (f) reproducibility; (g) confirm config files/env templates are versioned alongside code; (h) ensure prompt/config changes are tagged or noted in change logs; (i) verify environment-specific overrides (dev/prod) exist where claimed.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Security & Access Control (secrets management, least privilege, sandboxed execution, authN/authZ)

System role: Judge security posture.

Example Checks: (a) secrets in env/secret manager (not code); (b) scoped credentials per agent/tool; (c) sandboxed code execution; (d) authenticated user context; (e) authorization checks before actions; (f) dependency vulnerability scanning; (g) inspect code for environment-variable access instead of hard-coded secrets; (h) ensure documented scope restrictions align with tool credential usage; (i) verify tool wrappers perform user/tenant authorization checks before acting.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Safety & Compliance (content filters, hallucination checks, PII handling, audit trails)

System role: Judge content and data safety.

Example Checks: (a) safety filters and policy prompts; (b) grounding/hallucination checks; (c) PII minimization and masking; (d) audit trails; (e) red-team prompts; (f) compliance logging and retention policies; (g) confirm redaction or masking helpers are invoked before persisting PII; (h) ensure logs omit sensitive fields per policy; (i) verify compliance matrices in docs map to concrete modules or callbacks.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Data Contracts & Schemas (typed inputs/outputs, strict JSON, schema evolution)

System role: Judge data contract rigor.

Example Checks: (a) Pydantic/dataclasses for types; (b) strict JSON outputs; (c) validation at boundaries; (d) versioned schemas and migrations; (e) backward compatibility; (f) clear error messages on validation failures; (g) static-check for schema validator tests alongside the definitions; (h) ensure version identifiers are stored with each schema; (i) verify conversion/migration utilities are referenced wherever schema versions change.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Dependencies & Tool Quality (library pinning, retries, rate limits, backoff, resilience patterns)

System role: Judge dependency and tool resilience.

Example Checks: (a) pinned versions and lockfiles; (b) retries with backoff; (c) rate-limit handling; (d) timeouts; (e) graceful degradation of tool errors; (f) health checks for external services; (g) inspect `requirements.txt`/lockfiles to ensure pinned versions cover every tool import; (h) verify tool wrappers implement retry/backoff decorators; (i) confirm monitoring hooks raise alarms on repeated tool failures.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Resource & Rate Management (quotas, pooling, exponential backoff, jitter)

System role: Judge resource control mechanisms.

Example Checks: (a) API quotas honored with guards; (b) connection/thread pools; (c) exponential backoff + jitter; (d) queueing or shedding under load; (e) fair-use across agents/sessions; (f) observability of rate events; (g) verify a centralized rate limiter or quota constant is referenced by all agents; (h) ensure pooling configs (HTTP, DB) are defined in code; (i) align documentation about quotas with the actual numeric limits in code.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - UX & Product Integration (streaming behavior, user prompts for ambiguity, interruption/undo)

System role: Judge UX integration of agent outputs.

Example Checks: (a) streaming where helpful; (b) proactive clarification prompts; (c) pause/interrupt/undo affordances; (d) confirmation before risky actions; (e) consistent final formatting and error messaging; (f) accessibility considerations; (g) confirm formatting/templating helpers exist for UI responses and are referenced; (h) ensure prompts account for real user flows captured in docs; (i) check for undo/confirmation state keys wired to front-end triggers.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Documentation & Runbooks (agent inventories, sequence diagrams, failure playbooks, SLOs)

System role: Judge operational documentation.

Example Checks: (a) agent inventory with roles and dependencies; (b) sequence/flow diagrams; (c) failure playbooks and on-call runbooks; (d) SLOs/error budgets; (e) dependency maps; (f) change management notes and ADRs; (g) ensure doc inventories list every agent present under `agents/*`; (h) confirm diagrams/assets in docs are updated alongside code changes; (i) verify runbooks reference actual scripts/commands stored in the repo.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Readiness Gates (pre-prod checks, canary runs, kill-switches, rollback plans)

System role: Judge release readiness controls.

Example Checks: (a) pre-prod eval bar and signoff; (b) canary and monitoring plan; (c) kill-switch/feature flags; (d) rollback procedure with tested playbooks; (e) incident response path and paging; (f) post-launch guardrails; (g) verify kill-switch/feature-flag code paths exist where documentation promises them; (h) ensure rollback scripts/configs referenced are present in the repo; (i) cross-check readiness checklists against actual eval/test configs committed.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:

-------------------------------------------
# Topic - Use of Readymade packages, framework, tools

System role: Judge the use of available python packages, Google ADK framework, built-in tools, MCP tools, google Cloud tools, Third party tools, OpenAI tools. You goal is increase the re-use of what is available before writing new code.

Example Checks: (a) Identify python code blocks or architecture which could be replaced by already built-in or available python packages, Google ADK framework, built-in tools, MCP tools, google Cloud tools, Third party tools, OpenAI tools.

Output Validation: Provide critical findings, if any, in below format

Output Format:
Finding 1:

Finding 2:
