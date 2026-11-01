import pytest
from config.settings import USERNAME, PASSWORD

@pytest.mark.auth
def test_valid_credentials_return_token(api):
    response = api.authenticate(USERNAME, PASSWORD)
    assert response.status_code == 200, response.text
    assert response.json().get("token"), response.text

@pytest.mark.auth
@pytest.mark.negative
def test_invalid_credentials_are_rejected(api):
    response = api.authenticate("wrong-user", "wrong-password")
    assert response.status_code in (400, 401, 403), (
        f"Invalid credentials should be rejected; got {response.status_code}: {response.text}"
    )
