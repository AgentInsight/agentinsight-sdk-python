from .CallbackHandler import (
    LangchainCallbackHandler as CallbackHandler,
)

AgentInsightCallbackHandler = CallbackHandler  # For backward compatibility

__all__ = ["CallbackHandler", "AgentInsightCallbackHandler"]
