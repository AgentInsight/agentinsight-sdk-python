""".. include:: ../README.md"""

from typing import Any, Optional

from agentinsight.batch_evaluation import (
    BatchEvaluationResult,
    BatchEvaluationResumeToken,
    CompositeEvaluatorFunction,
    EvaluatorInputs,
    EvaluatorStats,
    MapperFunction,
)
from agentinsight.experiment import Evaluation, RegressionError, RunnerContext

from ._client import client as _client_module
from ._client.attributes import AgentInsightOtelSpanAttributes
from ._client.client import Serializable
from ._client.config import AgentInsightConfig
from ._client.constants import ObservationTypeLiteral
from ._client.exceptions import (
    AgentInsightAuthenticationError,
    AgentInsightConfigurationError,
    AgentInsightConnectionError,
    AgentInsightError,
    AgentInsightSerializationError,
    AgentInsightTimeoutError,
)
from ._client.get_client import get_client
from ._client.observe import observe
from ._client.propagation import propagate_attributes
from ._client.span import (
    AgentInsightAgent,
    AgentInsightChain,
    AgentInsightEmbedding,
    AgentInsightEvaluator,
    AgentInsightEvent,
    AgentInsightGeneration,
    AgentInsightGuardrail,
    AgentInsightRetriever,
    AgentInsightSpan,
    AgentInsightTool,
)
from ._version import __version__
from .span_filter import (
    KNOWN_LLM_INSTRUMENTATION_SCOPE_PREFIXES,
    is_agentinsight_span,
    is_default_export_span,
    is_genai_span,
    is_known_llm_instrumentor,
    is_langfuse_span,
)

AgentInsight = _client_module.AgentInsight
AgentInsightClient = _client_module.AgentInsightClient

_default_client: Optional[AgentInsight] = None


def init(
    *,
    public_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    base_url: Optional[str] = None,
    **kwargs: Any,
) -> AgentInsight:
    global _default_client
    _default_client = AgentInsight(
        public_key=public_key, secret_key=secret_key, base_url=base_url, **kwargs
    )
    return _default_client


__all__ = [
    "AgentInsight",
    "AgentInsightClient",
    "AgentInsightConfig",
    "init",
    "get_client",
    "observe",
    "propagate_attributes",
    "ObservationTypeLiteral",
    "AgentInsightSpan",
    "AgentInsightGeneration",
    "AgentInsightEvent",
    "AgentInsightOtelSpanAttributes",
    "Serializable",
    "AgentInsightAgent",
    "AgentInsightTool",
    "AgentInsightChain",
    "AgentInsightEmbedding",
    "AgentInsightEvaluator",
    "AgentInsightRetriever",
    "AgentInsightGuardrail",
    "AgentInsightError",
    "AgentInsightAuthenticationError",
    "AgentInsightConnectionError",
    "AgentInsightSerializationError",
    "AgentInsightConfigurationError",
    "AgentInsightTimeoutError",
    "Evaluation",
    "EvaluatorInputs",
    "MapperFunction",
    "CompositeEvaluatorFunction",
    "EvaluatorStats",
    "BatchEvaluationResumeToken",
    "BatchEvaluationResult",
    "RunnerContext",
    "RegressionError",
    "__version__",
    "is_default_export_span",
    "is_langfuse_span",
    "is_agentinsight_span",
    "is_genai_span",
    "is_known_llm_instrumentor",
    "KNOWN_LLM_INSTRUMENTATION_SCOPE_PREFIXES",
    "experiment",
    "api",
]
