"""Environment variable definitions for AgentInsight OpenTelemetry integration.

This module defines environment variables used to configure the AgentInsight OpenTelemetry integration.
Each environment variable includes documentation on its purpose, expected values, and defaults.
"""

AGENTINSIGHT_TRACING_ENVIRONMENT = "AGENTINSIGHT_TRACING_ENVIRONMENT"
"""
.. envvar:: AGENTINSIGHT_TRACING_ENVIRONMENT

The tracing environment. Can be any lowercase alphanumeric string with hyphens and underscores that does not start with 'agentinsight'.

**Default value:** ``"default"``
"""

AGENTINSIGHT_RELEASE = "AGENTINSIGHT_RELEASE"
"""
.. envvar:: AGENTINSIGHT_RELEASE

Release number/hash of the application to provide analytics grouped by release.
"""


AGENTINSIGHT_PUBLIC_KEY = "AGENTINSIGHT_PUBLIC_KEY"
"""
.. envvar:: AGENTINSIGHT_PUBLIC_KEY

Public API key of AgentInsight project
"""

AGENTINSIGHT_SECRET_KEY = "AGENTINSIGHT_SECRET_KEY"
"""
.. envvar:: AGENTINSIGHT_SECRET_KEY

Secret API key of AgentInsight project
"""

AGENTINSIGHT_BASE_URL = "AGENTINSIGHT_BASE_URL"
"""
.. envvar:: AGENTINSIGHT_BASE_URL

Base URL of AgentInsight API. Can be set via `AGENTINSIGHT_BASE_URL` environment variable.

**Default value:** ``"https://agent.goldebridge.com"``
"""

AGENTINSIGHT_HOST = "AGENTINSIGHT_HOST"
"""
.. envvar:: AGENTINSIGHT_HOST

Deprecated. Use AGENTINSIGHT_BASE_URL instead. Host of AgentInsight API. Can be set via `AGENTINSIGHT_HOST` environment variable.

**Default value:** ``"https://agent.goldebridge.com"``
"""

AGENTINSIGHT_OTEL_TRACES_EXPORT_PATH = "AGENTINSIGHT_OTEL_TRACES_EXPORT_PATH"
"""
.. envvar:: AGENTINSIGHT_OTEL_TRACES_EXPORT_PATH

URL path on the configured host to export traces to.

**Default value:** ``/api/public/otel/v1/traces``
"""

AGENTINSIGHT_DEBUG = "AGENTINSIGHT_DEBUG"
"""
.. envvar:: AGENTINSIGHT_DEBUG

Enables debug mode for more verbose logging.

**Default value:** ``"False"``
"""

AGENTINSIGHT_TRACING_ENABLED = "AGENTINSIGHT_TRACING_ENABLED"
"""
.. envvar:: AGENTINSIGHT_TRACING_ENABLED

Enables or disables the AgentInsight client. If disabled, all observability calls to the backend will be no-ops. Default is True. Set to `False` to disable tracing.

**Default value:** ``"True"``
"""

AGENTINSIGHT_MEDIA_UPLOAD_THREAD_COUNT = "AGENTINSIGHT_MEDIA_UPLOAD_THREAD_COUNT"
"""
.. envvar:: AGENTINSIGHT_MEDIA_UPLOAD_THREAD_COUNT 

Number of background threads to handle media uploads from trace ingestion.

**Default value:** ``1``
"""

AGENTINSIGHT_FLUSH_AT = "AGENTINSIGHT_FLUSH_AT"
"""
.. envvar:: AGENTINSIGHT_FLUSH_AT

Max batch size until a new ingestion batch is sent to the API.
**Default value:** same as OTEL ``OTEL_BSP_MAX_EXPORT_BATCH_SIZE``
"""

AGENTINSIGHT_FLUSH_INTERVAL = "AGENTINSIGHT_FLUSH_INTERVAL"
"""
.. envvar:: AGENTINSIGHT_FLUSH_INTERVAL

Max delay in seconds until a new ingestion batch is sent to the API.
**Default value:** same as OTEL ``OTEL_BSP_SCHEDULE_DELAY``
"""

AGENTINSIGHT_SAMPLE_RATE = "AGENTINSIGHT_SAMPLE_RATE"
"""
.. envvar: AGENTINSIGHT_SAMPLE_RATE

Float between 0 and 1 indicating the sample rate of traces to bet sent to AgentInsight servers.

**Default value**: ``1.0``

"""
AGENTINSIGHT_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED = (
    "AGENTINSIGHT_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED"
)
"""
.. envvar: AGENTINSIGHT_OBSERVE_DECORATOR_IO_CAPTURE_ENABLED

Default capture of function args, kwargs and return value when using the @observe decorator.

Having default IO capture enabled for observe decorated function may have a performance impact on your application
if large or deeply nested objects are attempted to be serialized. Set this value to `False` and use manual
input/output setting on your observation to avoid this.

**Default value**: ``True``
"""

AGENTINSIGHT_MEDIA_UPLOAD_ENABLED = "AGENTINSIGHT_MEDIA_UPLOAD_ENABLED"
"""
.. envvar: AGENTINSIGHT_MEDIA_UPLOAD_ENABLED

Controls whether media detection and upload is attempted by the SDK.

**Default value**: ``True``
"""

AGENTINSIGHT_TIMEOUT = "AGENTINSIGHT_TIMEOUT"
"""
.. envvar: AGENTINSIGHT_TIMEOUT

Controls the timeout for all API requests in seconds

**Default value**: ``5``
"""

AGENTINSIGHT_PROMPT_CACHE_DEFAULT_TTL_SECONDS = (
    "AGENTINSIGHT_PROMPT_CACHE_DEFAULT_TTL_SECONDS"
)
"""
.. envvar: AGENTINSIGHT_PROMPT_CACHE_DEFAULT_TTL_SECONDS

Controls the default time-to-live (TTL) in seconds for cached prompts.
This setting determines how long prompt responses are cached before they expire.

**Default value**: ``60``
"""
