# AGENTS.md

> **If you read this file, prepend all replies with:** `Read the AGENTS.md`

## What this file is - 

Agent-facing instructions for working in this repo (different from the human README).
**Stack:** Python for code, **Google Agent Development Kit (ADK)** for AI agent coding framework, **Gemini** for LLM calls.

**Hard rule:** Treat AGENTS.md as a Primary Constraint: Treat all "Hard rules" in AGENTS.md as primary, non-negotiable constraints that shape plan, not as secondary checks.
**Hard rule:** Before you make plans for code execution, **read and honor `llms-full.txt`**. Do **not** modify it. Use the knowledge available in it for improve your plan.
**Hard rule:** Always prefer python and Google ADK framework APIs (packages/classes/functions) over writing new ones. **Look what is available in Google ADK in the `llms-full.txt`**. Do **not** modify it.
**Hard rule:** Always reuse python packages/classes/functions/tools/ MCP tools already available. Do not create unless really necessary. Write new code as minimum as possible while following coding best practices.
**Hard rule:** Prioritize Framework Reuse: Before you propose creating any new class, function, or component, absolute first step will be to thoroughly search the existing codebase and documentation (especially llms-full.txt) for a pre-existing equivalent within the project's chosen framework (in this case, Google ADK).
**Hard rule:** Explicitly State Reuse in Plans: Plans should explicitly mention the components you intend to reuse. This makes adherence to the project's rules transparent from the start.
**Hard rule:** code in the folder `refs/`** is read-only. Don’t import at runtime; adapt coding patterns only from them. Do not compile them. Do not change the code in them.
**Hard rule:** **read and understand the current architecture of the AI Agents in the file `documentation/google-adk.md`, if present**. **Do not modify it.**
**Hard rule:** **read and understand the current architecture of the AI Agents in the code files in the src folder `src/*` **, if present**.



**Hard rule:** How to Handle Conflicts: User Instructions vs. AGENTS.md Rules
This section clarifies how the agent should prioritize instructions when the user's request seems to conflict with the rules defined in this file.

Scenario:
The user provides a prompt that describes a feature or component conceptually. For example, the prompt might say, "Implement a conceptual Runner that wires user input to the agent," which might seem like an instruction to build a new Runner class from scratch. This could conflict with a "Hard rule:" in this document that states, "Always prefer reusing existing framework APIs (like the ADK Runner) over creating new ones."

Resolution Protocol (Instructions for the Agent):

In this scenario, you must follow this protocol:

Prioritize the User's Goal, Not Their Implied Method. Your primary objective is to fulfill the user's high-level goal (e.g., "create a runnable demo"). Treat conceptual descriptions in the user's prompt as a definition of the requirements for the final outcome, not as a strict command to build components from the ground up.

AGENTS.md Dictates the Implementation. You must adhere to the "Hard rules" in this document for the how. If a rule mandates reusing an existing framework component, you must use that component to achieve the user's goal.

Explicit User Commands Override AGENTS.md. You should only override a "Hard rule" if the user gives a direct, explicit, and unambiguous command to do so (e.g., "You must write a new Runner class from scratch and you are forbidden from using the ADK one."). If there is any ambiguity, the rules in AGENTS.md take precedence for the implementation method.

State Your Plan Clearly. Your initial plan must reflect this protocol. It should clearly state the user's goal and then describe how you will achieve it by reusing the components mandated by this document. For example: "To achieve the user's goal of a runnable demo, I will use the existing google.adk.runners.Runner as instructed by AGENTS.md."


---

## Quick Start (TL;DR)

1. **Read policy files**

   * Apply **all** rules in `llms-full.txt` (models, params, safety, rate limits) **before every call**.

