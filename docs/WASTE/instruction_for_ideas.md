**Role & Objective**  
You are expert in Google Agent Development Kit (ADK), python and AI agent and Agentic AI.
Act as an expert evaluator for **Multi-AI agent system architectures**, suggest top 10 most impactful ideas for architecture improvement with reasons why?

---

## Checklist (do these, conceptually)
- **Hard rule:** **read and honor `llms-full.txt`, `AGENTS.md` **. Do **not** modify it. Use the knowledge available in it for improve your skill.
- **Hard rule:** **read and understand code files in `refs/*` folder **. Do **not** modify it. Use the knowledge of coding patters and best practices available in it to improve your ability to suggest improvement in multiagent architectures. Do not suggest ideas for the code files in `refs/*` folder
- **Hard rule:** **read and understand the current architecture of the AI Agents in the file `docs/google-adk.md`, if present**. **Do **not** modify it.**
- **Hard rule:** **read and understand the current architecture of the AI Agents in the code files in the folder `agents/*`**. 
- **Hard rule:** **The multi agent architecture for your evaluation is solely based on the content of `docs/google-adk.md`, if present, and code files in the folder `agents/*`, if present,. Do not review any other code files outside of the `agents/*` folder, if present,.**

- **Hard rule:** **read and understand the evaluation of current architecture of the AI Agents the document `docs/judge_architecture.md`**. **Do **not** modify it. Strictly based on the content of this evaluation, suggest ideas for improvement. The reasoning for each improvement ideas should be based on evaluation. Do not hallucinate improvements.**
- **Hard rule:** **consider both True and False criterions in `docs/judge_architecture.md`** to decide ideas for improvement.


## Output
- Provide the Output in **only one file**: `docs/Improvement_ideas.md`

## Output format example:
-----------------------------------------
**S. No.** 1

**Improvement Idea**:
Add a reviewer/critic agent that scores `draft_essay` before finalizing.

**Reason why**:
Criteria #50–#53 are False because only the generator exists; inserting an `EssayReviewer` LlmAgent that reads the existing `draft_essay` session key and writes `review_report` lets EssayComposer revise iteratively without disturbing the proven upstream outline/research steps (criteria #3–#9).

**Additional Note, if any**
Mirror the generator/critic pattern from ADK reference agents by reusing `AgentTool` or defining the reviewer as a sequential sub-agent stage.

-----------------------------------------
**S. No.** 2

**Improvement Idea**:
Enable session persistence and resumability for long essays

**Reason why**:
Criteria #88, #118, and #122 are unmet since InMemory defaults are implied; configuring `VertexAiSessionService` (or another ADK session backend) plus `ResumabilityConfig` lets EssayWriterPipeline recover mid-run without replaying WebResearcher work, which becomes critical as essay length grows.

**Additional Note, if any**
Reuse ADK session services and resumability APIs—no bespoke persistence layer.
-----------------------------------------