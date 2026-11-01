# Bug Report — Reservation Hub / Restful-booker

> Important: These are reproducible defect candidates encoded as regression checks. Run the suite against the live sandbox and replace the status below with observed evidence before submitting. Do not present a candidate as a confirmed finding unless the actual response has been captured.

## BUG-01 — Booking API accepts a negative total price
- **Status:** Pending live reproduction
- **Severity:** High — invalid financial data can reach partner systems and cause incorrect booking totals or reconciliation.
- **Endpoint:** `POST /booking`
- **Steps to reproduce:**
  1. Send the request below.
  2. Inspect the HTTP status and response body.
  3. If a booking ID is returned, retrieve it using `GET /booking/{id}`.
- **Request:**
```bash
curl -i -X POST 'https://restful-booker.herokuapp.com/booking' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname":"QA Negative Price",
    "lastname":"Regression",
    "totalprice":-1,
    "depositpaid":true,
    "bookingdates":{"checkin":"2030-10-20","checkout":"2030-10-22"},
    "additionalneeds":"Breakfast"
  }'
```
- **Expected:** Request is rejected with a client error (400/422); no booking is created.
- **Actual:** Capture exact status, response body, and whether a subsequent GET returns the created record.
- **Impact:** A negative monetary value can corrupt financial reporting and partner booking workflows.

## BUG-02 — Booking API accepts checkout date earlier than checkin
- **Status:** Pending live reproduction
- **Severity:** High — invalid stay duration can break availability, pricing, and downstream reservation workflows.
- **Endpoint:** `POST /booking`
- **Request:**
```bash
curl -i -X POST 'https://restful-booker.herokuapp.com/booking' \
  -H 'Content-Type: application/json' \
  -d '{
    "firstname":"QA Invalid Dates",
    "lastname":"Regression",
    "totalprice":250,
    "depositpaid":true,
    "bookingdates":{"checkin":"2030-10-20","checkout":"2030-10-19"},
    "additionalneeds":"Breakfast"
  }'
```
- **Expected:** Request is rejected with 400/422 and no booking is persisted.
- **Actual:** Capture exact status, response body, and follow-up GET result.
- **Impact:** An impossible stay duration may cause incorrect availability and booking calculations.

## Evidence to add before submission
For every confirmed defect, record the run date/time, status code, response body, booking ID (if created), and a follow-up GET result. If the API rejects either payload, mark that case as not reproduced rather than claiming a defect.
