import os

BASE_URL = os.getenv("BOOKING_BASE_URL", "https://restful-booker.herokuapp.com").rstrip("/")
USERNAME = os.getenv("BOOKING_USERNAME", "admin")
PASSWORD = os.getenv("BOOKING_PASSWORD", "password123")
REQUEST_TIMEOUT = float(os.getenv("REQUEST_TIMEOUT", "25"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_BACKOFF_SECONDS = float(os.getenv("RETRY_BACKOFF_SECONDS", "2"))
