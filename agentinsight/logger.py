"""Logger configuration for AgentInsight OpenTelemetry integration.

This module initializes and configures loggers used by the AgentInsight OpenTelemetry integration.
It sets up the main 'agentinsight' logger and configures the httpx logger to reduce noise.

Log levels used throughout AgentInsight:
- DEBUG: Detailed tracing information useful for development and diagnostics
- INFO: Normal operational information confirming expected behavior
- WARNING: Indication of potential issues that don't prevent operation
- ERROR: Errors that prevent specific operations but allow continued execution
- CRITICAL: Critical errors that may prevent further operation
"""

import logging

# Create the main AgentInsight logger
agentinsight_logger = logging.getLogger("agentinsight")
agentinsight_logger.setLevel(logging.WARNING)

# Configure httpx logger to reduce noise from HTTP requests
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

# Add console handler if no handlers exist
console_handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
httpx_logger.addHandler(console_handler)
