import pytest
from utils.data_factory import valid_booking

@pytest.mark.update
def test_full_update_changes_booking(api, booking, auth_token):
    updated = valid_booking()
    response = api.update_booking(booking["id"], updated, auth_token)
    assert response.status_code == 200, response.text
    assert response.json() == updated
    assert api.get_booking(booking["id"]).json() == updated

@pytest.mark.update
def test_partial_update_changes_only_requested_field(api, booking, auth_token):
    response = api.patch_booking(
        booking["id"], {"additionalneeds": "Late checkout"}, auth_token
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["additionalneeds"] == "Late checkout"
    assert body["firstname"] == booking["payload"]["firstname"]
    assert body["totalprice"] == booking["payload"]["totalprice"]

@pytest.mark.update
@pytest.mark.negative
def test_update_without_authentication_is_rejected(api, booking):
    response = api.request("PUT", f"/booking/{booking['id']}",
                           json=valid_booking())
    assert response.status_code in (401, 403), (
        f"Unauthenticated update should be rejected; got {response.status_code}: {response.text}"
    )
