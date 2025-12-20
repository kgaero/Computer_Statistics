# 📝 Product Requirements Document (PRD)

## Product Title

**OneClickSystemMonitor**

---

## 1. Objective

Develop an AI Agent that collects system statistics on memory, CPU, and disk in parallel using sub-agents, and presents a plain-text summary report to end users. The agentic platform must be **Google ADK**, implemented in **Python**, with **sub-agents using function tools** to collect statistics. User invocation will occur via **ADK Web**.

---

## 2. Target Users

* **Primary Users:** Everyday Windows users (non-technical or semi-technical)
* **Use Case:** Users who want to quickly understand the performance status of their computer (e.g., why it's slow or how resources are being used)

---

## 3. Problem Statement

Most end users struggle to interpret raw data from tools like Task Manager. They need an easy tool that provides a clear, plain-text performance summary of CPU, memory, and disk usage without requiring technical skills.

---

## 4. Solution Overview

Build an AI-driven system monitor that:

* Uses **Google ADK** as the agentic AI platform
* Runs on **Windows OS**
* Uses **parallel sub-agents** to collect system information for CPU, memory, and disk
* Ensures sub-agents use **function tools** for statistics collection
* Aggregates results via a **summary agent**
* Displays a **concise plain-text report**
* Is invoked by users through **ADK Web**

**Note on AGENTS.md:** I don’t have access to your AGENTS.md file in this environment. The architecture below is written to be compatible with typical ADK multi-agent + tool patterns and can be adjusted to match your exact conventions once that file is provided.

---

## 5. Key Features & Functionality

### 5.1 Sub-Agents (Parallel Workers) — Tool-Based Collection

Each sub-agent runs independently in parallel and uses function tools to collect and return structured system metrics (JSON-serializable dicts). The main agent orchestrates these in parallel and passes results to the summary agent.

* **Memory Sub-Agent**

  * Function Tool: `collect_memory_stats() -> MemoryStats`
  * Collects: total RAM, available RAM, memory usage %, cache/standby (if available), swap/pagefile usage

* **CPU Sub-Agent**

  * Function Tool: `collect_cpu_stats() -> CPUStats`
  * Collects: current usage %, per-core usage %, process-level CPU hogs, CPU temperature (if supported)

* **Disk Sub-Agent**

  * Function Tool: `collect_disk_stats() -> DiskStats`
  * Collects: total storage, free space, disk usage %, read/write throughput (best-effort), fragmentation (optional)

**Tool requirements (applies to all sub-agents):**

* Tools must be deterministic and side-effect free
* Tools must have clear schemas (typed keys, consistent units)
* Tools must handle missing/unsupported metrics gracefully (return null/None + reason)

### 5.2 Summary Agent

* **Responsibility:** Consolidate sub-agent outputs and generate a user-friendly plain-text report.
* **Optional Function Tool:** `generate_summary_report(memory: MemoryStats, cpu: CPUStats, disk: DiskStats) -> str`
* **Behavior:**

  * Normalizes units (GB, %, MB/s)
  * Highlights top drivers (e.g., low free RAM, high CPU, low disk space)
  * Produces an “overall status” using simple heuristics (Low/Moderate/High load)
  * Notes any unavailable metrics (e.g., “CPU temperature not supported on this device”)

### 5.3 Report Output

* Report is displayed as **plain text** in the **ADK Web UI**
* Copy/paste friendly
* Includes timestamp and system identifier (optional, non-sensitive)

---

## 6. Sample Output

**System Performance Summary (as of 2025-12-19 14:05):**

🧠 **Memory:**

* Total RAM: 16 GB
* Available: 4.2 GB (26%)
* Status: High usage – consider closing unused applications.

⚙️ **CPU:**

* Current usage: 72%
* Highest core: Core 3 at 89%
* Top process: Chrome.exe (32%)

💾 **Disk:**

* C:\ Drive: 82% used (410 GB of 500 GB)
* Read/Write: Moderate (throughput best-effort)

🔎 **Overall:** Your system is under moderate to high load. Closing browser tabs or restarting could improve performance.

---

## 7. Technical Requirements

* **Platform:** Windows 10 and later
* **Language:** Python
* **Agentic Platform:** Google ADK
* **Invocation Surface:** ADK Web (user triggers request via ADK Web UI)
* **Dependencies (metrics collection):**

  * `psutil` and/or Windows APIs (WMI / Performance Counters)
  * Throughput and temperature metrics are best-effort and must degrade gracefully
* **Concurrency:**

  * Sub-agent tool calls must run in parallel (async or thread/process pool)
  * Per-tool timeouts; partial results allowed (summary indicates missing sections)
* **Performance:**

  * Report generation (collection + summary) should complete in under 3 seconds on typical consumer hardware (best-effort if OS APIs are slow)
* **Security / Privacy:**

  * Local-only system inspection
  * No external network calls required for stats collection
  * Limit sensitive exposure: avoid file paths; keep process listing minimal (name + %)
* **Architecture / Conventions:**

  * Main orchestrator agent triggers sub-agents and passes results to summary agent
  * Sub-agents rely exclusively on function tools for collection
  * Standard tool schemas and structured outputs

---

## 8. User Flow (ADK Web)

1. User opens ADK Web and submits a request (e.g., “Generate system performance summary”)
2. Main agent orchestrates parallel sub-agent tool execution
3. Summary agent consolidates and formats results
4. Plain-text report is rendered in ADK Web response panel

---

## 10. Success Metrics

* ⏱ Time to complete full report: < 3 seconds (best-effort with graceful degradation)
* 👍 User understanding of report: > 90% of users report it’s “clear”
* 🧪 System compatibility: 95% success rate on tested Windows systems
* ✅ Reliability: > 99% of runs return at least a partial summary without crashing
