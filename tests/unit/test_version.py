from importlib.metadata import version

import agentinsight


def test_package_version_matches_distribution_metadata():
    assert agentinsight.__version__ == version("agentinsight-sdk")
