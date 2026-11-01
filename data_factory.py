from datetime import date, timedelta
from uuid import uuid4

def valid_booking():
    # Unique names make each test's data independent and easier to identify.
    suffix = uuid4().hex[:8]
    today = date.today()
    return {
        "firstname": f"QA{suffix}",
        "lastname": "Automation",
        "totalprice": 250,
        "depositpaid": True,
        "bookingdates": {
            "checkin": (today + timedelta(days=7)).isoformat(),
            "checkout": (today + timedelta(days=10)).isoformat()
        },
        "additionalneeds": "Breakfast"
    }
