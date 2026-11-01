import time
import requests
from config.settings import BASE_URL, REQUEST_TIMEOUT, MAX_RETRIES

class BookingAPI:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method, path, **kwargs):
        url = f"{BASE_URL}{path}"
        last_error = None
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.request(
                    method, url, timeout=REQUEST_TIMEOUT, **kwargs
                )
                # Retry only transient server errors. Do not retry writes blindly:
                # a timed-out POST may already have created a booking.
                if response.status_code in (502, 503, 504) and method.upper() in ("GET", "HEAD"):
                    if attempt < MAX_RETRIES - 1:
                        time.sleep(2 ** attempt)
                        continue
                return response
            except requests.RequestException as exc:
                last_error = exc
                # Retrying GET is safe; retrying POST/PUT/DELETE can duplicate or
                # repeat a state change, so surface those errors immediately.
                if method.upper() not in ("GET", "HEAD") or attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(2 ** attempt)
        raise last_error

    def authenticate(self, username, password):
        return self.request("POST", "/auth", json={
            "username": username, "password": password
        })

    def create_booking(self, payload):
        return self.request("POST", "/booking", json=payload)

    def get_booking(self, booking_id):
        return self.request("GET", f"/booking/{booking_id}")

    def update_booking(self, booking_id, payload, token):
        return self.request("PUT", f"/booking/{booking_id}",
                            json=payload, headers={"Cookie": f"token={token}"})

    def patch_booking(self, booking_id, payload, token):
        return self.request("PATCH", f"/booking/{booking_id}",
                            json=payload, headers={"Cookie": f"token={token}"})

    def delete_booking(self, booking_id, token):
        return self.request("DELETE", f"/booking/{booking_id}",
                            headers={"Cookie": f"token={token}"})