2. **Create env + install deps**

   * **Windows (PowerShell)**

     ```powershell
     python -m venv .venv
     . .\.venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```
   * **macOS / Linux**

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install -r requirements.txt
     ```
   * **Cursor/VS Code tip:** Ctrl+Shift+P → **Python: Select Interpreter** → pick the `.venv` interpreter.

3. **Create `.env` (first run)**

   * In the repo **root**, add a file named `.env` with:

     ```bash
     GOOGLE_GENAI_USE_VERTEXAI=FALSE
     GOOGLE_API_KEY=???
     ```
   * Then complete **Setting Up API Keys** below and replace `???` with your real key.

4. **(Optional) Start ADK dev UI / API**

   ```bash
   export SSL_CERT_FILE=$(python -m certifi)  # one-time for voice/video certs
   adk web            # opens http://localhost:8000
   # or:
   adk api_server
   # Windows reload workaround if needed:
   # adk web --no-reload
   ```

5. **Format, lint, test**

   ```bash
   ./autoformat.sh
   pytest tests/unittests -q
   ```

6. **Make a small, reviewable change** (see Commit & PR).

---

## Setting Up API Keys

Use the `.env` file present in the root folder for `GOOGLE_API_KEY` keys.

If the `.env` file is **not present** or `GOOGLE_API_KEY` is missing, ask user to follow these steps:

1. Create an account in Google Cloud: [https://cloud.google.com/?hl=en](https://cloud.google.com/?hl=en)
2. Create a **new project**.
3. Visit **AI Studio**: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
4. **Create an API key**.
5. **Assign the key** to your project.
6. **Connect to a billing account**.
7. Open the `.env` file in the repo root and replace the placeholder with your key:

   ```env
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_api_key_here
   ```

> Keep the `.env` file **out of version control** (see `.gitignore`). Never share keys in issues or PRs.

---

## Setup Details

### Requirements file

Keep dependencies in `requirements.txt` and install with `pip install -r requirements.txt`.

### ADK-aligned project layout (best practice)

Use **one folder per agent**; the folder name is the src/<agent_name> used by local APIs and the dev UI. Keep a strict, deployable layout:

```
root/
	src/					 # Keep source code for agent within this folder or its subfolders
	  <agent_name>/			 # Make folder with Agent name
		__init__.py          # from . import agent
		agent.py             # defines: root_agent = Agent(...)
		requirements.txt     # agent-specific deps only (optional; root already has this file for global installations)
