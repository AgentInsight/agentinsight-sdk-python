from functools import lru_cache
from importlib.metadata import PackageNotFoundError, version


@lru_cache(maxsize=1)
def get_agentinsight_version() -> str:
    try:
        return version("agentinsight-sdk")
    except PackageNotFoundError:
        return "0.0.0"


__version__ = get_agentinsight_version()
