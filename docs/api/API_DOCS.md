# BloodChain API Reference Document

> **Swagger UI (interactive docs):** http://localhost:<port>/api/docs/
> **Swagger JSON (import into Postman/Swagger Editor):** http://localhost:<port>/api/docs/?format=openapi
> **Postman Collection:** `docs/api/bloodchain_postman.json`

---

## 1. Donor Service

**Base URL:** `http://localhost:8001/api/donor/`
**Swagger UI:** http://localhost:8001/api/docs/
**Model:** `Donor` — `full_name`, `email`, `phone_number`, `blood_type`, `date_of_birth`, `is_eligible`, `registered_at`
**Model:** `Appointment` — `donor_email`, `appointment_date`, `status` (scheduled/completed/cancelled), `notes`, `created_at`

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **POST** | `/register/` | Register a new blood donor (must be 18+) |
| 2 | **GET** | `/list/` | List all donors. Filters: `?blood_type=A+`, `?eligible=true/false` |
| 3 | **GET** | `/profile/{email}/` | Get donor profile by email |
| 4 | **PATCH** | `/profile/{email}/update/` | Partial update of donor profile fields |
| 5 | **POST** | `/appointments/create/` | Create a new appointment |
| 6 | **GET** | `/appointments/{donor_email}/` | List appointments by donor email |
| 7 | **PATCH** | `/appointments/{pk}/update/` | Update appointment status/details |
| 8 | **GET** | `/eligibility/{donor_email}/` | Check donor eligibility (56-day gap, age, donation count) |

### Request/Response Examples