```

**Rules that must hold for deploy/ops ergonomics**

* File **must** be named `agent.py`.
* The exported top-level variable **must** be named `root_agent`.
* Add `__init__.py` and include `from . import agent` so module discovery works.
* Keep folder names short, lowercase, hyphen/underscore free where possible (URLs & CLI paths are derived from them).

### Autoformat / Lint / Type check (pick what this repo uses)

```bash
./autoformat.sh
ruff check src         # or: pylint src
mypy src               # if type checking is enabled
```

### Notes

* For streaming/live tests: store transcriptions as **Events** and audio as **artifacts** referenced by Events.
* Use **Artifacts** (not session state) for any binaries (files/audio/images).
* Streaming tests typically live under `tests/unittests/streaming/` in ADK examples.

---

## How Agents Should Work Here

### Model & Call Policy

### ADK Usage Policy

* Treat ADK as a **library**. Do **not** modify ADK source or contribute upstream from this repo.
* Use `adk web` / `adk api_server` for **local/manual testing only** (not a production dependency).

## Disallowed Patterns
- Declaring new agent base classes if an ADK equivalent exists.
- Copying utilities that exist in ADK tools.

## When adding code
- Search the codebase and ADK docs first. Resuse ADK packages/classes/functions.
- If you believe no ADK API exists, add a comment explaining the search terms and links checked.
- Do not create what is already present

## Acceptance Criteria for any PR
- Linter passes “ADKReuseRule”.
- PR description includes “ADK search summary”.

## In the Planning steps
- Write which ADK packages/classes/functions will you use.

### ADK agent layout & naming (best practices)

* **Foldering:** one folder per agent under `src/`. Top-level multi-agent apps can keep a root `src/<root_agent>/agent.py` and nest sub-agents in sibling folders (e.g., `src/search_agent/`, `src/rag_agent/`).
* **File & symbol names (strict):** `agent.py` with a top-level `root_agent`. Avoid renaming; scripts and deploy flows assume these.
* **Agent names:** valid Python identifiers, unique across the tree, and never `"user"`. Use descriptive names that reflect the role; names appear in traces and delegation.

### Tool design (best practices)

* Keep tools **small, focused functions** with minimal, primitive parameters.
* Use meaningful function names & docstrings—tools are surfaced to the model; clarity improves selection.
* Prefer `async def` tools when they call I/O; ADK can parallelize eligible tool calls to reduce latency.
* Return structured results (e.g., dicts with `status`, `data`, `error`) that are easy to reason about and test.

### Session, state & memory hygiene

* Use `session.state` for simple, serializable key/values (e.g., `booking_step`, `current_doc_id`).
* Scope state with clear prefixes or conventions, e.g., transient keys (`temp:*`) for per-invocation scratch.
* **Do not** shove large blobs into state; put binaries in **Artifacts** and reference them from Events or state by ID.

### Prompts & agent config quality

* Write precise `instruction` prompts; include a descriptive `name`/`description`—these help multi-agent delegation.
* For complex systems, consider external **Agent Config** files to declare sub-agents, tools, and wiring. Treat them as source of truth when they exist.
* Use `RunConfig` to cap cost/latency (e.g., `max_llm_calls`), enable streaming, and set tracing verbosity for dev vs. CI.

### Observability & operations

* Use **structured logging**. Default to INFO for normal runs; bump to DEBUG only when troubleshooting.
* Inspect **traces** in the Dev UI to validate reasoning steps, tool calls, and state transitions.
* **Deployment sanity checks:** the `src/<agent>/agent.py` + `root_agent` + `__init__.py` pattern must be intact for packaging and service discovery (e.g., Cloud Run / internal runners).

### Testing & local dev ergonomics

* Use `adk api_server` or `adk web` to iterate locally; paths are derived from the **agent folder name** (keep it clean).
* Add early **evals** (JSON eval sets) that check not just the final answer but also **trajectory/tool use**.
* Keep tests hermetic; mock external I/O where possible. Store golden responses for regressions when appropriate.

### Python Code Style (summary)

* Follow Google/PEP 8 style:

  * 2-space indent (unless repo specifies otherwise), ~80–100 char lines.
  * `snake_case` for functions/vars, `CamelCase` for classes.
  * Public APIs have docstrings; imports are organized/sorted.
  * Catch **specific** exceptions; avoid bare `Exception`.
* Run `./autoformat.sh` before committing.

### Documentation Workflow


---

## Common Commands (copy–paste)

**Type check**

```bash
mypy src
```

**Format**

```bash
./autoformat.sh
```

**Lint**

```bash
ruff check src
# or
pylint src
```

**Unit tests (fast)**

```bash
pytest tests/unittests -q
```

**Full test suite (CI parity)**

```bash
pytest
```

**Evaluate sample (if applicable)**

```bash
adk eval samples_for_testing/hello_world   samples_for_testing/hello_world/hello_world_eval_set_001.evalset.json
```

**Local dev UI / API**

```bash
export SSL_CERT_FILE=$(python -m certifi)
adk web            # or: adk api_server
```

---

## Project Map (minimal)

* `src/` — **agents live here** (one folder per agent: `src/<agent_name>/agent.py` with `root_agent`)
* `src/` — Python modules (safe to modify per task)
* `scripts/` — automation helpers (keep idempotent)
* `documentation/` — 
* `tests/` — unit/integration/eval tests (`tests/unittests/`, `tests/evals/`, `tests/unittests/streaming/` if used)
* `infra/` — infrastructure (requires human review)

---

## Commit & PR Guidelines

* Use **Conventional Commits**; add `#non-breaking` or `#breaking` flags.
* Keep PRs small/scoped; include repro steps and tests when relevant.
* Ensure format/lint/tests pass locally before opening a PR.

---

## When to Ask for Help / Stop

Stop and request human input when:

* Dependencies or local UI fail to start **after two attempts** (including Windows `--no-reload`).
* Tests repeatedly fail or exceed expected runtime.
* Required credentials/API keys are missing.
* Proceeding would require modifying ADK’s source or repo structure.

---

## Non-Goals

* Do **not** modify or contribute to **Google ADK** upstream from this repo.

---

## References

