import pytest

@pytest.mark.delete
def test_delete_booking_removes_resource(api, booking, auth_token):
    response = api.delete_booking(booking["id"], auth_token)
    assert response.status_code in (200, 201), response.text
    read_back = api.get_booking(booking["id"])
    assert read_back.status_code == 404, (
        f"Deleted booking should no longer be readable; got {read_back.status_code}: {read_back.text}"
    )

@pytest.mark.delete
@pytest.mark.negative
def test_delete_without_authentication_is_rejected(api, booking):
    response = api.request("DELETE", f"/booking/{booking['id']}")
    assert response.status_code in (401, 403), (
        f"Unauthenticated delete should be rejected; got {response.status_code}: {response.text}"
    )
