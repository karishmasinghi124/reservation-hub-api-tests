import pytest
from utils.data_factory import valid_booking

@pytest.mark.create
def test_create_booking_returns_id_and_persisted_fields(api):
    payload = valid_booking()
    response = api.create_booking(payload)
    assert response.status_code == 200, response.text
    body = response.json()
    assert isinstance(body.get("bookingid"), int), body
    assert body.get("booking") == payload, body
    read_back = api.get_booking(body["bookingid"])
    assert read_back.status_code == 200, read_back.text
    assert read_back.json() == payload

@pytest.mark.create
@pytest.mark.negative
@pytest.mark.risk_high
def test_negative_total_price_is_rejected(api):
    payload = valid_booking()
    payload["totalprice"] = -1
    response = api.create_booking(payload)
    assert response.status_code in (400, 422), (
        "Negative total price must be rejected. "
        f"Actual status={response.status_code}, body={response.text}"
    )

@pytest.mark.create
@pytest.mark.negative
@pytest.mark.risk_high
def test_checkout_before_checkin_is_rejected(api):
    payload = valid_booking()
    payload["bookingdates"]["checkin"] = "2030-10-20"
    payload["bookingdates"]["checkout"] = "2030-10-19"
    response = api.create_booking(payload)
    assert response.status_code in (400, 422), (
        "Checkout earlier than checkin must be rejected. "
        f"Actual status={response.status_code}, body={response.text}"
    )

@pytest.mark.create
@pytest.mark.negative
def test_missing_required_firstname_is_rejected(api):
    payload = valid_booking()
    payload.pop("firstname")
    response = api.create_booking(payload)
    assert response.status_code in (400, 422), (
        f"Missing firstname should be rejected; got {response.status_code}: {response.text}"
    )
