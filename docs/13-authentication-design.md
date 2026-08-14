# FARO - Authentication Design

Version: 1.0

Status: Approved

---

# Objective

Provide secure authentication for FARO users using:

- Email + Password
- Google Sign-In

The system must support future expansion to:

- WhatsApp notifications
- SMS notifications
- Trusted contacts
- Emergency communications

---

# Authentication Methods

Supported:

1. Email + Password
2. Google Sign-In

Both methods are valid and can coexist.

---

# User Identification

Primary Identifier:

email

Unique Constraints:

- email
- phone

---

# Password Security

Algorithm:

Argon2id

Rules:

- Minimum length: 8
- At least one uppercase letter
- At least one lowercase letter
- At least one number

Passwords are never stored in plain text.

---

# JWT Configuration

Access Token:

- Expiration: 15 minutes

Refresh Token:

- Expiration: 30 days

Token Type:

Bearer

---

# Refresh Token Security

Refresh tokens must:

- Be stored hashed in database
- Be revocable
- Be invalidated on logout

Refresh tokens must never be stored in plain text.

---

# Email Verification

Required:

YES

New users must verify email before accessing emergency features.

Fields:

email_verified BOOLEAN

Default:

FALSE

---

# Phone Verification

Required:

NOT IN MVP

Planned:

V2

Field:

phone_verified BOOLEAN

Default:

FALSE

Phone remains mandatory during registration.

---

# Required Registration Fields

- Full Name
- Email
- Password
- Phone Number

---

# Google Sign-In

Provider:

Google Identity Services

Stored Data:

google_id

Rules:

- Email must be verified by Google.
- If email already exists, accounts are linked.
- No duplicate users allowed.

---

# Password Recovery

Supported:

YES

Flow:

1. User requests recovery.
2. Recovery email sent.
3. User receives temporary token.
4. User sets new password.

Recovery tokens:

- Single use
- Expire after 15 minutes

---

# User Status

Field:

is_active BOOLEAN

Default:

TRUE

Purpose:

Allow account suspension without deleting user data.

---

# Login Tracking

Field:

last_login_at TIMESTAMP

Updated:

Every successful login.

---

# Future Authentication Features

Planned V2:

- Phone verification
- WhatsApp verification
- Two-Factor Authentication (2FA)

Planned V3:

- Emergency trusted device recognition
- Biometric login

---

# Security Rules

Forbidden:

- Plain text passwords
- Plain text refresh tokens
- Hardcoded secrets
- Shared accounts

Mandatory:

- HTTPS
- JWT validation
- Token expiration
- Input validation
- Rate limiting

---

# Approved Decisions

Authentication Strategy:

Email + Password + Google Sign-In

Password Hash:

Argon2id

Access Token:

15 minutes

Refresh Token:

30 days

Email Verification:

Required

Phone:

Mandatory

Phone Verification:

Future Version

Status:

Accepted

# Emergency Access Rules

Users can receive emergency notifications even if:

- Email is not verified

Users cannot:

- Create circles
- Invite members
- Manage dependents
- Configure emergency settings

until email verification is completed.