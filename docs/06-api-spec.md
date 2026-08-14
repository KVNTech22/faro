# FARO - API Specification

Version: 1.0 MVP

Base URL

https://api.faro.kvnttech.com/api/v1

Authentication

Bearer JWT

Authorization: Bearer <token>

---

# AUTH

## Register

POST /auth/register

Request

{
  "email": "user@email.com",
  "password": "********",
  "phone": "+573001234567",
  "first_name": "Andres",
  "last_name": "Perez"
}

Response

{
  "user_id": "uuid",
  "message": "Account created"
}

---

## Login

POST /auth/login

Request

{
  "email": "user@email.com",
  "password": "********"
}

Response

{
  "access_token": "",
  "refresh_token": "",
  "expires_in": 3600
}

---

# Authentication API

---

## Register

POST /auth/register

Request

```json
{
  "email": "usuario@correo.com",
  "password": "Password123",
  "phone": "+573001234567",
  "full_name": "Andrés Pérez"
}
```

Response

```json
{
  "message": "User registered successfully",
  "email_verification_sent": true
}
```

---

## Verify Email

POST /auth/verify-email

Request

```json
{
  "token": "verification_token"
}
```

Response

```json
{
  "message": "Email verified successfully"
}
```

---

## Login

POST /auth/login

Request

```json
{
  "email": "usuario@correo.com",
  "password": "Password123"
}
```

Response

```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "token_type": "bearer",
  "expires_in": 900
}
```

---

## Refresh Token

POST /auth/refresh

Request

```json
{
  "refresh_token": "refresh_token"
}
```

Response

```json
{
  "access_token": "new_access_token",
  "token_type": "bearer",
  "expires_in": 900
}
```

---

## Logout

POST /auth/logout

Headers

Authorization: Bearer access_token

Request

```json
{
  "refresh_token": "refresh_token"
}
```

Response

```json
{
  "message": "Logged out successfully"
}
```

---

## Forgot Password

POST /auth/forgot-password

Request

```json
{
  "email": "usuario@correo.com"
}
```

Response

```json
{
  "message": "Password reset email sent"
}
```

---

## Reset Password

POST /auth/reset-password

Request

```json
{
  "token": "reset_token",
  "new_password": "NewPassword123"
}
```

Response

```json
{
  "message": "Password updated successfully"
}
```

---

## Google Sign-In

POST /auth/google

Request

```json
{
  "id_token": "google_id_token"
}
```

Response

```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "token_type": "bearer",
  "expires_in": 900,
  "is_new_user": false
}
```

---

## Get Current User

GET /auth/me

Headers

Authorization: Bearer access_token

Response

```json
{
  "id": "uuid",
  "email": "usuario@correo.com",
  "full_name": "Andrés Pérez",
  "phone": "+573001234567",
  "email_verified": true,
  "phone_verified": false
}
```

## Google Login

POST /auth/google

Request

{
  "google_token": ""
}

Response

{
  "access_token": "",
  "refresh_token": ""
}

---

## Refresh Token

POST /auth/refresh

Request

{
  "refresh_token": ""
}

Response

{
  "access_token": ""
}

---

# USERS

## Get Profile

GET /users/me

Response

{
  "id": "",
  "email": "",
  "phone": "",
  "first_name": "",
  "last_name": ""
}

---

## Update Profile

PUT /users/me

---

# MEDICAL PROFILE

GET /users/me/medical-profile

PUT /users/me/medical-profile

Response

{
  "blood_type": "O+",
  "allergies": "",
  "medications": "",
  "critical_information": ""
}

---

# CRITICAL INFORMATION

GET /users/me/critical-info

PUT /users/me/critical-info

---

# EMERGENCY CONTACTS

GET /users/me/emergency-contacts

POST /users/me/emergency-contacts

PUT /users/me/emergency-contacts/{id}

DELETE /users/me/emergency-contacts/{id}

---

# CIRCLES

## Create Circle

POST /circles

Request

{
  "name": "Familia Perez",
  "description": "Grupo principal"
}

---

## List My Circles

GET /circles

---

## Circle Detail

GET /circles/{circle_id}

---

## Update Circle

PUT /circles/{circle_id}

---

## Delete Circle

DELETE /circles/{circle_id}

---

# CIRCLE MEMBERS

GET /circles/{circle_id}/members

POST /circles/{circle_id}/members

DELETE /circles/{circle_id}/members/{member_id}

PUT /circles/{circle_id}/members/{member_id}/role

PUT /circles/{circle_id}/primary-contact

Request

{
  "user_id": "uuid"
}
---

# INVITATIONS

POST /circles/{circle_id}/invite

Request

{
  "email": "persona@email.com"
}

o

{
  "phone": "+573001234567"
}

---

GET /invitations

POST /invitations/{id}/accept

POST /invitations/{id}/reject

---

# DEPENDENTS

GET /dependents

POST /dependents

PUT /dependents/{id}

DELETE /dependents/{id}

---

# PETS

GET /pets

POST /pets

PUT /pets/{id}

DELETE /pets/{id}

---

## Pet Owners

POST /pets/{id}/owners

DELETE /pets/{id}/owners/{user_id}

GET /pets/{id}/owners

---

# ALERT SETTINGS

GET /alert-settings

PUT /alert-settings

Request

{
  "notification_magnitude": 3.0,
  "protocol_magnitude": 5.0,
  "radius_km": 200,
  "auto_protocol_enabled": true
}

---

# EARTHQUAKES

GET /earthquakes

GET /earthquakes/latest

GET /earthquakes/{id}

---

# EMERGENCIES

GET /emergencies

GET /emergencies/{id}

---

# SOS

POST /sos

Request

{
  "message": "Necesito ayuda"
}

Response

{
  "emergency_id": ""
}

---

# EMERGENCY STATUS

POST /emergencies/{id}/status

Request

{
  "status": "SAFE"
}

Estados

SAFE
HELP

---

# GROUP CONFIRMATION

POST /emergencies/{id}/group-confirmation

Request

{
  "status": "SAFE",
  "users": [
    "uuid1",
    "uuid2",
    "uuid3"
  ]
}

---

# LOCATIONS

POST /locations

Request

{
  "emergency_id": "",
  "latitude": 0,
  "longitude": 0,
  "accuracy": 0
}

---

GET /emergencies/{id}/locations

---

# PET STATUS

POST /pets/{id}/status

Request

{
  "emergency_id": "",
  "status": "SAFE"
}

Estados

SAFE
MISSING
INJURED
UNKNOWN

---

# DEVICE TOKENS

POST /devices/token

Request

{
  "platform": "ANDROID",
  "token": ""
}

---

DELETE /devices/token

---

# NOTIFICATIONS

GET /notifications

GET /notifications/{id}

---

# HEALTHCHECK

GET /health

Response

{
  "status": "ok"
}