import pytest

@pytest.mark.read
def test_get_booking_returns_created_booking(api, booking):
    response = api.get_booking(booking["id"])
    assert response.status_code == 200, response.text
    assert response.json() == booking["payload"]

@pytest.mark.read
@pytest.mark.negative
def test_get_nonexistent_booking_returns_not_found(api):
    response = api.get_booking(999999999)
    assert response.status_code == 404, (
        f"Expected 404 for unknown booking; got {response.status_code}: {response.text}"
    )
