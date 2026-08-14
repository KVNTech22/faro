# FARO - Emergency Engine Design

Version: 1.0

Status: Approved

---

# Objective

Coordinate family and trusted contacts during emergencies.

The Emergency Engine is the core feature of FARO.

Its purpose is to:

- Detect emergency situations.
- Notify affected users.
- Collect status confirmations.
- Escalate when a user does not respond.
- Share relevant emergency information with authorized people.

---

# Emergency Triggers

Supported in MVP:

1. Earthquake Detection
2. Manual SOS

Future Versions:

- Severe weather alerts
- Flood alerts
- Landslide alerts
- Personal safety alerts

---

# Emergency States

A user can be in one of the following states:

## SAFE

User confirms they are safe.

Response visible to:

- Circle members
- Trusted contacts

---

## HELP

User confirms they need assistance.

Response visible to:

- Circle members
- Trusted contacts

Priority:

HIGH

---

## UNCONFIRMED

User has not responded within the configured time.

Default timeout:

5 minutes

Priority:

HIGH

---

## HIGH_RISK

User remains unconfirmed after escalation.

Default timeout:

15 minutes

Priority:

CRITICAL

---

# Emergency Flow

Earthquake or SOS

↓

Notification sent

↓

User chooses:

SAFE
or
HELP

↓

If no response after 5 minutes

↓

UNCONFIRMED

↓

Notify circle members

↓

If no response after 15 minutes

↓

HIGH_RISK

↓

Notify:

- Circle members
- Trusted contacts

---

# Earthquake Events

Sources:

- Servicio Geológico Colombiano (SGC)
- USGS
- EMSC

Events are normalized before processing.

---

# Earthquake Filters

Each user can configure their own earthquake alert preferences.

## Default Configuration

Magnitude:

3.0+

Scope:

Regional

---

## Minimum Magnitude

Range:

2.0 to 10.0

Examples:

- 2.0+
- 3.0+
- 4.0+
- 5.0+

Purpose:

Reduce unnecessary notifications for low-impact earthquakes.

---

## Geographic Scope

Options:

- Local
- Regional
- National
- Continental
- Worldwide

Purpose:

Allow users to receive alerts only from areas relevant to them.
---

## Emergency Override

During a major earthquake event, FARO may override user filters.

Conditions:

- Magnitude 6.5+
- Official high-impact event

Purpose:

Ensure users receive critical alerts even when their configured filters would normally suppress the notification.

# SOS Manual

Users can manually activate an emergency.

Button:

SOS

Confirmation required:

YES

Purpose:

Prevent accidental activations.

---

# Location Sharing

Enabled only during active emergencies.

Location is never shared continuously.

---

# Location Collection

Triggers:

- Earthquake Event
- SOS Event

Data:

- Latitude
- Longitude
- Timestamp

---

# Offline Location Queue

If internet is unavailable:

Store locally.

Send automatically when connection returns.

---

# Trusted Contacts

Users may define external trusted contacts.

Examples:

- Parents
- Siblings
- Friends
- Neighbors

Trusted contacts may receive:

- Emergency status
- Location links
- Escalation alerts

---

# Family Circles

A user may belong to multiple circles.

Examples:

- Family
- Partner Family
- Friends

Emergency notifications are sent to all relevant circles.

---

# Emergency Cards

Each user has an emergency profile.

Visible during emergencies.

Contains:

- Blood Type
- Allergies
- Medications
- Disabilities
- Medical Notes

---

# Pet Emergency Cards

Users may register pets.

Fields:

- Name
- Species
- Breed
- Age
- Medical Conditions
- Notes

Multiple pets supported.

---

# Quick Actions

During emergencies users can:

- Call member
- Open WhatsApp chat
- Open Google Maps location

One tap access.

---

# Escalation Notifications

MVP:

- Push Notifications

Future:

- Email
- WhatsApp
- SMS

---

# Emergency Closure

An emergency is closed when:

- User responds SAFE
- User responds HELP
- Circle owner closes event
- System closes inactive event after 60 minutes

---

# Privacy Rules

Location sharing only during emergencies.

No continuous tracking.

No background monitoring outside emergency events.

---

# Future Versions

V2

- WhatsApp integration
- SMS fallback
- Emergency reports

V3

- AI emergency recommendations
- Disaster prediction integrations
- Community emergency networks

---

# Approved Decisions

Response Timeout:

5 minutes

High Risk Timeout:

15 minutes

Automatic Closure:

60 minutes

Location Sharing:

Emergency only

Tracking:

Disabled outside emergencies

Status:

Accepted