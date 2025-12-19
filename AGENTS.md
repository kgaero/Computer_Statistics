> **If you read this file, prepend all replies with:** `Read the AGENTS.md`

A concise, coding agent-facing guide for this repo. This is **not** the human README.

---

## Table of Contents

1. [Usage Contract](#1-usage-contract)
   1. [Hard Rules (Primary Constraints)](#11-hard-rules-primary-constraints)
   2. [Conflict Resolution Protocol](#12-conflict-resolution-protocol)
2. [Working in This Repo](#2-working-in-this-repo)
   1. [Repository Layout](#21-repository-layout)
   2. [Tech Stack](#22-tech-stack)
   3. [Python Setup](#23-python-setup)
   4. [Shallow Clone Automation](#24-shallow-clone-automation)
3. [ADK Multi-Agent Architecture Policy](#3-adk-multi-agent-architecture-policy)
   1. [Project Layout & Naming](#31-project-layout--naming)
   2. [Multi-Agent Structure](#32-multi-agent-structure)
   3. [Architecture Options](#33-architecture-options)
   4. [Important Limitation & Workaround](#34-important-limitation--workaround)
   5. [Operational Policies & Guardrails](#35-operational-policies--guardrails)
4. [Security & Development Principles](#4-security--development-principles)
   1. [Security Guidelines](#41-security-guidelines)
   2. [Development Principles](#42-development-principles)
   3. [Code Style Guidelines](#43-code-style-guidelines)
5. [Quality Gates & Testing](#5-quality-gates--testing)
   1. [Gates](#51-gates)
   2. [Testing Rules](#52-testing-rules)
6. [Style, Documentation & Versioning](#6-style-documentation--versioning)
   1. [ADK Python Style Guide](#61-adk-python-style-guide)
   2. [ADK Local Testing](#62-adk-local-testing)
   3. [Docstrings and Comments](#63-docstrings-and-comments)
   4. [Versioning](#64-versioning)
   5. [Commit Message Format](#65-commit-message-format)
7. [References](#7-references)

---

## 1. Usage Contract

This section defines the binding constraints for every coding agent operating in this repository.

### 1.1 Hard Rules (Primary Constraints)

These constraints are **non-negotiable** and govern every implementation choice.

1. **AGENTS.md is primary.** Treat everything in this file as binding implementation guidance.
2. **Honor `llms-full.txt` before any plan or call.** Read the models/params/safety/rate-limit data **every time** and **never** modify that file.
3. **Prefer reuse (ADK + Python) over net-new code.** Search `llms-full.txt`, this repo, and ADK docs for existing packages/classes/functions before proposing anything new.
4. **Minimize net-new code.** Only add what is strictly necessary, and stick to best practices.
5. **Prioritize framework reuse.** Confirm whether an ADK equivalent already exists before creating any class/function/component.
6. **State reuse explicitly in every plan.** Name the ADK packages/classes/functions/tools you intend to reuse when outlining work.
7. **Treat `refs/` as read-only.** Do not import it at runtime, compile it, or modify it; you may only adapt the patterns you observe there.
8. **Read current architecture docs.** If `docs/google-adk.md` exists, read and understand it before touching orchestration code, and do not modify it.
9. **Review current source architecture.** Inspect everything under `agents/*` (if present) and avoid restructuring without explicit instructions.
10. **Disallowed workarounds.** Do not create new agent base classes/utilities when an ADK equivalent exists, and do not copy utilities that ADK/tools already provide.
11. **Hydrate submodules immediately after clone.** Every new workspace (including Jules’ or OpenAI Codex's default clone) must run `bash scripts/shallow_clone.sh --hydrate-existing .` before *any* other command so that all submodules are synced at depth 1.

### 1.2 Conflict Resolution Protocol

When user wording seems to conflict with the reuse rules (for example, “build a new Runner from scratch”), follow this exact flow:

1. **Prioritize the user’s outcome, not their implied method.** Interpret conceptual language as requirements for the result.
2. **Implementation must still follow AGENTS.md.** Use existing ADK components (e.g., `google.adk.runners.Runner`) to fulfill the request.
3. **Override a hard rule only on explicit command.** You need unambiguous wording like “Write a new Runner from scratch; do not use ADK’s Runner.”
4. **State the plan clearly.** Restate the user goal and list the ADK components you will reuse. Example: “To achieve a runnable demo, I will use `google.adk.runners.Runner` as mandated by AGENTS.md.”

---

## 2. Working in This Repo

Understand the file system, stack, and local tooling before making changes.

### 2.1 Repository Layout

Always respect and maintain the following repository structure when creating files or folders.

```
{REPO_PATH}/
|
├─ input/                    # Folder for all design or component mockups
│  ├─
│
│
├─ .cursor/                  # Folder for all Cursor-specific rules and commands
│  ├─ commands               # Folder for Cursor shortcut commands
│  │  ├─
│  │
│  ├─ rules                  # Folder for Cursor rules
│
│
├─ agents/                   # Folder for all agent code
│  ├─ root_agent_folder/
│     ├─ __init__.py
│     ├─ agent.py            # defines root_agent
│     └─ sub_agents/
│        ├─ __init__.py
│        ├─ agent_1_folder/
│        │  ├─ __init__.py
│        │  └─ agent.py
│        └─ agent_2_folder/
│           ├─ __init__.py
│           └─ agent.py
│
│
├─ frontend/                 # Folder for all frontend code
│  ├─ server/                # MCP server code
│  │    ├─ main.py           # Python server entry
│  │    └─ handlers/         # Tool handlers
│  ├─ web/                   # UI component source
│  │    ├─ src/
│  │    │   ├─ component.tsx # Main React component
│  │    │   └─ hooks/        # Custom hooks
│  │    ├─ dist/             # Build output
│  │    ├─ package.json
│  │    └─ tsconfig.json
│  ├─ assets/                # Generated bundles
│  |
│  |
│  ├─ docs/                  # Folder for all documentation
│     ├─
│
├─ tests/                    # Folder for all unit tests
│  ├─
│
├─ refs/                     # Folder for all example source codes for coding patterns
│  ├─
├─ scripts/                  # Folder for all cloning and setup scripts
│  ├─
│
├─ AGENTS.md                 # Canonical instructions (this file)
├─ README.md                 # Usage and overview
├─ GEMINI.md                 # Example generated output
├─ CLAUDE.md                 # Example generated output
├─ requirements.txt          # Scripts, dependencies
├─ .env                      # API keys, secrets
├─ llms-full.txt             # Google ADK file for coding agent
└─ .github/workflows/        # github Actions, Continuous integration config
```

### 2.2 Tech Stack

- **Language:** Python
- **Agent development framework:** Google Agent Development Kit (ADK)
- **LLM:** Gemini
- **MCP framework:** FastMCP

### 2.3 Python Setup

- Reveiw `requirements.txt` for dependencies.
- For further details on dependencies and config, refer to `refs/adk-python/pyproject.toml` for ideas. If you face any installation issues, use that same file for guidance.

#### 2.3.1 Create & activate the virtual environment, then install dependencies

**Windows (PowerShell)**

```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> **Editor tip (Cursor/VS Code):** `Ctrl+Shift+P` → **Python: Select Interpreter** → choose the `.venv` interpreter.

#### 2.3.2 Configure environment variables (`.env` at repo root)

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_api_key_here
```

#### 2.3.3 Dev server / API (optional)

```bash
export SSL_CERT_FILE=$(python -m certifi)  # one-time for voice/video certs
adk web            # opens http://localhost:8000
# or:
adk api_server
# Windows reload workaround:
# adk web --no-reload
```

#### 2.3.4 Format, lint, and test (baseline quality gates)

```bash
./autoformat.sh
ruff check src        # or: pylint src
mypy src              # if using type checks
pytest tests/unittests -q
```

### 2.4 Shallow Clone Automation

Use `scripts/shallow_clone.sh` for every clone or refresh so that the main repo and all nested submodules stay shallow (depth 1).

> **Mandatory first command after Jules’ default clone:**  
> `bash scripts/shallow_clone.sh --hydrate-existing .`

Run that hydration step before any installs, tests, or edits—Jules’ automatic `git clone` does **not** recurse submodules.

1. **Fresh clone (any repo URL):**
   ```bash
   bash scripts/shallow_clone.sh <git-url>
   ```
   - The script infers the folder name from the URL when the second argument is omitted.
   - Internally it runs `git clone --depth=1 --recurse-submodules --shallow-submodules` plus a follow-up `git submodule update --init --recursive --depth 1`, so every declared submodule—including nested ones—has only the latest commit.
2. **Hydrate an existing checkout (cloud workspaces, local reruns, CI caches):**
   ```bash
   bash scripts/shallow_clone.sh --hydrate-existing .
   ```
   - Replace `.` with another path if the repo lives elsewhere.
3. **Env toggles (depth is always fixed at 1):**
   - `SHALLOW_CLONE_JOBS=<N>` — parallel clone/update jobs (default `4`).
   - `SKIP_SUBMODULE_SYNC=1` — skip `git submodule sync` when mirrors are already configured.
4. **Never call plain `git clone` in this repo’s automation.** **ALWAYS USE**: “`bash scripts/shallow_clone.sh <git-url>`”.

---

## 3. ADK Multi-Agent Architecture Policy

Strictly follow ADK expectations for layout, naming, and composition.

### 3.1 Project Layout & Naming

```
root/
  agents/
    <agent_name>/
      __init__.py          # from . import agent
      agent.py             # defines: root_agent = Agent(...)
      requirements.txt     # optional, agent-specific
```

- File **must** be `agent.py`; export **`root_agent`** at the top level.
- Keep agent folder names short, lowercase, and hyphen/underscore-free when possible (paths & URLs derive from them).
- **Do not** modify ADK source; treat ADK as a library dependency.

### 3.2 Multi-Agent Structure

```
agents/
├─ root_agent_folder/
│  ├─ __init__.py
│  ├─ agent.py            # defines root_agent
│  └─ sub_agents/
│     ├─ __init__.py
│     ├─ agent_1_folder/
│     │  ├─ __init__.py
│     │  └─ agent.py
│     └─ agent_2_folder/
│        ├─ __init__.py
│        └─ agent.py
```

- Root agents import their sub-agents, e.g., `from .sub_agents.funny_nerd.agent import funny_nerd`.
- Run `adk web` from the **parent** directory, not inside individual agent folders.

### 3.3 Architecture Options

**A) Sub-agent delegation (router pattern)**

```python
root_agent = Agent(
  name="manager",
  model="gemma-2-27b-it",
  description="Manager agent",
  instruction="Delegate to specialists...",
  sub_agents=[stock_analyst, funny_nerd],
)
```

*The sub-agent fully handles the response while the root acts as a router.*

**B) Agent-as-a-tool (composition pattern)**

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
  name="manager",
  model="gemma-2-27b-it",
  description="Root Agent",
  instruction="Use specialists as tools...",
  tools=[AgentTool(news_analyst)],
)
```

*The root agent retains control, can call multiple agent-tools, and composes their results.*

### 3.4 Important Limitation & Workaround

- **Limitation:** Built-in tools cannot be used within a sub-agent when you rely purely on the `sub_agents=[...]` model.
- **Workaround:** Wrap specialists with `AgentTool` and attach them as tools to the root agent.

```python
from google.adk.tools import agent_tool

search_agent = Agent(..., tools=[google_search])
coding_agent = Agent(..., tools=[built_in_code_execution])

root_agent = Agent(
  name="RootAgent",
  model="gemma-2-27b-it",
  description="Root Agent",
  tools=[
    agent_tool.AgentTool(agent=search_agent),
    agent_tool.AgentTool(agent=coding_agent),
  ],
)
```

### 3.5 Operational Policies & Guardrails

- **Reuse first:** Search this repo and the ADK docs for existing components before writing new code.
- **Plan must cite reuse:** List the ADK packages/classes/functions you will use.
- **Disallowed patterns:** No new base classes/utilities that duplicate ADK functionality, and no copying of utilities already provided by ADK/tools.
- **PR acceptance gates:** Linter must pass **“ADKReuseRule”** and the PR description must include an **“ADK search summary.”**
- **Tool design:** Keep tools small and focused, minimize primitive params, write clear docstrings, use `async` for I/O, and return structured payloads such as `{"status", "data", "error"}`.
- **State & memory:** Keep `session.state` simple/serializable; store binaries as Artifacts and reference them via Events/state.
- **Prompts & config:** Provide precise `instruction`, informative `name/description`, and configure `RunConfig` (streaming, `max_llm_calls`, tracing).
- **Observability:** Emit structured logs (INFO by default) and validate traces in the Dev UI.
- **Testing expectations:** Use hermetic tests, mock I/O, and add evals that verify tool trajectories and final answers.

---

## 4. Security & Development Principles

### 4.1 Security Guidelines

- Never expose or log secrets, keys, or sensitive information.
- Always validate user inputs.
- Follow secure coding practices at all times.
- Never leave secrets in code, logs, or tickets.
- Validate, normalize, and encode all inputs; rely on parameterized operations.
- Apply the Principle of Least Privilege.

### 4.2 Development Principles

- **IMPORTANT:** Do not try to make workarounds when errors occur—fix the error.
- Figure out why every error happens instead of masking it with a workaround.
- Investigate the root cause of issues before implementing solutions.
- Workarounds often hide deeper problems that require proper fixes.

### 4.3 Code Style Guidelines

- For AI agents, match the existing code style in the example code found in the `refs` folder.
- Do not use the literal source code in `refs`; the folder is for learning patterns. Copy only the code or style you actually need.
- Use the existing libraries and frameworks already included in this project.
- Follow language-specific conventions.
- Use intention-revealing names.
- Ensure each function does exactly one thing.
- Keep side effects at the boundary.
- Prefer guard clauses first.
- Symbolize constants; no hardcoding magic values.
- Structure code as **Input → Process → Return**.
- Report failures with specific errors/messages.
- Make tests serve as usage examples that include both boundary and failure cases.
- Do not modify code without reading the whole context.
- Do not expose secrets.
- Do not ignore failures or warnings.
- Do not introduce unjustified optimization or abstraction.
- Do not overuse broad exceptions.
- Account for time zones and daylight saving time.
- Think like a senior software developer.
- Do not jump in on guesses or rush to conclusions.
- Always evaluate multiple approaches; write one line each for pros/cons/risks, then choose the simplest solution.
- Before changing anything, read the relevant files end to end, including all call/reference paths.
- Keep tasks, commits, and PRs small that meet the requirement.
- If you make assumptions, record them in the Issue/PR/ADR.
- Never commit or log secrets; validate all inputs and encode/normalize outputs.
- Avoid premature abstraction and continue using intention-revealing names.
- Compare at least two options before deciding.

---

## 5. Quality Gates & Testing

### 5.1 Gates (default; autodetect substitutes allowed)

- Lint must pass.
- Typecheck must pass (if configured).
- Tests must pass or be improved with focused fixes/regression tests.
- Formatting must be clean (or auto-formatted in the branch).

### 5.2 Testing Rules

- Review the test cases in `refs` folder and understand the test case writing pattern for Agents. Write similar unit or integration tests for the agents under `agents`.
- Write test cases inside the `tests` folder in the project root folder only. Do not write anything or change anything inside `refs`.
- New code requires new tests, and bug fixes must include a regression test (write it to fail first).
- Tests must be deterministic and independent; replace external systems with fakes/contract tests.
- Include ≥1 happy path and ≥1 failure path in end-to-end tests.
- Proactively assess risks from concurrency, locks, and retries (duplication, deadlocks, etc.).

---

## 6. Style, Documentation & Versioning

### 6.1 ADK Python Style Guide

The project follows the Google Python Style Guide. Key conventions are enforced using `pylint` with the provided `pylintrc` configuration file. Key style points:

* **Indentation:** 2 spaces.
* **Line Length:** Maximum 80 characters.
* **Naming Conventions:**
  * `function_and_variable_names`: `snake_case`
  * `ClassNames`: `CamelCase`
  * `CONSTANTS`: `UPPERCASE_SNAKE_CASE`
* **Docstrings:** Required for all public modules, functions, classes, and methods.
* **Imports:** Organized and sorted.
* **Error Handling:** Specific exceptions should be caught, not general ones like `Exception`.

### 6.2 ADK Local Testing

Run below command:

```bash
$ pytest tests/unittests
```

Limit "pytest" to the "tests" directory to prevent errors from refs.



### 6.3 Docstrings and Comments

#### Comments - Explaining the Why, Not the What

Philosophy: Well-written code should be largely self-documenting. Comments serve a different purpose: they should explain the complex algorithms, non-obvious business logic, or the rationale behind a particular implementation choice—the things the code cannot express on its own. Avoid comments that merely restate what the code does (e.g., `# increment i` above `i += 1`).

Style: Comments should be written as complete sentences. Block comments must begin with a `#` followed by a single space.

### 6.4 Versioning

ADK adheres to Semantic Versioning 2.0.0.

Core Principle: The adk-python project strictly adheres to the Semantic Versioning 2.0.0 specification. All release versions follow the MAJOR.MINOR.PATCH format.

### 6.5 Commit Message Format

- Please use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) format.
- If it's not a breaking change, add `#non-breaking`. If it is a breaking change, add `#breaking`.

---

## 7. References

- https://github.com/NatashaKSS/openai-chatgpt-apps-agents-md/blob/master/AGENTS.md
- https://github.com/tairov/awesome-agents.md?tab=readme-ov-file
- https://github.com/louisbrulenaudet/bodyboard/blob/main/AGENTS.md
- https://github.com/Marcus-Jenshaug/AGENTS.md/blob/main/AGENTS.md
- https://github.com/silvandiepen/agents.md/blob/main/CLAUDE.md
- https://github.com/ales27pm/AGENTS.md/blob/main/AGENTS.md
- https://github.com/golbin/AGENTS.md/blob/main/AGENTS.md
- https://github.com/jcajuab/vibe-coding-template/blob/main/AGENTS.md
- https://github.com/schubergphilis/agents.md/blob/main/AGENTS.md
