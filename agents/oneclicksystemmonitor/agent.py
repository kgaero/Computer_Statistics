"""Root agent for OneClickSystemMonitor."""

from google.adk.agents import ParallelAgent, SequentialAgent
from google.adk.agents.run_config import RunConfig, StreamingMode

from .callbacks import only_ram_after_agent_callback, skip_agent_if_requested
from deployment.observability import configure_arize_ax
from .sub_agents.cpu.agent import cpu_agent
from .sub_agents.disk.agent import disk_agent
from .sub_agents.memory.agent import memory_agent
from .sub_agents.summary.agent import summary_agent

configure_arize_ax()

RUN_CONFIG = RunConfig(
  streaming_mode=StreamingMode.NONE,
  max_llm_calls=6,
  custom_metadata={"trace": "oneclicksystemmonitor"},
)

system_info_gatherer = ParallelAgent(
  name="system_info_gatherer",
  description="Collects CPU, memory, and disk stats in parallel.",
  sub_agents=[cpu_agent, memory_agent, disk_agent],
)

root_agent = SequentialAgent(
  name="oneclick_system_monitor",
  description="Runs system info collection and summary report generation.",
  sub_agents=[system_info_gatherer, summary_agent],
  before_agent_callback=skip_agent_if_requested,
  after_agent_callback=only_ram_after_agent_callback,
)
