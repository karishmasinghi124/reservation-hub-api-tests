import pytest
from config.settings import USERNAME, PASSWORD
from utils.api_client import BookingAPI
from utils.data_factory import valid_booking

@pytest.fixture
def api():
    return BookingAPI()

@pytest.fixture
def auth_token(api):
    response = api.authenticate(USERNAME, PASSWORD)
    assert response.status_code == 200, (
        f"Authentication failed: status={response.status_code}, body={response.text}"
    )
    token = response.json().get("token")
    assert token, f"Auth response did not contain token: {response.text}"
    return token

@pytest.fixture
def booking(api):
    payload = valid_booking()
    response = api.create_booking(payload)
    assert response.status_code == 200, (
        f"Booking setup failed: status={response.status_code}, body={response.text}"
    )
    booking_id = response.json()["bookingid"]
    yield {"id": booking_id, "payload": payload}
    # Best-effort cleanup. Shared instance may reset or another process may delete it.
    try:
        token_response = api.authenticate("admin", "password123")
        token = token_response.json().get("token")
        if token:
            api.delete_booking(booking_id, token)
    except Exception:
        pass
