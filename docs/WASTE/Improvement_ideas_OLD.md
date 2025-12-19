-----------------------------------------
**S. No.** 1

**Improvement Idea**:
Add a resilience layer (retries + fallback agents) so each stage degrades gracefully instead of halting the whole SequentialAgent run.

**Reason why**:
Criteria #14, #66-67, and #98-102 are False because the current spec never defines retries, fallback agents, or graceful error handling; yet criteria #1-12 already confirm the three-step flow is sound, so wrapping OutlineGenerator/WebResearcher/EssayComposer with shared retry policies preserves the proven structure while addressing the biggest reliability gaps called out in documentation/judge_architecture.md:14-102.

**Additional Note, if any**
Reuse ADK's existing `before_agent_callback`/`after_agent_callback` hooks (as seen in refs/adk-samples/travel_concierge) plus `google.adk.runners.Runner` error handlers to record structured failures and trigger backup agents without inventing new orchestration.
-----------------------------------------
**S. No.** 2

**Improvement Idea**:
Upgrade EssayWriterPipeline from a strictly static SequentialAgent to an adaptive coordinator that can re-plan (e.g., via `google.adk.planners.BuiltInPlanner`) when sub-agent outputs fail quality thresholds.

**Reason why**:
Criteria #15 and #21 are False because the architecture never allows mid-run adjustments or explains how decomposition stays efficient as complexity grows; an adaptive planner that inspects session keys (topic/outline/sources) at each hop would keep the validated three-phase order (#5 True) but insert health checks that can repeat or skip steps when downstream dependencies are unmet.

**Additional Note, if any**
Leverage existing ADK planner APIs instead of crafting a bespoke scheduler—wrap the current sub-agents as planner steps so we can toggle between sequential and reactive modes within the same Runner configuration.
-----------------------------------------
**S. No.** 3

**Improvement Idea**:
Insert an explicit Clarifier/ConflictResolver agent that asks the user for disambiguation and reconciles contradictory research outputs before composition.

**Reason why**:
Criteria #16 and #17 are False: there is no mechanism to resolve conflicting agent outputs or to re-query the user when the topic is underspecified. Because the evaluation already marks context transfer (#11 True), adding a light-weight clarifier that reads `topic`/`outline` and updates `session.state['clarifications']` would eliminate the flagged ambiguity gap without rewriting existing agents.

**Additional Note, if any**
Implement this as an `AgentTool` so EssayWriterPipeline can invoke it on demand—mirrors how refs/adk-samples use agent-as-tool patterns for specialized negotiation without inflating the main sub-agent list.
-----------------------------------------
**S. No.** 4

**Improvement Idea**:
Add an EssayReviewer critic agent after EssayComposer to score `draft_essay`, request revisions, or flag blocking issues.

**Reason why**:
Criteria #50-53 are all False because no generator/critic loop exists; the evaluation explicitly notes the pipeline stops after composition. A reviewer that reads the existing `draft_essay` key and writes `review_report` would satisfy those unmet criteria while keeping the upstream Outline/WebResearch steps (criteria #1-9 True) untouched.

**Additional Note, if any**
Follow the generator/critic pattern from ADK samples by wrapping EssayReviewer as `AgentTool(essay_reviewer)` so EssayWriterPipeline can loop until the critic approves.
-----------------------------------------
**S. No.** 5

**Improvement Idea**:
Define human-in-the-loop checkpoints for sensitive topics, routed through a HumanApproval tool that can pause and resume the run.

**Reason why**:
Criteria #54-58 and #187-188 are False because there is no documented human approval or escalation path even when the subject matter is risky. Given the evaluation already praises the clean handoffs (#10-12 True), inserting an approval gate before WebResearch or EssayComposer will add governance without disturbing those validated transfers.

**Additional Note, if any**
Implement approvals with an ADK `FunctionTool` that writes to `session.state['approval']` and resumes once an operator responds, copying the pause/resume hooks demonstrated in refs/a2a-samples for compliance workflows.
-----------------------------------------
**S. No.** 6

**Improvement Idea**:
Establish concrete latency/cost budgets plus structured logging via callbacks so performance and spend stay within targets.

**Reason why**:
Criteria #18-20, #69, #77, #85, and #117 are False because no RunConfig, model parameter tuning, or observability exists. Since the decomposition is already efficient (criteria #1-6 True), setting per-agent temperature/max token values, enabling `before_model_callback` metrics across all agents (not just EssayComposer), and logging token/latency budgets will close those gaps without new functionality.

**Additional Note, if any**
Reuse `google.adk.runners.RunConfig` to cap calls, and extend the existing callbacks pattern (already used for WebResearch/EssayComposer) to emit cost telemetry to ADK's session events store.
-----------------------------------------
**S. No.** 7

**Improvement Idea**:
Harden tool usage with validation, docstrings, caching, and timeouts around the MCP web_search/url_reader integrations.

**Reason why**:
Criteria #65, #78, #82, #83, #100, and #177 are False because the spec never documents parameter validation, tool docstrings, memoization, or timeouts. Strengthening the only tool-using agent (WebResearcher) with ADK's tool schemas keeps criteria #9 (tool identification True) intact while addressing every tool-quality gap flagged by the evaluation.

**Additional Note, if any**
Wrap the MCP calls in reusable `google.adk.tools.FunctionTool` adapters so we can add schema validation, `max_duration`, and memoized responses without rewriting the MCP server bindings referenced in llms-full.txt.
-----------------------------------------
**S. No.** 8

**Improvement Idea**:
Persist session state outside memory and enable resumability so long essays survive restarts or manual pauses.

**Reason why**:
Criteria #88, #118, and #122 are False because state persistence and ResumabilityConfig are never mentioned; this clashes with the multi-step workflow that already depends on `outline`, `sources`, and `draft_essay`. Externalizing state via `VertexAiSessionService` (or another ADK session backend) keeps those validated keys while ensuring interrupted runs can resume.

**Additional Note, if any**
Adopt ADK's built-in session services plus `ResumabilityConfig(checkpoint_keys=["outline","sources","draft_essay"])` so no bespoke persistence layer is required.
-----------------------------------------
**S. No.** 9

**Improvement Idea**:
Add security and safety guardrails covering secrets, PII, moderation, jailbreak, and hallucination controls.

**Reason why**:
Criteria #91-97 and #197-200 are all False because the architecture never discusses secret handling, sanitization, or safety guardrails. Since the evaluation already confirms tools are known (#9 True) and callbacks exist (#189 True), layering ADK guardrail policies and ToolContext checks over those same touchpoints directly addresses every flagged risk area.

**Additional Note, if any**
Configure ADK guardrail policies (PII, moderation, jailbreak, hallucination) and load credentials from `.env` so we reuse the documented secret-management pattern instead of hand-rolled filters.
-----------------------------------------
**S. No.** 10

**Improvement Idea**:
Define artifact outputs and structured schemas for the final essay (and its references) so downstream tooling can consume results deterministically.

**Reason why**:
Criteria #154-156 and #196 are False—the pipeline emits only free-form markdown, so no artifact schema or JSON/Pydantic contract exists. Because earlier criteria already validate the session keys (#11 True), promoting `draft_essay` and `sources` into typed artifacts (e.g., `EssayArtifact` + `SourcesArtifact`) will satisfy the missing criteria without changing agent responsibilities.

**Additional Note, if any**
Reuse ADK's `artifacts.InMemoryArtifactService` interfaces to store structured outputs and mirror the schema patterns published under refs/adk-docs.
