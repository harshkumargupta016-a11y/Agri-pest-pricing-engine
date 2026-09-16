import pytest

from api.rate_limiter import redis_client


@pytest.fixture(autouse=True)
def reset_redis_state():
    try:
        redis_client.flushdb()
    except Exception:
        pass
    yield
