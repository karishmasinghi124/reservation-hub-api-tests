# Reservation Hub — API Automation Safety Net

## Overview
A Python/Pytest regression suite for the Restful-booker sandbox. The suite focuses on critical booking workflows, high-risk validation rules, authentication, and useful failure diagnostics.

## Setup
Requires Python 3.10+.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows
# .venv\\Scripts\\activate
pip install -r requirements.txt
```

Optional environment variables:
- `BOOKING_BASE_URL` (default: `https://restful-booker.herokuapp.com`)
- `BOOKING_USERNAME` (default sandbox credential: `admin`)
- `BOOKING_PASSWORD` (default sandbox credential: `password123`)
- `REQUEST_TIMEOUT` (default: 25 seconds)

## Run
```bash
pytest
```
The HTML report is generated at `reports/report.html`. Open it in a browser. It contains per-test outcomes and assertion messages; pytest-html also captures captured output. For richer request/response attachments, add a dedicated pytest hook or Allure integration if the team wants artifact-level diagnostics.

Run by feature:
```bash
pytest -m "create or negative"
pytest -m auth
pytest -m "smoke"
```

## Strategy and coverage
- **Health:** bounded polling to absorb the sandbox cold start.
- **Auth:** valid credentials and invalid-credential rejection.
- **Create:** valid payload and high-risk negative price/date validations, plus a missing required field.
- **Read:** retrieve a newly created booking and verify a missing ID returns 404.
- **Update:** authenticated full and partial updates; unauthenticated update rejection.
- **Delete:** authenticated cancellation and verification that the record is no longer readable; unauthenticated delete rejection.
- **Journey:** create/read/update/delete coverage is composed from isolated tests and fixtures rather than depending on test execution order.

## Reliability and shared environment
Each test creates its own booking with a unique generated name and dates. Tests do not depend on the pre-seeded ten records. A fixture attempts best-effort deletion after use. The sandbox can reset independently, so cleanup failures are deliberately non-fatal. Health checks use bounded exponential waits. Only safe read requests are retried; writes are not blindly retried because a timeout could occur after the server has already committed a change.

## Assertions and risk
Assertions validate response content and persistence, not only status codes. Negative price and reversed date tests are marked high risk because they map directly to the incident described in the assignment. The expected validation response is 400/422; if the sandbox returns success, the test fails and the behavior should be documented with captured evidence in `BUGS.md`.

## Deliberate scope limits
This first iteration does not attempt exhaustive schema/property fuzzing, concurrency/load testing, partner-specific authorization, or full contract testing. These are valuable follow-ups but are outside the highest-risk regression path for this time-boxed exercise.

## Known limitations
- Public sandbox data may reset or be affected by other users.
- The API can be slow during cold start; health polling is bounded.
- Credentials are sandbox defaults and configurable via environment variables.
- The initial report uses pytest-html. It records test outcomes and failure tracebacks; request/response bodies are included in assertion messages for API assertion failures. Do not put production secrets in environment variables or reports.
- Live execution is required to confirm the actual seeded defects and populate final evidence in `BUGS.md`.
