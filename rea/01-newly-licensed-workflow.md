# Rea's Newly Licensed Broker Workflow

## Overview

This workflow manages outreach to newly licensed real estate brokers (AMP passers) in the Chicago area. Rea receives a monthly list and works to schedule appointments with DJ.

---

## Monthly Data Intake Process

### Step 1: Receive CSV (1st of Month)
- Rea receives email with CSV of all new AMP passers in Illinois

### Step 2: Clean Data in Google Sheets
1. Open CSV in Google Sheets
2. Remove non-Chicago agents (can't work with them)
3. De-dupe the list
4. Click **"Import to Monday"** button (Google Apps Script)

### Step 3: Auto-Import to Monday
- Google Apps Script:
  1. Final de-dupe check
  2. Creates items in "Newly Licensed" board
  3. All new leads go to **"Never Responded"** group
  4. Triggers automated SMS workflow

---

## Board Structure

### Board Name: Newly Licensed Leads

### Groups (4)

| Group | Purpose |
|-------|---------|
| **Never Responded** | Initial group for all imports - no engagement yet |
| **Responded** | Replied to SMS/email - Rea actively working |
| **Scheduled Appointments** | Appointment booked via Calendly |
| **Initially Responded, Then Disappeared** | Engaged once, then went silent |

### Statuses

| Status | Color | Description |
|--------|-------|-------------|
| New Lead | Gray | Just imported, workflow starting |
| In Workflow | Blue | Automated SMS sequence running |
| Replied | Purple | Responded to SMS/email - workflow stops |
| Attempting Contact | Orange | Rea actively calling/texting |
| Appointment Scheduled | Green | Calendly booking confirmed |
| Completed Appointment | Dark Green | Showed up - DJ takes over |
| No Show | Red | Missed appointment - needs reschedule |
| Rescheduling | Yellow | Working to reschedule after no-show |
| Chose Another Firm | Maroon | Joined competitor - hibernate 90 days |
| Lost - No Response | Dark Gray | 30 days no engagement |
| Do Not Contact | Black | Said stop/leave me alone - NEVER contact |
| Won | Green | Signed with Kale! |

---

## Workflow Stages

### Stage 1: Automated Workflow (Close CRM)

**Trigger:** Lead imported → Workflow starts

**Sequence:**
1. Day 1: SMS #1 (intro/congrats)
2. Day 3: SMS #2 (follow-up)
3. Day 5: SMS #3 (value offer)
4. Day 7: SMS #4 (final attempt)

**Auto-Stop:** The moment they reply to ANY SMS, workflow stops automatically

### Stage 2: Rea Manual Engagement

**Trigger:** Lead replies to SMS

**Process:**
1. Lead moves from "Never Responded" → **"Responded"** group
2. Status → "Replied"
3. Rea responds within 24 business hours with Calendly link
4. **If appointment scheduled:** → "Scheduled Appointments" group
5. **If no appointment within 24 hours:** Rea calls next business day

### Stage 3: Call Follow-up Sequence

**Trigger:** No appointment scheduled after Rea's Calendly SMS

**Process:**
1. Day 1: Call attempt #1
2. Day 2: Call attempt #2
3. Day 3: Call attempt #3
4. Day 4: Call attempt #4
5. Day 5: Call attempt #5
6. Day 6: Call attempt #6
7. Day 7: Call attempt #7

**After 7 days of calls with no response:**
- Status → "Lost - No Response"
- Move to → Pool of lost new agent leads (for future event invites)

### Stage 4: Appointment Handling

**Calendly Integration:**

| Event | Action |
|-------|--------|
| Appointment booked | Status → "Appointment Scheduled", Move to "Scheduled Appointments" group |
| Appointment completed | Status → "Completed Appointment", DJ takes over |
| No show | Status → "No Show", Create task for Rea to call and reschedule |

### Stage 5: Never Responded Pool

**Trigger:** Week 3 of month (or when Rea has time)

**Reminder:** System reminder to Rea: "Time to call Never Responded leads"

**Process:**
1. Rea manually calls leads in "Never Responded" group
2. Goal: Get them to answer and schedule appointment
3. **If they respond:** Move to "Responded" group
4. **If no response after 30 days from import:** Status → "Lost - No Response", add to email list for future events

---

## Special Handling

### Chose Another Firm
**Trigger:** Lead tells Rea/DJ they joined another firm

**Process:**
1. Status → "Chose Another Firm"
2. Set "Hibernation Until" → Today + 90 days
3. After 90 days: Move to special re-engagement group
4. Goal: Check in, see how new firm is going, offer Kale again

### Do Not Contact
**Trigger:** Lead says "stop", "leave me alone", "unsubscribe", etc.

**Process:**
1. Status → "Do Not Contact"
2. Check "Do Not Contact" checkbox
3. **NEVER** schedule any activity
4. **NEVER** add to event invite list
5. Remove from all automated workflows
6. Only manual status removal can re-enable (unlikely)

### Initially Responded, Then Disappeared
**Trigger:** Lead engaged at any workflow step, then stopped responding

**Criteria:**
- Had at least 1 reply/engagement
- Rea attempted follow-up
- No response to follow-up attempts

**Process:**
1. Move to "Initially Responded, Then Disappeared" group
2. Lower priority than active "Responded" leads
3. Periodic re-engagement attempts

---

## Automations Required

### Native Monday Automations

| # | Trigger | Action |
|---|---------|--------|
| 1 | Status → "Do Not Contact" | Check "Do Not Contact" checkbox |
| 2 | Status → "Chose Another Firm" | Set "Hibernation Until" to +90 days |
| 3 | Status → "Appointment Scheduled" | Move to "Scheduled Appointments" group |
| 4 | Status → "No Show" | Create task "Call to reschedule" for Rea |
| 5 | Status → "Lost - No Response" | Add to "Event Invite List" |
| 6 | Every Monday of Week 3 | Notify Rea: "Time to call Never Responded leads" |

### Make.com Automations

| # | Trigger | Action |
|---|---------|--------|
| 1 | Google Sheets button clicked | Import rows to Monday "Newly Licensed" board |
| 2 | SMS reply received (Close) | Move lead to "Responded" group, Status → "Replied" |
| 3 | Calendly appointment booked | Status → "Appointment Scheduled", Move group |
| 4 | Calendly appointment completed | Status → "Completed Appointment" |
| 5 | Calendly no-show | Status → "No Show", Create reschedule task |
| 6 | 30 days since import, still "Never Responded" | Status → "Lost - No Response" |
| 7 | "Hibernation Until" expires | Move to re-engagement group |

---

## Columns Required

### Lead Info
| Column | Type | Description |
|--------|------|-------------|
| Name | Text | Full name (First + Last) |
| First Name | Text | First name |
| Last Name | Text | Last name |
| Email | Email | Email address |
| Phone | Phone | Phone number |
| Lead Status | Status | Current workflow status |
| Lead Source | Dropdown | "AMP Passer List" |
| Lead Owner | People | Rea |

### Workflow Tracking
| Column | Type | Description |
|--------|------|-------------|
| Import Date | Date | When imported from CSV |
| Last Contact Date | Date | Last outreach attempt |
| Last Response Date | Date | Last time they responded |
| Call Attempt Count | Number | # of call attempts |
| Workflow Status | Dropdown | In Workflow / Stopped / Complete |

### Appointment
| Column | Type | Description |
|--------|------|-------------|
| Appointment Date | Date | Scheduled meeting date |
| Appointment URL | Link | Calendly/Zoom link |
| No Show Count | Number | # of missed appointments |

### Special Handling
| Column | Type | Description |
|--------|------|-------------|
| Do Not Contact | Checkbox | NEVER contact if checked |
| Hibernation Until | Date | When to re-engage |
| Chose Firm | Text | Name of firm they joined |
| Add to Event List | Checkbox | Include in future event invites |

### Notes
| Column | Type | Description |
|--------|------|-------------|
| Notes | Long Text | Activity notes |
| Current Tasks | Long Text | Auto-populated tasks |

---

## Views for Rea

| View | Filter | Sort | Purpose |
|------|--------|------|---------|
| My Day | Status = "Replied" OR "Attempting Contact" OR "Rescheduling" | Last Response Date (newest) | Daily priority queue |
| Never Responded | Group = "Never Responded" | Import Date (oldest) | Week 3 calling list |
| Scheduled Appointments | Group = "Scheduled Appointments" | Appointment Date (soonest) | Upcoming meetings |
| No Shows | Status = "No Show" | Appointment Date (newest) | Needs reschedule |
| Initially Responded | Group = "Initially Responded, Then Disappeared" | Last Response Date (oldest) | Re-engagement |
| Chose Another Firm | Status = "Chose Another Firm" | Hibernation Until (soonest) | 90-day check-ins |
| Do Not Contact | Status = "Do Not Contact" | Name (A-Z) | Reference only |
| Lost Leads | Status = "Lost - No Response" | Import Date (newest) | Event invite list |

---

## Google Apps Script: Import Button

```javascript
// Add this to Google Sheets → Extensions → Apps Script

function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('Monday Import')
    .addItem('Import to Monday', 'importToMonday')
    .addToUi();
}

function importToMonday() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  const headers = data[0];

  // De-dupe by email
  const seen = new Set();
  const uniqueRows = [];

  for (let i = 1; i < data.length; i++) {
    const email = data[i][headers.indexOf('Email')];
    if (email && !seen.has(email.toLowerCase())) {
      seen.add(email.toLowerCase());
      uniqueRows.push(data[i]);
    }
  }

  // Send to Make.com webhook
  const webhookUrl = 'YOUR_MAKE_WEBHOOK_URL';

  const payload = {
    leads: uniqueRows.map(row => ({
      firstName: row[headers.indexOf('First Name')],
      lastName: row[headers.indexOf('Last Name')],
      email: row[headers.indexOf('Email')],
      phone: row[headers.indexOf('Phone')],
      leadSource: 'AMP Passer List',
      importDate: new Date().toISOString()
    }))
  };

  const options = {
    method: 'post',
    contentType: 'application/json',
    payload: JSON.stringify(payload)
  };

  try {
    UrlFetchApp.fetch(webhookUrl, options);
    SpreadsheetApp.getUi().alert(
      'Success!',
      `Imported ${uniqueRows.length} leads to Monday.com (${data.length - 1 - uniqueRows.length} duplicates removed)`,
      SpreadsheetApp.getUi().ButtonSet.OK
    );
  } catch (error) {
    SpreadsheetApp.getUi().alert('Error', 'Failed to import: ' + error.message, SpreadsheetApp.getUi().ButtonSet.OK);
  }
}
```

---

## Integration Points

### Close CRM
- Automated SMS workflow
- Reply detection → triggers workflow stop
- Sync lead status to Monday

### Calendly
- Appointment booked → Monday status update
- Appointment completed → Monday status update
- No show → Monday status + task creation

### Google Sheets
- Import button → Make.com webhook → Monday board

### Monday CRM
- New contacts created from Newly Licensed board
- Link to CRM Contacts for master database

---

## Timeline Summary

| Day | Action |
|-----|--------|
| 1 | Import leads, automated workflow starts |
| 1-7 | Automated SMS sequence |
| On Reply | Workflow stops, Rea responds within 24 hrs |
| +1 day after reply | If no appointment, Rea calls |
| +1 week | If still no appointment after daily calls → Lost |
| Week 3 | Rea calls "Never Responded" pool |
| Day 30 | "Never Responded" → "Lost - No Response" |
| Day 90 | "Chose Another Firm" → Re-engagement |
