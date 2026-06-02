"""Span attribute management for AgentInsight OpenTelemetry integration.

This module defines constants and functions for managing OpenTelemetry span attributes
used by AgentInsight. It provides a structured approach to creating and manipulating
attributes for different span types (trace, span, generation) while ensuring consistency.

The module includes:
- Attribute name constants organized by category
- Functions to create attribute dictionaries for different entity types
- Utilities for serializing and processing attribute values
"""

import json
from datetime import datetime
from typing import Any, Dict, Literal, Optional, Union

from agentinsight._client.constants import (
    ObservationTypeGenerationLike,
    ObservationTypeSpanLike,
)
from agentinsight._utils.serializer import EventSerializer
from agentinsight.api import MapValue
from agentinsight.model import PromptClient
from agentinsight.types import SpanLevel


class AgentInsightOtelSpanAttributes:
    TRACE_NAME = "langfuse.trace.name"
    TRACE_NAME_NEW = "agentinsight.trace.name"
    TRACE_USER_ID = "user.id"
    TRACE_USER_ID_NEW = "agentinsight.user.id"
    TRACE_SESSION_ID = "session.id"
    TRACE_SESSION_ID_NEW = "agentinsight.session.id"
    TRACE_TAGS = "langfuse.trace.tags"
    TRACE_TAGS_NEW = "agentinsight.trace.tags"
    TRACE_PUBLIC = "langfuse.trace.public"
    TRACE_PUBLIC_NEW = "agentinsight.trace.public"
    TRACE_METADATA = "langfuse.trace.metadata"
    TRACE_METADATA_NEW = "agentinsight.trace.metadata"
    TRACE_INPUT = "langfuse.trace.input"
    TRACE_INPUT_NEW = "agentinsight.trace.input"
    TRACE_OUTPUT = "langfuse.trace.output"
    TRACE_OUTPUT_NEW = "agentinsight.trace.output"

    OBSERVATION_TYPE = "langfuse.observation.type"
    OBSERVATION_TYPE_NEW = "agentinsight.observation.type"
    OBSERVATION_METADATA = "langfuse.observation.metadata"
    OBSERVATION_METADATA_NEW = "agentinsight.observation.metadata"
    OBSERVATION_LEVEL = "langfuse.observation.level"
    OBSERVATION_LEVEL_NEW = "agentinsight.observation.level"
    OBSERVATION_STATUS_MESSAGE = "langfuse.observation.status_message"
    OBSERVATION_STATUS_MESSAGE_NEW = "agentinsight.observation.status_message"
    OBSERVATION_INPUT = "langfuse.observation.input"
    OBSERVATION_INPUT_NEW = "agentinsight.observation.input"
    OBSERVATION_OUTPUT = "langfuse.observation.output"
    OBSERVATION_OUTPUT_NEW = "agentinsight.observation.output"

    OBSERVATION_COMPLETION_START_TIME = "langfuse.observation.completion_start_time"
    OBSERVATION_COMPLETION_START_TIME_NEW = (
        "agentinsight.observation.completion_start_time"
    )
    OBSERVATION_MODEL = "langfuse.observation.model.name"
    OBSERVATION_MODEL_NEW = "agentinsight.observation.model.name"
    OBSERVATION_MODEL_PARAMETERS = "langfuse.observation.model.parameters"
    OBSERVATION_MODEL_PARAMETERS_NEW = "agentinsight.observation.model.parameters"
    OBSERVATION_USAGE_DETAILS = "langfuse.observation.usage_details"
    OBSERVATION_USAGE_DETAILS_NEW = "agentinsight.observation.usage_details"
    OBSERVATION_COST_DETAILS = "langfuse.observation.cost_details"
    OBSERVATION_COST_DETAILS_NEW = "agentinsight.observation.cost_details"
    OBSERVATION_PROMPT_NAME = "langfuse.observation.prompt.name"
    OBSERVATION_PROMPT_NAME_NEW = "agentinsight.observation.prompt.name"
    OBSERVATION_PROMPT_VERSION = "langfuse.observation.prompt.version"
    OBSERVATION_PROMPT_VERSION_NEW = "agentinsight.observation.prompt.version"

    ENVIRONMENT = "langfuse.environment"
    ENVIRONMENT_NEW = "agentinsight.environment"
    RELEASE = "langfuse.release"
    RELEASE_NEW = "agentinsight.release"
    VERSION = "langfuse.version"
    VERSION_NEW = "agentinsight.version"

    AS_ROOT = "langfuse.internal.as_root"
    AS_ROOT_NEW = "agentinsight.internal.as_root"

    EXPERIMENT_ID = "langfuse.experiment.id"
    EXPERIMENT_ID_NEW = "agentinsight.experiment.id"
    EXPERIMENT_NAME = "langfuse.experiment.name"
    EXPERIMENT_NAME_NEW = "agentinsight.experiment.name"
    EXPERIMENT_DESCRIPTION = "langfuse.experiment.description"
    EXPERIMENT_DESCRIPTION_NEW = "agentinsight.experiment.description"
    EXPERIMENT_METADATA = "langfuse.experiment.metadata"
    EXPERIMENT_METADATA_NEW = "agentinsight.experiment.metadata"
    EXPERIMENT_DATASET_ID = "langfuse.experiment.dataset.id"
    EXPERIMENT_DATASET_ID_NEW = "agentinsight.experiment.dataset.id"
    EXPERIMENT_ITEM_ID = "langfuse.experiment.item.id"
    EXPERIMENT_ITEM_ID_NEW = "agentinsight.experiment.item.id"
    EXPERIMENT_ITEM_EXPECTED_OUTPUT = "langfuse.experiment.item.expected_output"
    EXPERIMENT_ITEM_EXPECTED_OUTPUT_NEW = "agentinsight.experiment.item.expected_output"
    EXPERIMENT_ITEM_METADATA = "langfuse.experiment.item.metadata"
    EXPERIMENT_ITEM_METADATA_NEW = "agentinsight.experiment.item.metadata"
    EXPERIMENT_ITEM_ROOT_OBSERVATION_ID = "langfuse.experiment.item.root_observation_id"
    EXPERIMENT_ITEM_ROOT_OBSERVATION_ID_NEW = (
        "agentinsight.experiment.item.root_observation_id"
    )


