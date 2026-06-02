class AgentInsightError(Exception):
    pass


class AgentInsightAuthenticationError(AgentInsightError):
    pass


class AgentInsightConnectionError(AgentInsightError):
    pass


class AgentInsightSerializationError(AgentInsightError):
    pass


class AgentInsightConfigurationError(AgentInsightError):
    pass


class AgentInsightTimeoutError(AgentInsightError):
    pass
