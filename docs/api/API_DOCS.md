# BloodChain API Reference Document

## Donor Service
Base URL: `http://localhost:8001/api/donor/`

### 1) Register Donor
* **Method:** `POST`
* **URL:** `/register/`
* **Description:** Registers a new donor.
* **Request Body:**
  ```json
  {
      "full_name": "string",
      "email": "string",
      "phone_number": "string",
      "blood_type": "string",
      "date_of_birth": "string (YYYY-MM-DD)"
  }
  ```
* **Response:**
  * `201 Created`: Returns donor data on success.
  * `400 Bad Request`: Validation errors.

### 2) Get Donor Profile
* **Method:** `GET`
* **URL:** `/profile/{email}/`
* **Description:** Returns donor profile.
* **Request Body:** None
* **Response:**
  * `200 OK`: Returns donor profile data.
  * `404 Not Found`: If donor doesn't exist.

## Hospital Service
Base URL: `http://localhost:8002/api/hospital/`

### 3) Create Blood Request
* **Method:** `POST`
* **URL:** `/request/`
* **Description:** Creates blood request.
* **Request Body:**
  ```json
  {
      "hospital": "string",
      "blood_type": "string",
      "units_needed": "integer"
  }
  ```
* **Response:**
  * `201 Created`: Success.
  * `400 Bad Request`: Validation errors.

### 4) Get All Blood Requests
* **Method:** `GET`
* **URL:** `/requests/`
* **Description:** Returns all blood requests.
* **Request Body:** None
* **Response:**
  * `200 OK`: Array of blood requests.

### 5) Get Blood Stock
* **Method:** `GET`
* **URL:** `/stock/{hospital_id}/`
* **Description:** Returns blood stock for hospital.
* **Request Body:** None
* **Response:**
  * `200 OK`: Array of blood stock objects.

## Blood Tracking Service
Base URL: `http://localhost:8003/api/tracking/`

### 6) Record Blood Bag
* **Method:** `POST`
* **URL:** `/bag/collect/`
* **Description:** Records new blood bag.
* **Request Body:**
  ```json
  {
      "blood_type": "string"
  }
  ```
* **Response:**
  * `201 Created`: Returns `{"bag_id": "uuid"}`.
  * `400 Bad Request`: Validation errors.

### 7) Get Bag Details
* **Method:** `GET`
* **URL:** `/bag/{bag_id}/`
* **Description:** Returns bag details.
* **Request Body:** None
* **Response:**
  * `200 OK`: Blood bag details.
  * `404 Not Found`: If bag not found.

## Rewards Service
Base URL: `http://localhost:8004/api/rewards/`

### 8) Mint Reward Tokens
* **Method:** `POST`
* **URL:** `/mint/`
* **Description:** Mints tokens for donor.
* **Request Body:**
  ```json
  {
      "donor_email": "string",
      "donor_wallet": "string",
      "tokens_minted": "integer",
      "bag_id": "string"
  }
  ```
* **Response:**
  * `201 Created`: Success.
  * `400 Bad Request`: Validation errors.

### 9) Get All Rewards
* **Method:** `GET`
* **URL:** `/list/`
* **Description:** Returns all reward records.
* **Request Body:** None
* **Response:**
  * `200 OK`: Array of reward records.

## Notifications Service
Base URL: `http://localhost:8005/api/notifications/`

### 10) Send Emergency Alert
* **Method:** `POST`
* **URL:** `/alert/`
* **Description:** Sends emergency alert.
* **Request Body:**
  ```json
  {
      "recipient_email": "string",
      "message": "string",
      "blood_type_needed": "string",
      "hospital_name": "string",
      "is_emergency": "boolean"
  }
  ```
* **Response:**
  * `201 Created`: Success.
  * `400 Bad Request`: Validation errors.

### 11) Get All Notifications
* **Method:** `GET`
* **URL:** `/list/`
* **Description:** Returns all notifications.
* **Request Body:** None
* **Response:**
  * `200 OK`: Array of notification records.