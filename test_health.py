import time
import pytest

@pytest.mark.smoke
def test_health_endpoint_returns_success(api):
    # Cold-start aware polling; bounded so a genuinely unavailable service fails clearly.
    last = None
    for attempt in range(4):
        last = api.request("GET", "/ping")
        if last.status_code == 201:
            break
        time.sleep(2 ** attempt)
    assert last.status_code == 201, (
        f"Health check failed after retries: status={last.status_code}, body={last.text}"
    )
