# Native Monday Automations

These automations should be set up directly in Monday.com (Superlative Leads board → Automate tab).

---

## Board Reference

**Board:** Superlative Leads (ID: 18390370563)

---

## Automation 1: 30-Day Timeout Setup

**When:** Status changes to "30-Day Timeout"

**Then:**
1. Set "Timeout Until" to today + 30 days
2. Check "Do Not Contact"

---

## Automation 2: Hibernation Setup

**When:** Status changes to "Hibernation 90-Day"

**Then:**
1. Set "Hibernation Until" to today + 90 days
2. Check "Do Not Contact"

---

## Automation 3: Dead Lead Setup

**When:** Status changes to "Dead - Negative Reply"

**Then:**
1. Set "Dead Until" to today + 365 days
2. Check "Do Not Contact"

---

## Automation 4: Return to Pool

**When:** Status changes to "New Lead"

**Then:**
1. Uncheck "Do Not Contact"

---

## Automation 5: Won Notification

**When:** Status changes to "Won"

**Then:**
1. Send notification (Slack or Email): "{item name} just signed with Kale Realty!"

---

## Automation 6: Timeout Return (Scheduled)

**When:** Every day at 8:00 AM

**If:** "Timeout Until" is before today AND Status is "30-Day Timeout"

**Then:**
1. Change Status to "New Lead"
2. Increment "Timeout Count" by 1

**Note:** If "Timeout Count" reaches 3, may need separate logic to move to Hibernation instead.

---

## Automation 7: Hibernation Return (Scheduled)

**When:** Every day at 8:00 AM

**If:** "Hibernation Until" is before today AND Status is "Hibernation 90-Day"

**Then:**
1. Change Status to "New Lead"

---

## Automation 8: No Reply → Timeout

**When:** Every day at 8:00 AM

**If:** Status is "SMS Sent" AND "Last Contact Date" is more than 7 days ago

**Then:**
1. Change Status to "30-Day Timeout"

---

## Column Reference

| Column | ID | Type |
|--------|-----|------|
| Status | `status` | status |
| Do Not Contact | `boolean_mky6sedx` | checkbox |
| Timeout Until | `date_mky69mew` | date |
| Timeout Count | `numeric_mky6c75r` | number |
| Hibernation Until | `date_mky68ca2` | date |
| Dead Until | `date_mky68q9y` | date |
| Last Contact Date | `date_mky6fwh8` | date |

---

## Notes

- Automations 6, 7, 8 are scheduled/recurring and may require Make.com if Monday's native scheduling doesn't support the logic
- Test each automation with a sample item before going live
- The "Timeout Count" increment may need Make.com for proper number incrementing