**POST /register/**
```json
{
    "full_name": "John Doe",
    "email": "john@example.com",
    "phone_number": "+1234567890",
    "blood_type": "A+",
    "date_of_birth": "1990-01-15"
}
```
→ `201 Created`: Returns full donor object.
→ `400 Bad Request`: Validation errors (underage, invalid blood type, etc.)

**GET /eligibility/{donor_email}/**
→ `200 OK`:
```json
{
    "is_eligible": true,
    "last_donation_date": null,
    "next_eligible_date": "2026-06-05",
    "days_until_next": 0,
    "total_donations": 3,
    "blood_type": "A+",
    "age": 36
}
```

---

## 2. Hospital Service

**Base URL:** `http://localhost:8002/api/hospital/`
**Swagger UI:** http://localhost:8002/api/docs/
**Model:** `Hospital` — `name`, `location`, `contact_email`, `contact_phone`, `is_active`, `registered_at`
**Model:** `BloodRequest` — `hospital` (FK), `blood_type`, `units_needed`, `status` (pending/fulfilled/cancelled), `requested_at`
**Model:** `BloodStock` — `hospital_id`, `blood_type`, `units_available`

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **POST** | `/register/` | Register a new hospital |
| 2 | **GET** | `/profile/{email}/` | Get hospital profile by contact email |
| 3 | **PATCH** | `/profile/{email}/update/` | Upsert hospital profile (create if not exists) |
| 4 | **POST** | `/request/` | Create a new blood request (status = pending) |
| 5 | **GET** | `/requests/` | List all blood requests |
| 6 | **GET** | `/requests/{pk}/` | Get blood request detail |
| 7 | **PATCH** | `/requests/{pk}/update/` | Update blood request status/details |
| 8 | **GET** | `/stock/{hospital_id}/` | List blood stock for a hospital |
| 9 | **POST** | `/stock/{hospital_id}/update/` | Upsert blood stock entry |

---

## 3. Blood Tracking Service

**Base URL:** `http://localhost:8003/api/tracking/`
**Swagger UI:** http://localhost:8003/api/docs/
**Model:** `BloodBag` — `bag_id` (UUID, auto), `blood_type`, `donor_email`, `status` (collected/tested/stored/transfused/discarded), `collected_at`, `stored_at`

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **POST** | `/bag/collect/` | Record a new blood bag collection |
| 2 | **GET** | `/bag/{bag_id}/` | Get blood bag by bag_id |
| 3 | **GET** | `/bags/donor/{donor_email}/` | List all bags for a donor (newest first) |

### Request/Response Examples

**POST /bag/collect/**
```json
{
    "blood_type": "O-",
    "donor_email": "john@example.com"
}
```
→ `201 Created`: `{"bag_id": "a1b2c3d4-..."}`
→ `400 Bad Request`: Validation errors.

---

## 4. Notifications Service

**Base URL:** `http://localhost:8004/api/notifications/`
**Swagger UI:** http://localhost:8004/api/docs/
**Model:** `EmergencyAlert` — `recipient_email`, `message`, `blood_type_needed`, `hospital_name`, `is_emergency`, `sent_at`, `acknowledged`

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **POST** | `/alert/` | Send an emergency blood alert |
| 2 | **GET** | `/list/` | List all notifications |

### Request/Response Examples

**POST /alert/**
```json
{
    "recipient_email": "hospital@example.com",
    "message": "Urgent: O- blood needed!",
    "blood_type_needed": "O-",
    "hospital_name": "City Hospital",
    "is_emergency": true
}
```
→ `201 Created`: Returns alert object with `sent_at` timestamp.

---

## 5. User Management Service

**Base URL:** `http://localhost:8009/api/users/`
**Swagger UI:** http://localhost:8009/api/docs/
**Model:** `User` — `email` (PK), `username`, `password`, `role` (donor/hospital/admin), `is_active`, `created_at`
**Model:** `Token` — `user` (FK), `token`, `created_at`

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **GET** | `/users/` | List all users |
| 2 | **POST** | `/users/` | Create a user |
| 3 | **GET** | `/users/{pk}/` | Get user detail |
| 4 | **PUT** | `/users/{pk}/` | Full update of a user |
| 5 | **PATCH** | `/users/{pk}/` | Partial update of a user |
| 6 | **DELETE** | `/users/{pk}/` | Delete a user |
| 7 | **POST** | `/api/auth/register/` | Register a new user; returns auth token |
| 8 | **POST** | `/api/auth/login/` | Login with email + password; returns auth token |

### Request/Response Examples

**POST /api/auth/register/**
```json
{
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "donor"
}
```
→ `201 Created`:
```json
{
    "token": "a1b2c3d4...",
    "user": {"email": "john@example.com", "role": "donor"}
}
```

**POST /api/auth/login/**
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```
→ `200 OK`: Returns token + user object.
→ `401 Unauthorized`: Invalid credentials.

---

## 6. Data Warehouse / Analytics Service

**Base URL:** `http://localhost:8006/api/analytics/`
**Swagger UI:** http://localhost:8006/api/docs/
**Model:** `DonationStat` — `date`, `blood_type`, `region`, `total_donations`
**Model:** `HospitalDemand` — `date`, `hospital_id`, `blood_type`, `units_needed`

### Donation Stats
| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **GET** | `/warehouse/donation-stats/` | List donation stats. Filters: `?date=`, `?blood_type=`, `?region=` |
| 2 | **POST** | `/warehouse/donation-stats/` | Create a donation stat entry |
| 3 | **GET** | `/warehouse/donation-stats/{pk}/` | Get donation stat detail |
| 4 | **PUT** | `/warehouse/donation-stats/{pk}/` | Full update |
| 5 | **PATCH** | `/warehouse/donation-stats/{pk}/` | Partial update |
| 6 | **DELETE** | `/warehouse/donation-stats/{pk}/` | Delete entry |

### Hospital Demands
| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 7 | **GET** | `/warehouse/hospital-demands/` | List hospital demands. Filters: `?date=`, `?hospital_id=`, `?blood_type=` |
| 8 | **POST** | `/warehouse/hospital-demands/` | Create a demand entry |
| 9 | **GET** | `/warehouse/hospital-demands/{pk}/` | Get demand detail |
| 10 | **PUT** | `/warehouse/hospital-demands/{pk}/` | Full update |
| 11 | **PATCH** | `/warehouse/hospital-demands/{pk}/` | Partial update |
| 12 | **DELETE** | `/warehouse/hospital-demands/{pk}/` | Delete entry |

---

## 7. Location Service

**Base URL:** `http://localhost:8007/api/location/`
**Swagger UI:** http://localhost:8007/api/docs/
**Model:** `Location` — `name`, `address`, `latitude`, `longitude`, `location_type` (donation_center/hospital/lab), `is_active`, `created_at`

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **GET** | `/locations/` | List active locations. Filters: `?location_type=`, `?is_active=` |
| 2 | **POST** | `/locations/` | Create a location |
| 3 | **GET** | `/locations/{pk}/` | Get location detail |
| 4 | **PUT** | `/locations/{pk}/` | Full update |
| 5 | **PATCH** | `/locations/{pk}/` | Partial update |
| 6 | **DELETE** | `/locations/{pk}/` | Delete location |

---

## 8. Rewards Service

**Base URL:** `http://localhost:8008/api/rewards/`
**Swagger UI:** http://localhost:8008/api/docs/
**Model:** `Reward` — `donor_id`, `points`, `reason`, `created_at`
**Model:** `Redemption` — `donor_id`, `reward`, `points_spent`, `redeemed_at`

### Rewards
| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | **GET** | `/rewards/` | List rewards. Filter: `?donor_id=` |
| 2 | **POST** | `/rewards/` | Create a reward |
| 3 | **GET** | `/rewards/{pk}/` | Get reward detail |
| 4 | **PUT** | `/rewards/{pk}/` | Full update |
| 5 | **PATCH** | `/rewards/{pk}/` | Partial update |
| 6 | **DELETE** | `/rewards/{pk}/` | Delete reward |

### Redemptions
| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 7 | **GET** | `/redemptions/` | List redemptions. Filter: `?donor_id=` |
| 8 | **POST** | `/redemptions/` | Create a redemption |
| 9 | **GET** | `/redemptions/{pk}/` | Get redemption detail |
| 10 | **PUT** | `/redemptions/{pk}/` | Full update |
| 11 | **PATCH** | `/redemptions/{pk}/` | Partial update |
| 12 | **DELETE** | `/redemptions/{pk}/` | Delete redemption |

---

## Service Port Summary

| Service | Port | Swagger UI |
|---------|------|------------|
| Donor | 8001 | http://localhost:8001/api/docs/ |
| Hospital | 8002 | http://localhost:8002/api/docs/ |
| Blood Tracking | 8003 | http://localhost:8003/api/docs/ |
| Notifications | 8004 | http://localhost:8004/api/docs/ |
| Data Warehouse | 8006 | http://localhost:8006/api/docs/ |
| Location | 8007 | http://localhost:8007/api/docs/ |
| Rewards | 8008 | http://localhost:8008/api/docs/ |
| User Management | 8009 | http://localhost:8009/api/docs/ |
| Nginx (frontend) | 80 | http://localhost/ |

---

## Common Status Codes

| Code | Meaning |
|------|---------|
| `200 OK` | Successful GET/PATCH/PUT |
| `201 Created` | Successful POST (resource created) |
| `400 Bad Request` | Validation error in request body |
| `401 Unauthorized` | Invalid credentials (auth endpoints) |
| `404 Not Found` | Resource does not exist |
| `405 Method Not Allowed` | Wrong HTTP method for endpoint |

---

## Postman / Swagger Editor Import

1. Open Postman or https://editor.swagger.io/
2. Click **Import** → **Raw Text**
3. Paste the JSON from any `http://localhost:<port>/api/docs/?format=openapi` URL
4. A full collection with all endpoints, request bodies, and example responses will be generated

Individual Swagger JSON files are also saved at:
- `docs/api/swagger_donor.json`
- `docs/api/swagger_hospital.json`
- `docs/api/swagger_blood_tracking.json`
- `docs/api/swagger_notifications.json`
- `docs/api/swagger_user_management.json`
- `docs/api/swagger_data_warehouse.json`
- `docs/api/swagger_location.json`
- `docs/api/swagger_rewards.json`
