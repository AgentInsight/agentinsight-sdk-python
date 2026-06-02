import os

from agentinsight._client.client import AgentInsight
from agentinsight.logger import agentinsight_logger

"""
Level	Numeric value
logging.DEBUG	10
logging.INFO	20
logging.WARNING	30
logging.ERROR	40
"""


def test_default_AgentInsight():
    AgentInsight()

    assert agentinsight_logger.level == 30


def test_via_env():
    os.environ["AGENTINSIGHT_DEBUG"] = "True"

    AgentInsight()

    assert agentinsight_logger.level == 10

    os.environ.pop("AGENTINSIGHT_DEBUG")


def test_debug_AgentInsight():
    AgentInsight(debug=True)
    assert agentinsight_logger.level == 10

    agentinsight_logger.setLevel("WARNING")
