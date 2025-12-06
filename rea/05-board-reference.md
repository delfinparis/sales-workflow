# Newly Licensed Leads Board - Reference

## Board Info
- **Board Name:** Newly Licensed Leads
- **Board ID:** 18391158354
- **Workspace:** CRM

---

## Groups

| Group | ID |
|-------|-----|
| Never Responded | group_mkyb6hgy |
| Responded | group_mkyb51b6 |
| Scheduled Appointments | group_mkybxtds |
| Initially Responded, Then Disappeared | group_mkyb64mg |

---

## Columns

### Lead Info
| Column | ID | Type |
|--------|-----|------|
| Name | name | name |
| First Name | text_mkybe1vc | text |
| Last Name | text_mkyb85z9 | text |
| Email | email_mkybfqax | email |
| Phone | phone_mkyb4cr0 | phone |
| Lead Owner | multiple_person_mkyb4wzn | people |

### Workflow Tracking
| Column | ID | Type |
|--------|-----|------|
| Import Date | date_mkybk1hp | date |
| Last Contact Date | date_mkyb95b | date |
| Last Response Date | date_mkybnadc | date |
| Call Attempt Count | numeric_mkybkv6z | numbers |
| Close CRM Lead ID | text_mkyb1a5v | text |

### Appointment
| Column | ID | Type |
|--------|-----|------|
| Appointment Date | date_mkyb9hr1 | date |
| Appointment URL | link_mkybkpnj | link |
| No Show Count | numeric_mkybzb1j | numbers |

### Special Handling
| Column | ID | Type |
|--------|-----|------|
| Do Not Contact | boolean_mkyb12v8 | checkbox |
| Hibernation Until | date_mkyb1317 | date |
| Chose Firm | text_mkybb8mk | text |
| Add to Event List | boolean_mkybat8 | checkbox |

### Notes
| Column | ID | Type |
|--------|-----|------|
| Notes | long_text_mkybev5j | long_text |

### Status
| Column | ID | Type |
|--------|-----|------|
| Lead Status | color_mkybxbyk | status |

---

## Status Labels

| Index | Label | Color |
|-------|-------|-------|
| 5 | New Lead | Gray |
| 1 | In Workflow | Blue |
| 0 | Replied | Purple |
| 2 | Attempting Contact | Orange |
| 3 | Appointment Scheduled | Dark Green |
| 4 | Completed Appointment | Eden (Teal) |
| 6 | No Show | Red |
| 7 | Rescheduling | Yellow |
| 8 | Chose Another Firm | Brown |
| 9 | Lost - No Response | Dark Gray |
| 10 | Do Not Contact | Black |
| 11 | Won | Lime Green |

---

## Integration IDs

### Close CRM
- **Workflow Name:** New Amp Passer Leads
- **Sequence ID:** `seq_7TUbe0qzdkzDqHMTy63BMb`
- **API Key:** See `06-close-crm-workflow-reference.md`

### Calendly
- **Event Type:** (to be configured)
- **Schedule Link:** https://joinkale.com/schedule

### Google Sheets
- **Webhook URL:** (to be created in Make.com - see `rea/make/01-google-sheets-import.json`)

---

## Make.com Scenarios

| # | Scenario | File |
|---|----------|------|
| 1 | Google Sheets Import | `rea/make/01-google-sheets-import.json` |
| 2 | Close SMS Reply Received | `rea/make/02-close-sms-reply-received.json` |
| 3 | Calendly Appointment Booked | `rea/make/03-calendly-appointment-booked.json` |
| 4 | Calendly Appointment Completed | `rea/make/04-calendly-appointment-completed.json` |
| 5 | Calendly No Show | `rea/make/05-calendly-no-show.json` |
| 6 | 30-Day Timeout Check | `rea/make/06-thirty-day-timeout.json` |
| 7 | Hibernation Expiration | `rea/make/07-hibernation-expiration.json` |
| 8 | Week 3 Calling Reminder | `rea/make/08-week-three-calling-reminder.json` |
