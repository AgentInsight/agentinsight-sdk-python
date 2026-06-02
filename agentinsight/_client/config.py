from dataclasses import dataclass
from typing import Callable, Dict, Optional

import httpx
from opentelemetry.sdk.trace import ReadableSpan, TracerProvider
from opentelemetry.sdk.trace.export import SpanExporter

from agentinsight.types import MaskFunction


@dataclass
class AgentInsightConfig:
    public_key: Optional[str] = None
    secret_key: Optional[str] = None
    base_url: Optional[str] = None
    timeout: Optional[int] = None
    debug: bool = False
    tracing_enabled: Optional[bool] = True
    flush_at: Optional[int] = None
    flush_interval: Optional[float] = None
    environment: Optional[str] = None
    release: Optional[str] = None
    media_upload_thread_count: Optional[int] = None
    sample_rate: Optional[float] = None
    mask: Optional[MaskFunction] = None
    should_export_span: Optional[Callable[[ReadableSpan], bool]] = None
    additional_headers: Optional[Dict[str, str]] = None
    tracer_provider: Optional[TracerProvider] = None
    span_exporter: Optional[SpanExporter] = None
    httpx_client: Optional[httpx.Client] = None
    strict_mode: bool = False
