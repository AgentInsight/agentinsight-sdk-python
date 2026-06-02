"""Simplified tests for additional_headers functionality in Langfuse client.

This module tests that additional headers are properly configured in the HTTP clients.
"""

from typing import Sequence

import httpx
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import SpanExporter, SpanExportResult

from agentinsight._client.client import AgentInsight


class NoOpSpanExporter(SpanExporter):
    """Minimal exporter used to verify custom exporter injection."""

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        pass


class TestAdditionalHeadersSimple:
    """Simple test suite for additional_headers functionality."""

    def teardown_method(self):
        """Clean up after each test to avoid singleton interference."""
        from agentinsight._client.resource_manager import AgentInsightResourceManager

        AgentInsightResourceManager.reset()

    def test_httpx_client_has_additional_headers_when_none_provided(self):
        """Test that additional headers are set in httpx client when no custom client is provided."""
        additional_headers = {
            "X-Custom-Header": "custom-value",
            "X-Another-Header": "another-value",
        }

        langfuse = AgentInsight(
            public_key="test-public-key",
            secret_key="test-secret-key",
            host="https://mock-host.com",
            additional_headers=additional_headers,
            tracing_enabled=False,
        )

        assert (
            langfuse._resources.httpx_client.headers["X-Custom-Header"]
            == "custom-value"
        )
        assert (
            langfuse._resources.httpx_client.headers["X-Another-Header"]
            == "another-value"
        )

    def test_custom_httpx_client_with_additional_headers_ignores_additional_headers(
        self,
    ):
        """Test that when additional headers are provided with custom client, additional headers are ignored."""
        existing_headers = {"X-Existing-Header": "existing-value"}
        custom_client = httpx.Client(headers=existing_headers)

        additional_headers = {
            "X-Custom-Header": "custom-value",
            "X-Another-Header": "another-value",
        }

        langfuse = AgentInsight(
            public_key="test-public-key",
            secret_key="test-secret-key",
            host="https://mock-host.com",
            httpx_client=custom_client,
            additional_headers=additional_headers,
            tracing_enabled=False,
        )

        assert langfuse._resources.httpx_client is custom_client

        assert (
            langfuse._resources.httpx_client.headers["x-existing-header"]
            == "existing-value"
        )

        assert "x-custom-header" not in langfuse._resources.httpx_client.headers
        assert "x-another-header" not in langfuse._resources.httpx_client.headers

    def test_custom_httpx_client_without_additional_headers_preserves_client(self):
        """Test that when no additional headers are provided, the custom client is preserved."""
        existing_headers = {"X-Existing-Header": "existing-value"}
        custom_client = httpx.Client(headers=existing_headers)

        langfuse = AgentInsight(
            public_key="test-public-key",
            secret_key="test-secret-key",
            host="https://mock-host.com",
            httpx_client=custom_client,
            additional_headers=None,
            tracing_enabled=False,
        )

        assert (
            langfuse._resources.httpx_client.headers["x-existing-header"]
            == "existing-value"
        )

    def test_media_manager_uses_custom_httpx_client(self):
        """Test that media manager reuses the configured custom httpx client."""
        custom_client = httpx.Client()

        langfuse = AgentInsight(
            public_key="test-public-key",
            secret_key="test-secret-key",
            host="https://mock-host.com",
            httpx_client=custom_client,
            tracing_enabled=False,
        )

        assert langfuse._resources is not None
        assert langfuse._resources._media_manager._httpx_client is custom_client

    def test_none_additional_headers_works(self):
        """Test that passing None for additional_headers works without errors."""
        langfuse = AgentInsight(
            public_key="test-public-key",
            secret_key="test-secret-key",
            host="https://mock-host.com",
            additional_headers=None,
            tracing_enabled=False,
        )

        assert langfuse is not None
        assert langfuse._resources is not None
        assert langfuse._resources.httpx_client is not None

    def test_empty_additional_headers_works(self):
        """Test that passing an empty dict for additional_headers works."""
        langfuse = AgentInsight(
            public_key="test-public-key",
            secret_key="test-secret-key",
            host="https://mock-host.com",
            additional_headers={},
            tracing_enabled=False,
        )

        assert langfuse is not None
        assert langfuse._resources is not None
        assert langfuse._resources.httpx_client is not None

    def test_span_processor_has_additional_headers_in_otel_exporter(self):
        """Test that span processor includes additional headers in OTEL exporter."""
        from agentinsight._client.span_processor import AgentInsightSpanProcessor

        additional_headers = {
            "X-Custom-Trace-Header": "trace-value",
            "X-Override-Default": "override-value",
        }

        processor = AgentInsightSpanProcessor(
            public_key="test-public-key",
            secret_key="test-secret-key",
            base_url="https://mock-host.com",
            additional_headers=additional_headers,
        )

        exporter = processor.span_exporter

        assert exporter._headers["X-Custom-Trace-Header"] == "trace-value"
        assert exporter._headers["X-Override-Default"] == "override-value"

        assert "Authorization" in exporter._headers
        assert "x_langfuse_sdk_name" in exporter._headers
        assert "x_langfuse_public_key" in exporter._headers

        assert exporter._headers["X-Override-Default"] == "override-value"

    def test_span_processor_none_additional_headers_works(self):
        """Test that span processor works with None additional headers."""
        from agentinsight._client.span_processor import AgentInsightSpanProcessor

        processor = AgentInsightSpanProcessor(
            public_key="test-public-key",
            secret_key="test-secret-key",
            base_url="https://mock-host.com",
            additional_headers=None,
        )

        exporter = processor.span_exporter

        assert "Authorization" in exporter._headers
        assert "x_langfuse_sdk_name" in exporter._headers
        assert "x_langfuse_public_key" in exporter._headers

    def test_span_processor_uses_custom_span_exporter_when_provided(self):
        """Test that a custom exporter bypasses the default OTLP exporter construction."""
        from agentinsight._client.span_processor import AgentInsightSpanProcessor

        custom_exporter = NoOpSpanExporter()

        processor = AgentInsightSpanProcessor(
            public_key="test-public-key",
            secret_key="test-secret-key",
            base_url="https://mock-host.com",
            additional_headers={"X-Custom-Trace-Header": "trace-value"},
            span_exporter=custom_exporter,
        )

        assert processor.span_exporter is custom_exporter
