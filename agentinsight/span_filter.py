"""Public span filter helpers for AgentInsight OpenTelemetry export control."""

from agentinsight._client.span_filter import (
    KNOWN_LLM_INSTRUMENTATION_SCOPE_PREFIXES,
    is_agentinsight_span,
    is_default_export_span,
    is_genai_span,
    is_known_llm_instrumentor,
    is_langfuse_span,
)

__all__ = [
    "is_default_export_span",
    "is_langfuse_span",
    "is_agentinsight_span",
    "is_genai_span",
    "is_known_llm_instrumentor",
    "KNOWN_LLM_INSTRUMENTATION_SCOPE_PREFIXES",
]