def create_trace_attributes(
    *,
    input: Optional[Any] = None,
    output: Optional[Any] = None,
    public: Optional[bool] = None,
) -> dict:
    attributes = {
        AgentInsightOtelSpanAttributes.TRACE_INPUT: _serialize(input),
        AgentInsightOtelSpanAttributes.TRACE_OUTPUT: _serialize(output),
        AgentInsightOtelSpanAttributes.TRACE_PUBLIC: public,
    }

    return {k: v for k, v in attributes.items() if v is not None}


def create_span_attributes(
    *,
    metadata: Optional[Any] = None,
    input: Optional[Any] = None,
    output: Optional[Any] = None,
    level: Optional[SpanLevel] = None,
    status_message: Optional[str] = None,
    version: Optional[str] = None,
    observation_type: Optional[
        Union[ObservationTypeSpanLike, Literal["event"]]
    ] = "span",
) -> dict:
    attributes = {
        AgentInsightOtelSpanAttributes.OBSERVATION_TYPE: observation_type,
        AgentInsightOtelSpanAttributes.OBSERVATION_LEVEL: level,
        AgentInsightOtelSpanAttributes.OBSERVATION_STATUS_MESSAGE: status_message,
        AgentInsightOtelSpanAttributes.VERSION: version,
        AgentInsightOtelSpanAttributes.OBSERVATION_INPUT: _serialize(input),
        AgentInsightOtelSpanAttributes.OBSERVATION_OUTPUT: _serialize(output),
        **_flatten_and_serialize_metadata(metadata, "observation"),
    }

    return {k: v for k, v in attributes.items() if v is not None}


