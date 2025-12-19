# Workflow for Generating Multi-Agent Plans
Plan before you code. Follow the instructions below to step by step generate Plan that works.

1. **Preparation**
   - Re-read `AGENTS.md`, `llms-full.txt`, and any linked guidance they cite.
   - Confirm no source code changes are required for this workflow.
   - Target architecture must reuse existing ADK components (e.g.,
     `google.adk.agents.Agent`, `AgentTool`, `google_search`) and separate
     search, drafting, and review agents coordinated by a root agent.

2. **Initial Plan — `docs/ai_docs/google-adk_PLAN.md`**
   - Follow every step in `docs/instructions/instruction_for_ADK_plan.md`.
   - Save the resulting architecture plan to `docs/ai_docs/google-adk_PLAN.md`
     (overwrite if it already exists).
   - Do not create or modify any other files in this step.

3. **Critic Review — `docs/ai_docs/judge_PLAN.md`**
   - Use the proposal in `docs/ai_docs/google-adk_PLAN.md` as the sole input.
   - Apply the evaluation rubric from
     `docs/instructions/instructions_to_judge_adk_PLAN.md`.
   - Save the critique findings to `docs/ai_docs/judge_PLAN.md`.
   (overwrite if it already exists).

4. **Master Plan — `docs/ai_docs/MASTER_PLAN.md`**
   - Revisit every finding noted in `docs/ai_docs/judge_PLAN.md`.
   - Incorporate resolutions or mitigations for MOST CRITICAL issue for multi agent architecture, if any.
   - Incorporate as much information as necessary for effective coding using the plan
     as a guide.
   - Author the final implementation roadmap in
     `docs/ai_docs/MASTER_PLAN.md`, explicitly noting how critic feedback was
     addressed.

5. **Sign-off**
   - After writing `docs/ai_docs/MASTER_PLAN.md`, ask the user to review and
     approve it before any implementation work begins.

6. **Restrictions**
   - Do not modify application code during this documentation workflow.
   - Maintain the step order above; do not skip directly to the master plan.
