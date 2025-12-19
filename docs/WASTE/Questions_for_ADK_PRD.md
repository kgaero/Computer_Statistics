# PRD Prep Questions for a Coding Agent (Agentic AI • Python • Google ADK)

## 1) High-Level Goal

* Do we need multiple specialties to finish this task, or will one specialty do?
* Will one agent be enough, or do we need multiple agents to get the desired output?
* Are we building a single-agent system or a multi-agent system?
* Should the user see streaming (live) output?
* Will we use `RunConfig` to control runtime behavior and options?
* Do we need the ability to resume stopped agents with `ResumabilityConfig()`?

## 2) Runtime

* Will we run the agent from **ADK Web**?
* Will we run the agent with the **runner**?
* If using the runner, should we call `run_async()`?

## 3) Session & Memory

* Which session service will we use: `BaseSessionService`, `InMemorySessionService`, `VertexAiSessionService`, or `DatabaseSessionService`?
* What keys/fields will we store in `session.state`?
* Is every value in the state serializable?

## 4) Agent Type

* Is the agent’s work deterministic (same input → same output)?
* Is the agent’s work probabilistic (may vary run to run)?

## 5) Sequential Agent

* Which sub-agents will we include?
* In what order will these sub-agents run?
* What are the inputs and outputs for each sub-agent?

## 6) Loop Agent

* Which sub-agents will we include in the loop?
* In what order will they run each iteration?
* What are the inputs and outputs for each sub-agent?
* What is the maximum number of iterations?
* What condition ends the loop?
* Which sub-agents can signal STOP/termination?

## 7) Parallel Agent

* Which sub-agents will run in parallel?
* How many sub-agents will run at the same time?
* Do any dependencies prevent true concurrency?
* Do sub-agents need to share conversation history or state?
* What are the inputs and outputs for each sub-agent?
* Will we launch sub-agents with `run_async()`?
* Where could race conditions happen?
* How will we prevent or handle race conditions?

## 8) Custom Agent

* Do we need conditional logic to choose the next step based on runtime results?
* Do we need complex state management beyond simple pass-through?
* Do sub-agents need to call external APIs, databases, or custom libraries?
* Is the choice of next sub-agent made dynamically at runtime?
* Do we need orchestration that doesn’t fit strictly sequential, parallel, or loop patterns?

## 9) Agent System Instruction

* What is the agent’s name?
* What personality or persona should the agent use?
* What is the agent an expert in?
* What tasks should the agent perform?
* What should the final output look like?
* Do we have example outputs to follow?
* Is a strict JSON output required?
* Should we use a Pydantic class to enforce the JSON shape?

## 10) Model for the Agent

* Which model will the agent use?

## 11) Tools

* Does the agent need tools?
* Which built-in tools fit best for this agent?

  * File search (search files)
  * Web search (search the internet)
  * `built_in_code_execution` (run code and return results)
  * `google_search`
  * `vertex_ai_rag_retrieval`
  * `vertex_ai_search_tool`
  * BigQuery
  * Spanner
  * Bigtable
* Do we need third-party tools?

  * Web search via LangChain’s Tavily
  * Web search via CrewAI’s Serper API
* When should the agent use each tool, and why?
* If built-in tools are not enough, do we need custom function tools?
* What are the exact inputs and outputs for each custom function tool?
* What code will implement each custom function?
* Should any function be wrapped with `LongRunningFunctionTool()`?
* Should the agent call other agents as tools via `AgentTool()`?
* Will the agent call tools asynchronously?
* Do tool calls require human confirmation (`require_confirmation`) or more detailed `request_confirmation`?
* Do we need to call tools hosted on an MCP server using `MCPToolset()`?
* Do we have all parameters required to call each MCP tool such as server details etc.?
* Does any MCP tool need an API key?
* Does any tool require authentication?
* Does any tool need a `ToolContext`?
* Which tools require callbacks, and for what purpose?

  * `before_tool_callback`
  * `after_tool_callback`

## 12) Communication Pattern

* Which session state variables will agents use to pass information?
* Should the agent transfer control to a peer agent using `transfer_to_agent()`?
* Should an `LlmAgent` route calls to a sub-agent?
* Do we need Human-in-the-Loop steps for approvals or decisions?
* Where do we need human confirmation for decisions, verification, security, or oversight?

## 13) Callback

* Do we need callbacks? For what goals (logging, metrics, guardrails, UX)?
* Which callbacks will we use, and why?

  * `before_agent_callback`
  * `after_agent_callback`
  * `before_model_callback`
  * `after_model_callback`
* Do callbacks need a `CallbackContext`?
* Will the user provide any artifact as input?
* Will the agent produce any artifact as output?

## 14) Gaurdrail
Which gaurdrails are required among below?
PII - personally identifiable information
  Common
    Person name
    Email address
    Phone number
    Location
    Date or time
    IP address
    URL
    Credit card number
    International bank account number (IBAN)
    Cryptocurrency wallet address
    Nationality / religion / political group
    Medical license number
  USA
    US bank account number
    US driver license number
    US individual taxpayer identification number (ITIN)
    US passport number
    US Social Security number
  UK
    National Insurance number
    UK NHS number
  Spain
    Spanish NIF number
    Spanish NIE number
  Italy
    Italian fiscal code
    Italian VAT code
    Italian passport number
    Italian driver license number
    Italian identity card number
  Poland
    Polish PESEL number
  Singapore
    Singapore NRIC/FIN
    Singapore UEN
  Australia
    Australian Business Number (ABN)
    Australian Company Number (ACN)
    Australian Tax File Number (TFN)
    Australian Medicare number
  India
    Indian Aadhaar number
    Indian PAN
    Indian passport number
    Indian voter ID number
    Indian vehicle registration number
  Finland
    Finnish personal identity code

Moderation
  Sexual Content
    sexual (Sexually explicit or suggestive content)
    sexual/minors (Sexual content that includes individuals under the age of 18)
  Hate & Harassment
    hate (Hate speech and discriminatory content)
    hate/threatening (Hateful content that also includes violence or serious harm)
    harassment (Harassing or bullying content)
    harassment/threatening (Harassment content that also includes violence or serious harm)
  Self-Harm
    self-harm (Content promoting or depicting self-harm)
    self-harm/intent (Content where the speaker expresses intent to harm oneself)
    self-harm/instructions (Content that provides instructions for self-harm)
  Violence
    violence (Content that depicts death, violence, or physical injury)
    violence/graphic (Content that depicts death, violence, or physical injury in graphic detail)
  Illicit Activities
    illicit (Content that gives advice or instruction on how to commit illicit acts)
    illicit/violent (Illicit content that also includes references to violence or procuring a weapon)

Jailbreak
Hallucination

