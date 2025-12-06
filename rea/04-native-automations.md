# Native Monday Automations - Newly Licensed Leads Board

These automations should be set up directly in Monday.com (Newly Licensed Leads board → Automate tab).

---

## Automation 1: Do Not Contact Setup

**When:** Status changes to "Do Not Contact"

**Then:**
1. Check "Do Not Contact" checkbox
2. Move item to archived group (optional)

---

## Automation 2: Chose Another Firm - Hibernation

**When:** Status changes to "Chose Another Firm"

**Then:**
1. Set "Hibernation Until" to today + 90 days
2. Check "Do Not Contact" (temporary - prevents outreach during hibernation)

---

## Automation 3: Appointment Scheduled - Move Group

**When:** Status changes to "Appointment Scheduled"

**Then:**
1. Move item to "Scheduled Appointments" group

---

## Automation 4: No Show - Create Reschedule Task

**When:** Status changes to "No Show"

**Then:**
1. Increment "No Show Count" by 1
2. Create notification/task for Rea: "Call {item name} to reschedule"
3. Update "Current Tasks" with "Call to reschedule - no show"

---

## Automation 5: Lost - Add to Event List

**When:** Status changes to "Lost - No Response"

**Then:**
1. Check "Add to Event List" checkbox

---

## Automation 6: Week 3 Reminder (Scheduled)

**When:** Every Monday at 9:00 AM (Week 3 of month)

**Then:**
1. Notify Rea: "Time to call Never Responded leads!"

**Note:** Monday.com's native scheduling may not support "Week 3 of month" logic. May need Make.com for this.

---

## Automation 7: Replied - Move to Responded Group

**When:** Status changes to "Replied"

**Then:**
1. Move item to "Responded" group
2. Set "Workflow Status" to "Stopped"

---

## Automation 8: Completed Appointment Notification

**When:** Status changes to "Completed Appointment"

**Then:**
1. Notify DJ: "{item name} completed their appointment - ready for your follow-up!"

---

## Automation 9: Won Celebration

**When:** Status changes to "Won"

**Then:**
1. Send notification (Slack/Email): "🎉 {item name} just signed with Kale Realty!"

---

## Make.com Automations Required

The following automations require Make.com due to complexity:

| # | Trigger | Action |
|---|---------|--------|
| 1 | Google Sheets button clicked | Import rows to Monday "Newly Licensed" board |
| 2 | SMS reply received (Close CRM) | Move lead to "Responded" group, Status → "Replied" |
| 3 | Calendly appointment booked | Status → "Appointment Scheduled", Move to group |
| 4 | Calendly appointment completed | Status → "Completed Appointment" |
| 5 | Calendly no-show detected | Status → "No Show", Increment No Show Count |
| 6 | 30 days since import, still "Never Responded" | Status → "Lost - No Response" |
| 7 | "Hibernation Until" date expires | Status → "New Lead" (for re-engagement), Uncheck "Do Not Contact" |
| 8 | Lead imported to Monday | Create lead in Close CRM, Start "New Amp Passer Leads" workflow |

---

## Close CRM Workflow Reference

The "New Amp Passer Leads" workflow in Close CRM has 12 steps:

| Day | Type | Description |
|-----|------|-------------|
| 0 | SMS | Initial outreach |
| 1 | SMS | Follow-up SMS |
| 1 | Email | Follow-up email |
| 3 | Email | Value proposition email |
| 3 | SMS | Check-in SMS |
| 5 | Email | Continue engagement |
| 6 | Email | Building relationship |
| 7 | Email | Week 1 wrap-up |
| 8 | Email | Week 2 start |
| 9 | Email | Continue nurture |
| 30 | SMS | Final SMS attempt |
| - | Lead Update | Mark workflow complete |

**Auto-Stop:** When lead replies to ANY message, workflow stops automatically in Close CRM.

---

## Column Reference (After Board Creation)

| Column | Expected ID Pattern | Type |
|--------|---------------------|------|
| Lead Status | `status` | status |
| Do Not Contact | `checkbox_xxxxx` | checkbox |
| Hibernation Until | `date_xxxxx` | date |
| Add to Event List | `checkbox_xxxxx` | checkbox |
| No Show Count | `numbers_xxxxx` | number |
| Workflow Status | `dropdown_xxxxx` | dropdown |
| Current Tasks | `long_text_xxxxx` | long text |

*Note: Replace `xxxxx` with actual column IDs after board creation.*