def create_generation_attributes(
    *,
    name: Optional[str] = None,
    completion_start_time: Optional[datetime] = None,
    metadata: Optional[Any] = None,
    level: Optional[SpanLevel] = None,
    status_message: Optional[str] = None,
    version: Optional[str] = None,
    model: Optional[str] = None,
    model_parameters: Optional[Dict[str, MapValue]] = None,
    input: Optional[Any] = None,
    output: Optional[Any] = None,
    usage_details: Optional[Dict[str, int]] = None,
    cost_details: Optional[Dict[str, float]] = None,
    prompt: Optional[PromptClient] = None,
    observation_type: Optional[ObservationTypeGenerationLike] = "generation",
) -> dict:
    attributes = {
        AgentInsightOtelSpanAttributes.OBSERVATION_TYPE: observation_type,
        AgentInsightOtelSpanAttributes.OBSERVATION_LEVEL: level,
        AgentInsightOtelSpanAttributes.OBSERVATION_STATUS_MESSAGE: status_message,
        AgentInsightOtelSpanAttributes.VERSION: version,
        AgentInsightOtelSpanAttributes.OBSERVATION_INPUT: _serialize(input),
        AgentInsightOtelSpanAttributes.OBSERVATION_OUTPUT: _serialize(output),
        AgentInsightOtelSpanAttributes.OBSERVATION_MODEL: model,
        AgentInsightOtelSpanAttributes.OBSERVATION_PROMPT_NAME: prompt.name
        if prompt and not prompt.is_fallback
        else None,
        AgentInsightOtelSpanAttributes.OBSERVATION_PROMPT_VERSION: prompt.version
        if prompt and not prompt.is_fallback
        else None,
        AgentInsightOtelSpanAttributes.OBSERVATION_USAGE_DETAILS: _serialize(
            usage_details
        ),
        AgentInsightOtelSpanAttributes.OBSERVATION_COST_DETAILS: _serialize(
            cost_details
        ),
        AgentInsightOtelSpanAttributes.OBSERVATION_COMPLETION_START_TIME: _serialize(
            completion_start_time
        ),
        AgentInsightOtelSpanAttributes.OBSERVATION_MODEL_PARAMETERS: _serialize(
            model_parameters
        ),
        **_flatten_and_serialize_metadata(metadata, "observation"),
    }

    return {k: v for k, v in attributes.items() if v is not None}


def _serialize(obj: Any) -> Optional[str]:
    if obj is None or isinstance(obj, str):
        return obj

    return json.dumps(obj, cls=EventSerializer)


def _flatten_and_serialize_metadata_values(
    metadata: Optional[Dict[str, Any]],
) -> Optional[Dict[str, str]]:
    if metadata is None:
        return None

    flattened_metadata: Dict[str, str] = {}

    def flatten_value(path: str, value: Any) -> None:
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                flatten_value(f"{path}.{nested_key}", nested_value)

            return

        serialized_value = _serialize(value)

        if serialized_value is not None:
            flattened_metadata[path] = serialized_value

    for key, value in metadata.items():
        flatten_value(str(key), value)

    return flattened_metadata


def _flatten_and_serialize_metadata(
    metadata: Any, type: Literal["observation", "trace"]
) -> dict:
    prefix = (
        AgentInsightOtelSpanAttributes.OBSERVATION_METADATA
        if type == "observation"
        else AgentInsightOtelSpanAttributes.TRACE_METADATA
    )

    metadata_attributes: Dict[str, Union[str, int, None]] = {}

    if not isinstance(metadata, dict):
        metadata_attributes[prefix] = _serialize(metadata)
    else:
        for key, value in metadata.items():
            metadata_attributes[f"{prefix}.{key}"] = (
                value
                if isinstance(value, str) or isinstance(value, int)
                else _serialize(value)
            )

    return metadata_attributes