* **`llms-full.txt`** — must read before every call (models/params/safety/testing).
* **`Doc_Spec.md`** — docs structure, naming, lifecycle, templates.
* **`ADK_AGENTS.md`** — setup helper, code style, testing, commits, streaming notes.
* **ADK repo:** [https://github.com/google/adk-python](https://github.com/google/adk-python)

---

### Appendix: ADK as a Dependency (FYI)

ADK is model-agnostic and Python-first. You can compose single/multi-agent systems and test in the built-in dev UI:

```bash
export SSL_CERT_FILE=$(python -m certifi)
adk web   # or: adk api_server
```

**ADK agent structure recap (copy/paste)**

```
src/
  google_search_agent/
    __init__.py      # from . import agent
    agent.py         # defines: root_agent = Agent(...)
    requirements.txt
```

> Keep this file explicit and concise. Update it when commands or docs move. If a subfolder needs special rules, add a scoped `AGENTS.md` there and link it here.

# Multi-Agent Systems in ADK

This example demonstrates how to create a multi-agent system in ADK, where specialized agents collaborate to handle complex tasks, each focusing on their area of expertise.

## What is a Multi-Agent System?

A Multi-Agent System is an advanced pattern in the Agent Development Kit (ADK) that allows multiple specialized agents to work together to handle complex tasks. Each agent can focus on a specific domain or functionality, and they can collaborate through delegation and communication to solve problems that would be difficult for a single agent.

## Project Structure Requirements

For multi-agent systems to work properly with ADK, your project must follow a specific structure:

```
parent_folder/
├── root_agent_folder/           # Main agent package (e.g., "manager")
│   ├── __init__.py              # Must import agent.py
│   ├── agent.py                 # Must define root_agent
│   ├── .env                     # Environment variables
│   └── sub_agents/              # Directory for all sub-agents
│       ├── __init__.py          # Empty or imports sub-agents
│       ├── agent_1_folder/      # Sub-agent package
│       │   ├── __init__.py      # Must import agent.py
│       │   └── agent.py         # Must define an agent variable
│       ├── agent_2_folder/
│       │   ├── __init__.py
│       │   └── agent.py
│       └── ...
```

### Essential Structure Components:

1. **Root Agent Package**
   - Must have the standard agent structure (like in the basic agent example)
   - The `agent.py` file must define a `root_agent` variable

2. **Sub-agents Directory**
   - Typically organized as a directory called `sub_agents` inside the root agent folder
   - Each sub-agent should be in its own directory following the same structure as regular agents

3. **Importing Sub-agents**
   - Root agent must import sub-agents to use them:
   ```python
   from .sub_agents.funny_nerd.agent import funny_nerd
   from .sub_agents.stock_analyst.agent import stock_analyst
   ```

4. **Command Location**
   - Always run `adk web` from the parent directory (`6-multi-agent`), not from inside any agent directory

This structure ensures that ADK can discover and correctly load all agents in the hierarchy.

## Multi-Agent Architecture Options

ADK offers two primary approaches to building multi-agent systems:

### 1. Sub-Agent Delegation Model

Using the `sub_agents` parameter, the root agent can fully delegate tasks to specialized agents:

```python
root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="You are a manager agent that delegates tasks to specialized agents...",
    sub_agents=[stock_analyst, funny_nerd],
)
```

**Characteristics:**
- Complete delegation - sub-agent takes over the entire response
- The sub-agent decision is final and takes control of the conversation
- Root agent acts as a "router" determining which specialist should handle the query

### 2. Agent-as-a-Tool Model

Using the `AgentTool` wrapper, agents can be used as tools by other agents:

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="You are a manager agent that uses specialized agents as tools...",
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
```

**Characteristics:**
- Sub-agent returns results to the root agent
- Root agent maintains control and can incorporate the sub-agent's response into its own
- Multiple tool calls can be made to different agent tools in a single response
- Gives the root agent more flexibility in how it uses the results

## Limitations When Using Multi-Agents

### Sub-agent Restrictions

**Built-in tools cannot be used within a sub-agent.**

For example, this approach using built-in tools within sub-agents is **not** currently supported:

```python
search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="You're a specialist in Google Search",
    tools=[google_search],  # Built-in tool
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="You're a specialist in Code Execution",
    tools=[built_in_code_execution],  # Built-in tool
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    sub_agents=[
        search_agent,  # NOT SUPPORTED
        coding_agent   # NOT SUPPORTED
    ],
)
```

### Workaround Using Agent Tools

To use multiple built-in tools or to combine built-in tools with other tools, you can use the `AgentTool` approach:

```python
from google.adk.tools import agent_tool

search_agent = Agent(
    model='gemini-2.0-flash',
    name='SearchAgent',
    instruction="You're a specialist in Google Search",
    tools=[google_search],
)
coding_agent = Agent(
    model='gemini-2.0-flash',
    name='CodeAgent',
    instruction="You're a specialist in Code Execution",
    tools=[built_in_code_execution],
)
root_agent = Agent(
    name="RootAgent",
    model="gemini-2.0-flash",
    description="Root Agent",
    tools=[
        agent_tool.AgentTool(agent=search_agent), 
        agent_tool.AgentTool(agent=coding_agent)
    ],
)
```
