# Make.com Automations - Batch 2

**Board ID:** `18390370563` (Superlative Leads)

---

## API Credentials & User IDs

### Monday.com API
```
API Token: eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzMDE5NDQxNywiYWFpIjoxMSwidWlkIjoxMDk5MzEwNywiaWFkIjoiMjAyNC0wMy0wN1QyMTo1MDoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NDk2MDA1OSwicmduIjoidXNlMSJ9.m3bCdQF0HwlTYrLQy4-fbTtv04A8RPxzTsWeTsGHFfI
API URL: https://api.monday.com/v2
```

### User IDs (for person column assignments)
| Name | Email | User ID |
|------|-------|---------|
| **Ana (Anaya Dada)** | anaya@kalerealty.com | `97053956` |
| D.J. Paris | dj@kalerealty.com | `10993107` |
| Jennica Mercedes Abiera | jennica.abiera@gmail.com | `96623424` |
| Rea Endaya | rea@kalerealty.com | `10995945` |

### Board IDs
| Board | ID |
|-------|-----|
| Superlative Leads (main) | `18390370563` |
| REA Newly Licensed Leads | `18391158354` |
| JustCall Contacts | *(created by JustCall integration)* |
| JustCall Calls | `18387583881` |
| JustCall SMS | `18387583880` |

### Instantly API (Cold Email)
```
API URL: https://api.instantly.ai/api/v2
Authorization: Bearer Mzg0NjFkOGUtYTljZC00N2Y3LThmZTAtOTJjMWMzZDNjYWU2OnlhaXBod0dCWVZDcA==
```

**Webhook Setup (for lead_interested events):**
```json
POST https://api.instantly.ai/api/v2/webhooks
Headers:
  Authorization: Bearer Mzg0NjFkOGUtYTljZC00N2Y3LThmZTAtOTJjMWMzZDNjYWU2OnlhaXBod0dCWVZDcA==
  Content-Type: application/json
Body:
  {
    "target_hook_url": "YOUR_MAKE_WEBHOOK_URL",
    "event_type": "lead_interested"
  }
```

### JustCall API (SMS)
```
API URL: https://api.justcall.io/v1
API Key: a0de455c4755393df988913e1303804c91bc67e3
API Secret: 962e2b2b3b45d0b47ae3b1f7a22dded09cf575c6
```

**For Make.com HTTP modules:**
```
Authorization: Bearer a0de455c4755393df988913e1303804c91bc67e3:962e2b2b3b45d0b47ae3b1f7a22dded09cf575c6
```

**Send SMS endpoint:**
```
POST https://api.justcall.io/v1/texts/new
```

---

## Already Completed ✅

| # | Scenario |
|---|----------|
| 1 | Auto-Create Contact on New Lead |
| 2 | Create Deal on Won Status |
| 3 | Duplicate Detection |
| 4 | Sync Contact Updates |
| 5 | Link Brokerage to Account |

**Native Monday (also done):**
- Temperature Auto-Update (13 rules)
- Stage Entry Date
- First Contact Date
- 12 notification/date automations

---

## Column Reference (All New Columns)

### Speed-to-Lead
| Column | ID | Type |
|--------|-----|------|
| Reply Received At | `date_mkyc9xa8` | Date |
| First Response At | `date_mkycjb4b` | Date |
| Response Time Mins | `numeric_mkycpyr8` | Number |

### Ghost Prevention
| Column | ID | Type |
|--------|-----|------|
| Ghost Risk | `color_mkyc52cw` | Status (Low/Medium/High/Ghosted) |
| Last Meaningful Reply | `date_mkyctpv2` | Date |
| Re-engagement Attempts | `numeric_mkyc534x` | Number |

### Lead Scoring
| Column | ID | Type |
|--------|-----|------|
| Lead Score | `numeric_mkycbffy` | Number (0-100) |
| Pain Signals | `numeric_mkycmf31` | Number |

### Pipeline Velocity
| Column | ID | Type |
|--------|-----|------|
| Days In Stage | `numeric_mkycxytk` | Number |
| Total Days in Pipeline | `numeric_mkycf1d6` | Number |

### Competitive Intelligence
| Column | ID | Type |
|--------|-----|------|
| Competitor Name | `color_mkyc4rpk` | Status |
| Win-Back Date | `date_mkyct9n3` | Date |

### Referral Tracking
| Column | ID | Type |
|--------|-----|------|
| Referral Source | `color_mkych05` | Status |
| Lead Source (existing) | `dropdown_mky6ctrz` | Dropdown |

---

## BATCH 1: Core Tracking (3 Scenarios)

### Scenario 6: Capture Reply Time

**Trigger:** Status changes to "Replied - Awaiting Ana"

**Action:** Set Reply Received At to current timestamp

```json
{
  "name": "Capture Reply Timestamp",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status",
    "value": "Replied - Awaiting Ana"
  },
  "actions": [
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "date_mkyc9xa8": {
          "date": "{{now | date: 'YYYY-MM-DD'}}",
          "time": "{{now | date: 'HH:mm:ss'}}"
        },
        "date_mkyctpv2": {
          "date": "{{now | date: 'YYYY-MM-DD'}}"
        }
      }
    }
  ]
}
```

---

### Scenario 7: Calculate Response Time

**Trigger:** Status changes to "Ana Engaged" (from "Replied - Awaiting Ana")

**Action:** Set First Response At + calculate Response Time Mins

```json
{
  "name": "Calculate Response Time",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status",
    "value": "Ana Engaged"
  },
  "actions": [
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "columns": ["date_mkyc9xa8"]
    },
    {
      "module": "tools.calculate",
      "note": "Calculate minutes between reply and response",
      "formula": "ROUND((NOW - reply_received_at) / 60000)"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "date_mkycjb4b": {
          "date": "{{now | date: 'YYYY-MM-DD'}}",
          "time": "{{now | date: 'HH:mm:ss'}}"
        },
        "numeric_mkycpyr8": "{{response_time_mins}}"
      }
    }
  ]
}
```

---

### Scenario 8: Ghost Risk Detection (DAILY)

**Trigger:** Schedule - Daily at 8:00 AM

**Action:** For all active leads, update Ghost Risk based on days since Last Meaningful Reply

**Logic:**
| Days Since Reply | Ghost Risk |
|------------------|------------|
| 0-3 days | Low |
| 4-7 days | Medium |
| 8-14 days | High |
| 15+ days | Ghosted |

```json
{
  "name": "Update Ghost Risk (Daily)",
  "trigger": {
    "module": "schedule",
    "interval": "daily",
    "time": "08:00"
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "note": "Get all leads in active statuses",
      "query": {
        "rules": [
          {
            "column_id": "status",
            "compare_value": ["Ana Engaged", "Tool Offered", "Training Invited", "Relationship Building", "Ask Made"]
          }
        ]
      }
    },
    {
      "module": "iterator",
      "array": "{{items}}"
    },
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "columns": ["date_mkyctpv2"]
    },
    {
      "module": "tools.calculate",
      "formula": "FLOOR((NOW - last_meaningful_reply) / 86400000)"
    },
    {
      "module": "tools.switch",
      "value": "{{days_since_reply}}",
      "cases": [
        {"condition": "days <= 3", "result": "Low"},
        {"condition": "days <= 7", "result": "Medium"},
        {"condition": "days <= 14", "result": "High"},
        {"condition": "days > 14", "result": "Ghosted"}
      ]
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "column_values": {
        "color_mkyc52cw": {
          "label": "{{ghost_risk}}"
        }
      }
    }
  ]
}
```

---

## BATCH 2: Scoring & Velocity (3 Scenarios)

### Scenario 9: Calculate Lead Score

**Trigger:** Status, Temperature, or Pain Signals changes

**Action:** Calculate lead score (0-100) and update

**Scoring Logic:**
| Status | Base Points |
|--------|-------------|
| SMS Sent | 5 |
| Replied | 20 |
| Ana Engaged | 30 |
| Tool Offered | 45 |
| Training Invited | 50 |
| Relationship Building | 60 |
| Ask Made | 75 |
| Meeting Scheduled | 90 |
| Won | 100 |

| Temperature | Bonus |
|-------------|-------|
| Cold | +0 |
| Warm | +5 |
| Hot | +10 |

| Pain Signals | Bonus |
|--------------|-------|
| Each signal | +3 |

```json
{
  "name": "Calculate Lead Score",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "columns": ["status", "color_mkyce0h5", "numeric_mkycmf31"]
  },
  "actions": [
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "columns": ["status", "color_mkyce0h5", "numeric_mkycmf31"]
    },
    {
      "module": "tools.switch",
      "name": "status_points",
      "value": "{{status}}",
      "cases": [
        {"pattern": "New Lead", "result": 0},
        {"pattern": "SMS Sent", "result": 5},
        {"pattern": "Replied.*", "result": 20},
        {"pattern": "Ana Engaged", "result": 30},
        {"pattern": "Tool Offered", "result": 45},
        {"pattern": "Training Invited", "result": 50},
        {"pattern": "Relationship Building", "result": 60},
        {"pattern": "Ask Made", "result": 75},
        {"pattern": "Meeting Scheduled", "result": 90},
        {"pattern": "DJ Meeting Complete", "result": 95},
        {"pattern": "Offer Extended", "result": 98},
        {"pattern": "Won", "result": 100}
      ],
      "default": 0
    },
    {
      "module": "tools.switch",
      "name": "temp_points",
      "value": "{{temperature}}",
      "cases": [
        {"pattern": "Cold", "result": 0},
        {"pattern": "Warm", "result": 5},
        {"pattern": "Hot", "result": 10}
      ],
      "default": 0
    },
    {
      "module": "tools.calculate",
      "formula": "MIN(100, status_points + temp_points + (pain_signals * 3))"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "numeric_mkycbffy": "{{total_score}}"
      }
    }
  ]
}
```

---

### Scenario 10: Days In Stage Update (DAILY)

**Trigger:** Schedule - Daily at 6:00 AM

**Action:** For all active leads, calculate days since Stage Entry Date

```json
{
  "name": "Update Days In Stage (Daily)",
  "trigger": {
    "module": "schedule",
    "interval": "daily",
    "time": "06:00"
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "note": "Get all non-closed leads",
      "query": {
        "rules": [
          {
            "column_id": "status",
            "compare_value_not": ["Won", "Lost - Not Interested", "Lost - Competitor", "Lost - Not Qualified", "Dead - Negative Reply"]
          }
        ]
      }
    },
    {
      "module": "iterator",
      "array": "{{items}}"
    },
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "columns": ["date_mkyck8r9"]
    },
    {
      "module": "tools.calculate",
      "formula": "FLOOR((NOW - stage_entry_date) / 86400000)"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "column_values": {
        "numeric_mkycxytk": "{{days_in_stage}}"
      }
    }
  ]
}
```

---

### Scenario 11: Calculate Total Days on Close

**Trigger:** Status changes to Won, Lost, or Dead

**Action:** Calculate Total Days in Pipeline from First Contact Date

```json
{
  "name": "Calculate Total Pipeline Days",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status",
    "value": ["Won", "Lost - Not Interested", "Lost - Competitor", "Lost - Not Qualified", "Dead - Negative Reply"]
  },
  "actions": [
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "columns": ["date_mkycg4ew"]
    },
    {
      "module": "tools.calculate",
      "formula": "FLOOR((NOW - first_contact_date) / 86400000)"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "numeric_mkycf1d6": "{{total_days}}"
      }
    }
  ]
}
```

---

## BATCH 3: Win-Back & Misc (4 Scenarios)

### Scenario 12: Set Win-Back Date

**Trigger:** Competitor Name is set

**Action:** Set Win-Back Date to today + 90 days

```json
{
  "name": "Set Win-Back Date",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "color_mkyc4rpk"
  },
  "actions": [
    {
      "module": "tools.dateAdd",
      "date": "{{now}}",
      "amount": 90,
      "unit": "days"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "date_mkyct9n3": {
          "date": "{{win_back_date | date: 'YYYY-MM-DD'}}"
        }
      }
    }
  ]
}
```

---

### Scenario 13: Win-Back Reminder (DAILY)

**Trigger:** Schedule - Daily at 9:00 AM

**Action:** Find leads where Win-Back Date = today, create notification

```json
{
  "name": "Win-Back Reminder (Daily)",
  "trigger": {
    "module": "schedule",
    "interval": "daily",
    "time": "09:00"
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "query": {
        "rules": [
          {
            "column_id": "date_mkyct9n3",
            "compare_value": "{{TODAY}}"
          }
        ]
      }
    },
    {
      "module": "iterator",
      "array": "{{items}}"
    },
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "columns": ["name", "color_mkyc4rpk"]
    },
    {
      "module": "monday.createUpdate",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "body": "🔔 WIN-BACK REMINDER: It's been 90 days since this lead went to {{competitor_name}}. Time to check in!"
    },
    {
      "module": "slack.sendMessage",
      "channel": "#leads",
      "message": "🔔 *Win-Back Reminder*\n\n*Lead:* {{name}}\n*Went to:* {{competitor_name}}\n*90 days ago* - Time to reach out and check in!"
    }
  ]
}
```

---

### Scenario 14: Re-engagement Counter

**Trigger:** Update/note added to item containing re-engagement keywords

**Keywords:** "re-engage", "follow up", "checking in", "ping", "reaching out again"

**Action:** Increment Re-engagement Attempts by 1

```json
{
  "name": "Increment Re-engagement Counter",
  "trigger": {
    "module": "monday.watchUpdates",
    "board_id": 18390370563
  },
  "actions": [
    {
      "module": "tools.textParser",
      "input": "{{update_body}}",
      "pattern": "(re-?engage|follow.?up|checking in|ping|reaching out again)",
      "case_insensitive": true
    },
    {
      "module": "filter",
      "condition": "{{pattern_matched}} = true"
    },
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{item_id}}",
      "columns": ["numeric_mkyc534x"]
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{item_id}}",
      "column_values": {
        "numeric_mkyc534x": "{{re_engagement_attempts + 1}}"
      }
    }
  ]
}
```

---

### Scenario 15: Auto-Set Referral Source

**Trigger:** New item created

**Action:** Based on Lead Source dropdown, set Referral Source status

**Mapping:**
| Lead Source | → Referral Source |
|-------------|-------------------|
| Courted | Courted.ai Superlative |
| Event | Event/Training |
| Website | Website |
| Referral | Agent Referral |
| (other) | Other |

```json
{
  "name": "Auto-Set Referral Source",
  "trigger": {
    "module": "monday.watchItems",
    "board_id": 18390370563,
    "event": "create"
  },
  "actions": [
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "columns": ["dropdown_mky6ctrz"]
    },
    {
      "module": "tools.switch",
      "value": "{{lead_source}}",
      "cases": [
        {"pattern": "Courted", "result": "Courted.ai Superlative"},
        {"pattern": "Event", "result": "Event/Training"},
        {"pattern": "Website", "result": "Website"},
        {"pattern": "Referral", "result": "Agent Referral"}
      ],
      "default": "Other"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "color_mkych05": {
          "label": "{{referral_source}}"
        }
      }
    }
  ]
}
```

---

## Summary: All 21 Make.com Scenarios

### Completed ✅
| # | Name | Type |
|---|------|------|
| 1 | Auto-Create Contact on New Lead | Event |
| 2 | Create Deal on Won Status | Event |
| 3 | Duplicate Detection | Event |
| 4 | Sync Contact Updates | Event |
| 5 | Link Brokerage to Account | Event |

### To Build 🔨
| # | Name | Type | Priority |
|---|------|------|----------|
| 6 | Capture Reply Time | Event | Batch 1 |
| 7 | Calculate Response Time | Event | Batch 1 |
| 8 | Ghost Risk Detection | Daily | Batch 1 |
| 9 | Calculate Lead Score | Event | Batch 2 |
| 10 | Days In Stage Update | Daily | Batch 2 |
| 11 | Calculate Total Days on Close | Event | Batch 2 |
| 12 | Set Win-Back Date | Event | Batch 3 |
| 13 | Win-Back Reminder | Daily | Batch 3 |
| 14 | Re-engagement Counter | Event | Batch 3 |
| 15 | Auto-Set Referral Source | Event | Batch 3 |
| 16 | Gmail Meeting Notes (Gemini) | Event | Batch 4 |
| 17 | Instantly Cold Email Response | Event | Batch 5 |
| 18 | Kale Roster → Won Sync | Daily | Batch 6 |
| 19 | Former Agent Win-Back SMS | Daily (GitHub) | Batch 7 |
| 20 | Former Agent Win-Back Email | Daily (Make) | Batch 7 |
| 21 | REA Google Sheets Import | Event (Webhook) | Batch 8 |

---

## BATCH 4: Integrations (1 Scenario)

### Scenario 16: Gmail → Monday Meeting Notes (Gemini)

**Purpose:** Automatically capture Google Gemini meeting notes from Gmail and post them as updates on the corresponding Monday.com lead.

**Gmail Account:** `dj@kalerealty.com`

**Trigger:** Gmail - Watch Emails
- **Connect DJ's Gmail:** `dj@kalerealty.com`
- Filter: From `noreply@google.com` AND subject contains "Meeting notes"
- Folder: Inbox (or create a label filter for organization)

**Flow:**
```
Gmail Email Arrives → Parse Attendee Email → Search Monday Board → Create Update
```

**Make.com Scenario:**

```json
{
  "name": "Gmail Meeting Notes to Monday",
  "trigger": {
    "module": "gmail.watchEmails",
    "connection": "dj@kalerealty.com",
    "folder": "INBOX",
    "criteria": {
      "from": "noreply@google.com",
      "subject": "Meeting notes"
    },
    "markAsRead": true
  },
  "actions": [
    {
      "module": "tools.textParser",
      "name": "Extract Attendee Email",
      "note": "Parse the meeting notes body to find attendee email addresses",
      "input": "{{email_body}}",
      "pattern": "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}",
      "match_all": true
    },
    {
      "module": "filter",
      "note": "Only continue if we found at least one non-kale email (external attendee)",
      "condition": "{{attendee_emails | filter: 'not contains \"@kalerealty.com\"' | length}} > 0"
    },
    {
      "module": "tools.setVariable",
      "name": "lead_email",
      "value": "{{attendee_emails | filter: 'not contains \"@kalerealty.com\"' | first}}"
    },
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "note": "Search Superlative Leads board for matching email",
      "query": {
        "rules": [
          {
            "column_id": "email",
            "compare_value": "{{lead_email}}"
          }
        ]
      }
    },
    {
      "module": "filter",
      "note": "Only continue if lead found",
      "condition": "{{items | length}} > 0"
    },
    {
      "module": "monday.createUpdate",
      "board_id": 18390370563,
      "item_id": "{{items[0].id}}",
      "body": "📝 **Meeting Notes (Auto-captured from Gemini)**\n\n**Subject:** {{email_subject}}\n**Date:** {{email_date | date: 'MMM D, YYYY h:mm A'}}\n\n---\n\n{{email_body | stripHtml}}"
    },
    {
      "module": "monday.updateItem",
      "note": "Update Last Meaningful Reply date since this was a meeting",
      "board_id": 18390370563,
      "item_id": "{{items[0].id}}",
      "column_values": {
        "date_mkyctpv2": {
          "date": "{{now | date: 'YYYY-MM-DD'}}"
        }
      }
    }
  ]
}
```

**Step-by-Step Setup in Make.com:**

1. **Create New Scenario** → Name: "Gmail Meeting Notes to Monday"

2. **Module 1: Gmail - Watch Emails**
   - **Gmail Account:** `dj@kalerealty.com` (connect DJ's Gmail)
   - Folder: `INBOX`
   - Criteria:
     - From contains: `noreply@google.com`
     - Subject contains: `Meeting notes`
   - Mark emails as read: Yes
   - Max results: 10

3. **Module 2: Text Parser - Match Pattern**
   - Pattern: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}`
   - Text: `{{1.text}}` (email body)
   - Global match: Yes

4. **Module 3: Array Aggregator** (if multiple emails found)
   - Aggregate results from text parser

5. **Module 4: Iterator**
   - Iterate through found email addresses
   - Filter out @kalerealty.com addresses

6. **Module 5: Monday.com - Search Items by Column Value**
   - Board: Superlative Leads (18390370563)
   - Column: Email
   - Value: `{{iterator.email}}`

7. **Module 6: Filter**
   - Condition: `{{length(items)}} > 0`

8. **Module 7: Monday.com - Create an Update**
   - Board: Superlative Leads
   - Item ID: `{{5.items[1].id}}`
   - Body:
   ```
   📝 **Meeting Notes (Auto-captured from Gemini)**

   **Subject:** {{1.subject}}
   **Date:** {{formatDate(1.date; "MMM D, YYYY h:mm A")}}

   ---

   {{1.text}}
   ```

9. **Module 8: Monday.com - Change Column Value** (optional)
   - Update `Last Meaningful Reply` to today
   - This prevents ghost detection from flagging leads you've just met with

**Also Search Newly Licensed Board (Optional):**

If you want to also check the Newly Licensed board for matches:

```json
{
  "module": "monday.searchItems",
  "board_id": 18391158354,
  "note": "Also check Newly Licensed board",
  "query": {
    "rules": [
      {
        "column_id": "email",
        "compare_value": "{{lead_email}}"
      }
    ]
  }
}
```

**Cost:** Free (Make.com Gmail module included in all plans)

**Testing:**
1. Have a test meeting with Gemini recording enabled
2. Wait for the Gemini notes email to arrive
3. Verify the scenario triggers
4. Check Monday.com lead for the new update

---

## Testing Checklist

### Batch 1 Tests
- [ ] Change status to "Replied - Awaiting Ana" → verify Reply Received At is set
- [ ] Change status to "Ana Engaged" → verify First Response At and Response Time Mins set
- [ ] Wait for 8am daily run → verify Ghost Risk updates for active leads

### Batch 2 Tests
- [ ] Change status/temperature → verify Lead Score recalculates
- [ ] Wait for 6am daily run → verify Days In Stage updates
- [ ] Change status to "Won" → verify Total Days in Pipeline calculated

### Batch 3 Tests
- [ ] Set Competitor Name → verify Win-Back Date = today + 90 days
- [ ] On a lead's win-back date → verify Slack notification and Monday update
- [ ] Add note with "follow up" → verify Re-engagement Attempts increments
- [ ] Create new item → verify Referral Source auto-sets from Lead Source

### Batch 4 Tests
- [ ] Have a test meeting with Gemini recording enabled
- [ ] Wait for Gemini notes email to arrive in Gmail
- [ ] Verify Make.com scenario triggers on email arrival
- [ ] Verify lead is found by email address match
- [ ] Check Monday.com lead for new update with meeting notes
- [ ] Verify Last Meaningful Reply date is updated

---

## BATCH 5: Instantly Cold Email Integration (1 Scenario)

### Scenario 17: Instantly "Interested" Reply → Monday.com

**Purpose:** When a lead replies "interested" to an Instantly cold email campaign, this scenario:
1. Checks if the lead exists in Monday.com (both boards)
2. If exists: Updates the lead with email conversation, notifies assigned person
3. If DJ is assigned: Alerts both DJ and Ana
4. If nobody assigned: Assigns to Ana
5. If NOT exists: Creates new lead on Superlative board, assigns to Jennica for Courted lookup

**Context:** Instantly sends cold emails from a "fake" Kale persona. When leads respond positively, we need to capture this and route to the right team member.

**Trigger:** Instantly Webhook (`lead_interested` event)

**Flow Diagram:**
```
Instantly "Interested" Webhook
         │
         ▼
┌─────────────────────────────┐
│ Search Superlative Board    │
│ by email                    │
└──────────────┬──────────────┘
               │
      ┌────────┴────────┐
      │  Found?         │
      ▼                 ▼
     YES               NO
      │                 │
      ▼                 ▼
┌──────────────┐  ┌──────────────────┐
│ Check Owner  │  │ Search Newly     │
│              │  │ Licensed Board   │
└──────┬───────┘  └────────┬─────────┘
       │                   │
       ▼              Found? ──NO──▶ CREATE NEW LEAD
┌──────────────────┐       │         (assign Jennica)
│ DJ assigned?     │      YES
│                  │       │
└──────┬───────────┘       ▼
       │              ┌──────────────┐
  ┌────┴────┐         │ Update lead  │
  │         │         │ Notify Rea   │
 YES       NO         └──────────────┘
  │         │
  ▼         ▼
Alert     Is anyone
DJ+Ana    assigned?
          │
     ┌────┴────┐
    YES       NO
     │         │
     ▼         ▼
  Notify    Assign Ana
  owner     + Notify
```

### Column IDs Reference

**Superlative Board (18390370563):**
| Column | ID | Type |
|--------|-----|------|
| Email | `email_mky6p7cy` | email |
| First Name | `text_mky6wn9s` | text |
| Last Name | `text_mky6whek` | text |
| Person (legacy) | `person` | people |
| Assigned To | `multiple_person_mky6jgt4` | people |
| Status | `status` | status |

**Newly Licensed Board (18391158354):**
| Column | ID | Type |
|--------|-----|------|
| Email | `email_mkybfqax` | email |
| First Name | `text_mkybe1vc` | text |
| Last Name | `text_mkyb85z9` | text |
| Lead Owner | `multiple_person_mkyb4wzn` | people |
| Status | `color_mkybxbyk` | status |

**User IDs:**
| Name | User ID |
|------|---------|
| Ana (Anaya Dada) | `97053956` |
| D.J. Paris | `10993107` |
| Jennica Mercedes Abiera | `96623424` |
| Rea Endaya | `10995945` |

### Step-by-Step Make.com Setup

#### Step 1: Create the Webhook

1. In Make.com, create a new scenario
2. Add module: **Webhooks > Custom Webhook**
3. Click "Add" to create a new webhook
4. Name it: `Instantly Lead Interested`
5. Copy the webhook URL (you'll need this for Instantly)

#### Step 2: Register Webhook with Instantly

Run this API call to register your Make.com webhook with Instantly:

```bash
curl -X POST "https://api.instantly.ai/api/v2/webhooks" \
  -H "Authorization: Bearer Mzg0NjFkOGUtYTljZC00N2Y3LThmZTAtOTJjMWMzZDNjYWU2OnlhaXBod0dCWVZDcA==" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "lead_interested",
    "webhook_url": "YOUR_MAKE_WEBHOOK_URL_HERE"
  }'
```

#### Step 3: Build the Make.com Scenario

**Module 1: Webhooks - Custom Webhook**
- The trigger you created in Step 1

**Module 2: Monday.com - Search Items by Column Value**
- Board: Superlative Leads (`18390370563`)
- Column: Email (`email_mky6p7cy`)
- Value: `{{1.email}}` (from Instantly webhook)

**Module 3: Router** (3 paths)

---

**PATH A: Found in Superlative Board**

Condition: `{{length(2.items)}} > 0`

**Module A1: Monday.com - Get Item**
- Get full item details including person column
- Item ID: `{{2.items[1].id}}`

**Module A2: Router** (check who's assigned)

**Path A2a: DJ is assigned**
- Condition: Check if `10993107` is in the people column
- Action: Create update + notify both DJ and Ana

**Module A2a-1: Monday.com - Create Update**
```
📧 **Instantly Cold Email Reply - INTERESTED**

Lead replied positively to Instantly campaign.

**Email:** {{1.email}}
**Campaign:** {{1.campaign_name}}
**Reply:** {{1.reply_text}}

⚠️ Note: This lead was contacted via Instantly (cold email). DJ and Ana should discuss next steps since DJ is already assigned.
```

**Module A2a-2: Slack - Send Message** (to #ana-alerts)
```
🔥 *Instantly Lead Interested - DJ's Lead*
Lead *{{A1.name}}* replied to cold email!
<Monday Link>
DJ is assigned - please discuss next steps together.
```

**Path A2b: Someone else assigned (not DJ)**
- Condition: People column is not empty AND doesn't contain DJ
- Action: Update lead + notify the assigned person

**Module A2b-1: Monday.com - Create Update**
```
📧 **Instantly Cold Email Reply - INTERESTED**

Lead replied positively to Instantly campaign.

**Email:** {{1.email}}
**Campaign:** {{1.campaign_name}}
**Reply:** {{1.reply_text}}

Please follow up with this lead!
```

**Path A2c: Nobody assigned**
- Condition: People column is empty
- Action: Assign Ana + notify Ana

**Module A2c-1: Monday.com - Change Column Value**
- Column: `multiple_person_mky6jgt4` (Assigned To)
- Value: `{"personsAndTeams":[{"id":97053956,"kind":"person"}]}`

**Module A2c-2: Monday.com - Create Update**
```
📧 **Instantly Cold Email Reply - INTERESTED**

Lead replied positively to Instantly campaign.

**Email:** {{1.email}}
**Campaign:** {{1.campaign_name}}
**Reply:** {{1.reply_text}}

Ana has been auto-assigned to follow up.
```

---

**PATH B: Not in Superlative, Check Newly Licensed**

Condition: `{{length(2.items)}} = 0`

**Module B1: Monday.com - Search Items by Column Value**
- Board: Newly Licensed (`18391158354`)
- Column: Email (`email_mkybfqax`)
- Value: `{{1.email}}`

**Module B2: Filter**
- Condition: `{{length(B1.items)}} > 0`

**Module B3: Monday.com - Create Update**
- Item: `{{B1.items[1].id}}`
```
📧 **Instantly Cold Email Reply - INTERESTED**

Lead replied positively to Instantly campaign.

**Email:** {{1.email}}
**Campaign:** {{1.campaign_name}}
**Reply:** {{1.reply_text}}

Rea, please follow up with this lead!
```

**Module B4: Slack - Send Message** (to Rea's channel or DM)
```
🔥 *Instantly Lead Interested - Your Board*
Lead replied to cold email!
Email: {{1.email}}
<Monday Link>
```

---

**PATH C: Not Found Anywhere - Create New Lead**

Condition: `{{length(2.items)}} = 0` AND (Module B1 returns 0 items)

**Module C1: Monday.com - Create Item**
- Board: Superlative Leads (`18390370563`)
- Name: `{{1.email}}` (email as name since we don't have full name)
- Column Values:
```json
{
  "email_mky6p7cy": {"email": "{{1.email}}", "text": "{{1.email}}"},
  "multiple_person_mky6jgt4": {"personsAndTeams": [{"id": 96623424, "kind": "person"}]},
  "status": {"label": "New Lead"}
}
```

**Module C2: Monday.com - Create Update**
```
📧 **NEW LEAD from Instantly Cold Email**

This lead replied "interested" to an Instantly campaign but was NOT in our CRM.

**Email:** {{1.email}}
**Campaign:** {{1.campaign_name}}
**Reply:** {{1.reply_text}}

🔍 **Jennica Action Required:**
1. Look up this email in Courted
2. Fill in First Name, Last Name, Phone Number
3. Once complete, Ana will take over

⚠️ This is a cold email response - the lead doesn't know who contacted them (fake Kale persona was used).
```

**Module C3: Slack - Send Message** (to Jennica or #jennica-alerts)
```
🆕 *NEW Instantly Lead - Courted Lookup Needed*
A new lead replied to cold email but wasn't in our CRM.
Email: {{1.email}}
<Monday Link>
Please look them up in Courted and fill in their info!
```

---

### Instantly Webhook Payload Example

When Instantly fires the `lead_interested` webhook, it sends data like:

```json
{
  "event_type": "lead_interested",
  "email": "agent@example.com",
  "first_name": "John",
  "last_name": "Smith",
  "campaign_id": "abc123",
  "campaign_name": "Chicago Agents - December 2024",
  "reply_text": "Yes, I'd love to learn more about Kale Realty!",
  "reply_timestamp": "2024-12-09T15:30:00Z",
  "lead_id": "xyz789"
}
```

### Testing Checklist

- [ ] Register webhook with Instantly using the curl command
- [ ] Test with existing lead in Superlative (no owner) → should assign Ana
- [ ] Test with existing lead in Superlative (DJ assigned) → should alert DJ + Ana
- [ ] Test with existing lead in Superlative (someone else assigned) → should notify that person
- [ ] Test with existing lead in Newly Licensed → should notify Rea
- [ ] Test with NEW email (not in CRM) → should create lead, assign Jennica
- [ ] Verify Slack notifications are sent correctly
- [ ] Verify Monday updates contain correct info

### Follow-up Automation (Optional)

After Jennica fills in the lead details, you may want a native Monday automation:

**Trigger:** When First Name AND Last Name AND Phone are filled in
**Condition:** Lead Source = "Instantly" or status = "New Lead from Instantly"
**Action:**
1. Change status to "Replied - Awaiting Ana"
2. Assign Ana
3. Notify Ana

This ensures smooth handoff once Jennica completes the Courted lookup.

---

## BATCH 6: Cross-Board Sync (1 Scenario)

### Scenario 18: Kale Roster → Won Status Sync (DAILY)

**Purpose:** Automatically marks leads as "Won" when they appear in the active Kale Realty Agents roster board. This catches converted agents who may not have been manually updated.

**Context:** The Kale Realty Agents board (`359616654`) contains all active Kale agents. When a lead becomes an agent, their email and/or phone appears in this board. This scenario scans for matches and marks those leads as Won.

**Trigger:** Schedule - Daily at 7:00 AM (before ghost risk/days-in-stage updates)

**Boards Involved:**
| Board | ID | Purpose |
|-------|-----|---------|
| Kale Realty Agents (roster) | `359616654` | Source - active agents |
| Superlative Leads | `18390370563` | Target - mark as Won |
| Newly Licensed Leads | `18391158354` | Target - mark as Won |

**Column IDs:**

**Kale Realty Agents (Roster):**
| Column | ID | Type |
|--------|-----|------|
| Work Email | `work_email` | text |
| Phone Number | `phone_number8` | phone |
| Group | `group_title` | group |

**Superlative Leads:**
| Column | ID | Type |
|--------|-----|------|
| Email | `email_mky6p7cy` | email |
| Phone | `phone_mky6fr9j` | phone |
| Status | `status` | status |

**Newly Licensed Leads:**
| Column | ID | Type |
|--------|-----|------|
| Email | `email_mkybfqax` | email |
| Phone | `phone_mkyb4cr0` | phone |
| Lead Status | `color_mkybxbyk` | status |

**Make.com Scenario:**

```json
{
  "name": "Roster to Won Sync (Daily)",
  "trigger": {
    "module": "schedule",
    "interval": "daily",
    "time": "07:00"
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 359616654,
      "note": "Get all agents from Kale Agents group",
      "query": {
        "group_id": "group_title"
      },
      "columns": ["work_email", "phone_number8"]
    },
    {
      "module": "tools.aggregator",
      "note": "Build sets of agent emails and phones for comparison",
      "aggregate": {
        "emails": "{{items | map: 'work_email' | compact | map: 'lowercase'}}",
        "phones": "{{items | map: 'phone_number8' | compact | map: 'last10digits'}}"
      }
    },
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "note": "Get all Superlative leads not already Won",
      "query": {
        "rules": [
          {
            "column_id": "status",
            "compare_value_not": ["Won"]
          }
        ]
      },
      "columns": ["email_mky6p7cy", "phone_mky6fr9j"]
    },
    {
      "module": "iterator",
      "array": "{{superlative_leads}}"
    },
    {
      "module": "filter",
      "note": "Check if lead's email OR phone matches any agent",
      "condition": "{{agent_emails contains lead.email.lowercase}} OR {{agent_phones contains lead.phone.last10digits}}"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{lead.id}}",
      "column_values": {
        "status": {"label": "Won"}
      }
    },
    {
      "module": "monday.createUpdate",
      "board_id": 18390370563,
      "item_id": "{{lead.id}}",
      "body": "🎉 **Converted to Kale Agent!**\n\nThis lead has joined Kale Realty and is now in the active agent roster.\n\n*Automatically synced from Kale Realty Agents board.*"
    }
  ]
}
```

**Step-by-Step Setup in Make.com:**

1. **Create New Scenario** → Name: "Roster to Won Sync (Daily)"

2. **Module 1: Schedule**
   - Interval: Daily
   - Time: 07:00 (before other daily syncs)

3. **Module 2: Monday.com - Search Items (Roster)**
   - Board: Kale Realty Agents (`359616654`)
   - Filter by group: `group_title` (Kale Agents)
   - Columns: `work_email`, `phone_number8`
   - Limit: 500+ (to get all agents)

4. **Module 3: Tools - Set Multiple Variables**
   ```
   agent_emails = {{map(2.items; "column_values.work_email.text") | filter | map: lowercase}}
   agent_phones = {{map(2.items; "column_values.phone_number8.phone") | filter | map: last10digits}}
   ```

5. **Module 4: Monday.com - Search Items (Superlative)**
   - Board: Superlative Leads (`18390370563`)
   - Query: Status != Won
   - Columns: `email_mky6p7cy`, `phone_mky6fr9j`

6. **Module 5: Iterator**
   - Array: `{{4.items}}`

7. **Module 6: Filter**
   - Condition: Lead email in agent_emails OR lead phone (last 10 digits) in agent_phones

8. **Module 7: Monday.com - Change Column Value**
   - Board: `18390370563`
   - Item: `{{5.id}}`
   - Column: Status → "Won"

9. **Module 8: Monday.com - Create Update**
   - Item: `{{5.id}}`
   - Body: Conversion celebration message

10. **Duplicate Modules 4-8 for Newly Licensed Board** (18391158354)
    - Same logic, different board/column IDs

**Phone Normalization:**

Make.com doesn't have a built-in "last 10 digits" function. Use this formula:
```
{{if(length(phone) >= 10; substring(phone; length(phone) - 10; 10); phone)}}
```

**Email Normalization:**

Use lowercase comparison:
```
{{lowercase(trim(email))}}
```

**Alternative: Python Script (One-Time)**

For bulk backfill or if Make.com complexity is too high, use the Python script:

```bash
cd scripts && python3 sync-won-from-roster.py
```

Script location: `scripts/sync-won-from-roster.py`

**Dry-run first:**
```bash
python3 sync-won-from-roster.py --dry-run
```

**Testing Checklist:**

- [ ] Add a test lead with email/phone matching a known Kale agent
- [ ] Run scenario manually or wait for 7am
- [ ] Verify lead status changed to "Won"
- [ ] Verify update note was created
- [ ] Check Newly Licensed board works the same way
- [ ] Verify no false positives (non-matching leads unchanged)

---

## BATCH 7: Win-Back Campaigns (2 Scenarios)

### Scenario 19: Former Agent Win-Back SMS (DAILY - GitHub Actions)

**Purpose:** Sends personalized spintax SMS to former agents on a quarterly cadence. SMS messages rotate through 3 templates, with emails sent 15 days after each SMS via Make.com (Scenario 20).

**Staggered Schedule:**
| Day | Channel | Message Theme |
|-----|---------|---------------|
| 90 | SMS | AI Tool Feedback Request |
| 105 | Email | AI Tool Feedback (expanded) |
| 180 | SMS | We'd Love You Back |
| 195 | Email | What's New at Kale |
| 270 | SMS | New Feature Announcement |
| 285 | Email | Personal Check-In |

**Trigger:** Schedule - Daily at 10:00 AM CT (GitHub Actions)

**Board:** Former Kale Agents We Want Back (`18391489234`)

**Column IDs:**
| Column | Column ID | Type |
|--------|-----------|------|
| Name | `name` | name |
| First Name | `text_mkyfws0a` | text |
| Phone | `phone_mkyfkn1f` | phone |
| Email | `email_mkyfnfx4` | email |
| Status | `color_mkyfnpqe` | status |
| Termination Date | `date_mkygj51c` | date |
| Win-Back Date (SMS) | `date_mkygkfv` | date |
| Email Win-Back Date | `date_mkyg2ebg` | date |
| Win-Back Count | `numeric_mkyg19jw` | number |
| Do Not Contact | `boolean_mkygt8d2` | checkbox |
| Owner | `multiple_person_mkyftdm7` | people |

**SMS Messages (Spintax - rotates based on Win-Back Count % 3):**

**SMS #1 - Day 90: AI Tool Feedback**
```
{Hey|Hi} {first_name} - {hope all is well|hope you're doing great|how's it going}! I just launched this listing description AI tool and would love your feedback. It researches your neighborhood and rewrites listings to get more showings.

Try it free: listing.joinkale.com

{Let me know what you think|Would love your thoughts|Curious what you think}? {No strings - just want honest feedback|Just looking for honest feedback} from someone who knows their stuff.

- DJ
```

**SMS #2 - Day 180: We'd Love You Back**
```
{Hey|Hi} {first_name} - just wanted to {check in|reach out|say hi}. {Miss having you around|Been thinking about the old crew|Hope the new gig is treating you well}. {If things ever change|If you ever want to chat|If you're ever curious about what's new}, {my door's always open|you know where to find me|just reach out}.

- DJ
```

**SMS #3 - Day 270: New Feature**
```
{Hey|Hi} {first_name} - {it's been a while|long time no talk|hope you're killing it out there}. {We've been making some changes here at Kale|Lot of new stuff happening at Kale|Things are evolving here} and {I thought of you|wanted to let you know|figured you might be curious}. {Let me know if you ever want to catch up|Would love to chat sometime|Reach out if you want to hear about it}.

- DJ
```

**Implementation: GitHub Actions (Free)**

This automation runs via GitHub Actions to avoid Make.com credit costs. The Python script:
1. Queries Former Agents board for items where Win-Back Date = today AND Win-Back Sent = false
2. Sends SMS via JustCall API
3. Marks Win-Back Sent = true
4. Creates update note on the item

**GitHub Actions Workflow:** `.github/workflows/winback-sms.yml`

```yaml
name: Daily Win-Back SMS

on:
  schedule:
    # Runs every day at 3:00 PM UTC (10 AM Chicago time)
    - cron: '0 15 * * *'
  workflow_dispatch:
    # Allows manual trigger from GitHub Actions tab

jobs:
  send-winback-sms:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests

      - name: Run Win-Back SMS Script
        env:
          MONDAY_API_KEY: ${{ secrets.MONDAY_API_KEY }}
          JUSTCALL_API_KEY: ${{ secrets.JUSTCALL_API_KEY }}
          JUSTCALL_API_SECRET: ${{ secrets.JUSTCALL_API_SECRET }}
        run: python scripts/send-winback-sms.py

      - name: Upload log
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: winback-log-${{ github.run_number }}
          path: /tmp/winback_sms.log
          retention-days: 30
```

**Python Script:** `scripts/send-winback-sms.py`

```python
#!/usr/bin/env python3
"""
Win-Back SMS Script

Sends personalized SMS to former agents 90 days after termination,
offering free access to the Kale Listing AI tool.

Runs daily via GitHub Actions.
"""

import requests
import json
import time
import os
from datetime import datetime, date

# Configuration
MONDAY_API_KEY = os.environ.get("MONDAY_API_KEY")
JUSTCALL_API_KEY = os.environ.get("JUSTCALL_API_KEY")
JUSTCALL_API_SECRET = os.environ.get("JUSTCALL_API_SECRET")

MONDAY_API_URL = "https://api.monday.com/v2"
JUSTCALL_SMS_URL = "https://api.justcall.io/v1/texts/new"

FORMER_AGENTS_BOARD_ID = "18391489234"
WINBACK_DATE_COL = "date_mkygkfv"
WINBACK_SENT_COL = "boolean_mkygr6v"
FIRST_NAME_COL = "text_mkyfws0a"
PHONE_COL = "phone_mkyfkn1f"

SMS_MESSAGE = """Hey {first_name} - hope all is well! I just launched this listing description AI tool and would love your feedback. It researches your neighborhood and rewrites listings to get more showings.

Try it free: listing.joinkale.com

Let me know what you think? No strings - just want honest feedback from someone who knows their stuff.

- DJ"""

def monday_query(query):
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json",
        "API-Version": "2024-10"
    }
    response = requests.post(MONDAY_API_URL, headers=headers, json={"query": query})
    return response.json().get("data")

def get_todays_winbacks():
    """Get former agents where Win-Back Date = today and Win-Back Sent = false."""
    today = date.today().isoformat()

    query = """
    query {
        boards(ids: [%s]) {
            items_page(limit: 100) {
                items {
                    id
                    name
                    column_values {
                        id
                        text
                        value
                    }
                }
            }
        }
    }
    """ % FORMER_AGENTS_BOARD_ID

    result = monday_query(query)
    items = result.get("boards", [{}])[0].get("items_page", {}).get("items", [])

    ready_items = []
    for item in items:
        cols = {c["id"]: c for c in item.get("column_values", [])}

        winback_date = cols.get(WINBACK_DATE_COL, {}).get("text", "")
        winback_sent = cols.get(WINBACK_SENT_COL, {}).get("text", "")

        if winback_date == today and winback_sent != "true":
            first_name = cols.get(FIRST_NAME_COL, {}).get("text", "")
            phone_data = cols.get(PHONE_COL, {}).get("value", "{}")
            phone = json.loads(phone_data).get("phone", "") if phone_data else ""

            if phone and first_name:
                ready_items.append({
                    "id": item["id"],
                    "name": item["name"],
                    "first_name": first_name,
                    "phone": phone
                })

    return ready_items

def send_sms(phone, message):
    """Send SMS via JustCall API."""
    headers = {
        "Authorization": f"{JUSTCALL_API_KEY}:{JUSTCALL_API_SECRET}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": phone,
        "body": message
    }
    response = requests.post(JUSTCALL_SMS_URL, headers=headers, json=payload)
    return response.status_code == 200

def mark_sent(item_id):
    """Mark Win-Back Sent = true on Monday item."""
    query = """
    mutation {
        change_column_value(
            board_id: %s,
            item_id: %s,
            column_id: "%s",
            value: "{\\"checked\\": true}"
        ) {
            id
        }
    }
    """ % (FORMER_AGENTS_BOARD_ID, item_id, WINBACK_SENT_COL)

    return monday_query(query)

def create_update(item_id, message):
    """Create update note on Monday item."""
    query = """
    mutation {
        create_update(
            item_id: %s,
            body: "%s"
        ) {
            id
        }
    }
    """ % (item_id, message.replace('"', '\\"').replace('\n', '\\n'))

    return monday_query(query)

def main():
    print("=" * 60)
    print("Win-Back SMS Script")
    print(f"Date: {date.today().isoformat()}")
    print("=" * 60)

    items = get_todays_winbacks()
    print(f"Found {len(items)} agents ready for win-back SMS")

    stats = {"sent": 0, "failed": 0}

    for item in items:
        message = SMS_MESSAGE.format(first_name=item["first_name"])

        print(f"  Sending to {item['name']} ({item['phone']})...", end=" ")

        if send_sms(item["phone"], message):
            mark_sent(item["id"])
            create_update(item["id"],
                f"Win-back SMS sent via JustCall.\\n\\n"
                f"Message: {message[:100]}...")
            print("SENT")
            stats["sent"] += 1
        else:
            print("FAILED")
            stats["failed"] += 1

        time.sleep(1)  # Rate limiting

    print()
    print("=" * 60)
    print("Complete!")
    print(f"  Sent: {stats['sent']}")
    print(f"  Failed: {stats['failed']}")

if __name__ == "__main__":
    main()
```

**Monday.com Automation (Set Win-Back Date):**

Create a native Monday automation to auto-calculate Win-Back Date:

**Trigger:** When Termination Date changes
**Action:** Set Win-Back Date = Termination Date + 90 days

This can be done with Monday's formula column or a simple automation.

**Required GitHub Secrets:**
- `MONDAY_API_KEY` - Already added
- `JUSTCALL_API_KEY` - JustCall API key
- `JUSTCALL_API_SECRET` - JustCall API secret

**Testing Checklist:**

- [ ] Add Win-Back columns to Former Agents board (DONE)
- [ ] Create Monday automation: Termination Date → Win-Back Date + 90 days
- [ ] Add JustCall API credentials to GitHub Secrets
- [ ] Create `scripts/send-winback-sms.py`
- [ ] Create `.github/workflows/winback-sms.yml`
- [ ] Test with a single agent (set Win-Back Date = today)
- [ ] Verify SMS received
- [ ] Verify Win-Back Sent checkbox marked
- [ ] Verify update note created on item

**JustCall Reply Handling (Future):**

When a former agent replies to the SMS, JustCall can send a webhook to Make.com. A simple scenario would:
1. Receive JustCall incoming SMS webhook
2. Match phone number to Former Agents board
3. Update status to "Replied"
4. Assign to Ana
5. Notify Ana via Slack/Monday

This reply handling can be added as Scenario 21 once the outbound SMS is working.

---

### Scenario 20: Former Agent Win-Back Email (DAILY - Make.com)

**Purpose:** Sends personalized emails to former agents 15 days after each SMS touchpoint. Emails are sent via Make.com from `dj@kalerealty.com` (max 5/day to protect sender reputation).

**Trigger:** Schedule - Daily at 10:00 AM CT

**Board:** Former Kale Agents We Want Back (`18391489234`)

**Logic:** When SMS is sent (Scenario 19), the Python script sets `Email Win-Back Date` = today + 15 days. This Make.com scenario watches for leads where that date equals today.

---

#### Make.com Module Flow

```
[Schedule: Daily 10AM CT]
        ↓
[Monday: Search Items where Email Win-Back Date = today AND Do Not Contact != true, limit 5]
        ↓
[Iterator: Loop through results]
        ↓
[Router: Based on Win-Back Count % 3]
        ↓
[Route 0: AI Tool Feedback Email]
[Route 1: What's New at Kale Email]
[Route 2: Personal Check-In Email]
        ↓
[Email: Send from dj@kalerealty.com]
        ↓
[Monday: Update Email Win-Back Date + 90 days]
        ↓
[Monday: Create Update note]
```

---

#### Module 1: Schedule Trigger
- **Type:** Schedule
- **Interval:** Every day at 10:00 AM (CT)

#### Module 2: Monday.com - Search Items by Column Value
- **Board:** Former Agents (`18391489234`)
- **Column:** Email Win-Back Date (`date_mkyg2ebg`)
- **Value:** `{{formatDate(now; "YYYY-MM-DD")}}`
- **Additional Filter:** Do Not Contact (`boolean_mkygt8d2`) != true
- **Limit:** `5`

#### Module 3: Iterator
- **Array:** Results from Module 2

#### Module 4: Router (3 paths based on Win-Back Count % 3)

**Route Conditions:**
- **Route 0:** `{{mod(3.Win-Back Count; 3)}} = 0` → AI Tool Feedback
- **Route 1:** `{{mod(3.Win-Back Count; 3)}} = 1` → What's New
- **Route 2:** `{{mod(3.Win-Back Count; 3)}} = 2` → Personal Check-In

---

#### Email #1 - Day 105: AI Tool Feedback (Route 0)

**Subject Lines (use `pick()` for variation):**
```
{{pick("Quick question"; "Curious what you think"; "Need your expert opinion")}}, {{3.First Name}}
```

**Body:**
```html
<div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6;">

{{pick("Hey"; "Hi")}} {{3.First Name}},<br><br>

{{pick("Hope you're doing well"; "Hope things are going great"; "How's everything going")}}!<br><br>

I {{pick("just built"; "recently launched"; "put together")}} this AI tool that {{pick("rewrites listing descriptions"; "helps agents write better listings"; "generates listing copy")}} - it actually {{pick("researches the neighborhood"; "pulls local data"; "analyzes the area")}} and {{pick("creates descriptions that get more showings"; "writes copy that converts"; "generates high-performing content")}}.<br><br>

{{pick("I know you always had an eye for good marketing"; "You always knew what worked"; "You've got great instincts for this stuff")}}, so I'd {{pick("really value your feedback"; "love to hear what you think"; "appreciate your honest take")}}.<br><br>

{{pick("Here's the link"; "Check it out"; "Try it here")}}: <a href="https://listing.joinkale.com">listing.joinkale.com</a><br><br>

{{pick("No strings attached"; "Totally free"; "No commitment")}} - just {{pick("looking for honest feedback"; "want to know if it's actually useful"; "curious if it helps")}}.<br><br>

{{pick("Thanks"; "Appreciate it")}},<br>
DJ<br><br>

--<br>
DJ Paris<br>
Kale Realty<br>
dj@kalerealty.com

</div>
```

---

#### Email #2 - Day 195: What's New at Kale (Route 1)

**Subject Lines:**
```
{{pick("Things have changed"; "Lot happening")}} at Kale, {{3.First Name}}
```

**Body:**
```html
<div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6;">

{{pick("Hey"; "Hi")}} {{3.First Name}},<br><br>

{{pick("Wanted to reach out"; "Just thinking about you"; "Hope you're killing it out there")}}.<br><br>

{{pick("We've made some changes at Kale"; "Things have evolved here"; "A lot has happened since you left")}} - {{pick("new tools"; "better systems"; "some cool stuff")}} that {{pick("I think you'd appreciate"; "might interest you"; "you'd probably like")}}.<br><br>

{{pick("If you're ever curious"; "If things change on your end"; "If you ever want to chat")}}, {{pick("I'd love to catch up"; "my door's open"; "just reach out")}}. {{pick("We'd love to have you back"; "Always a spot for you here"; "You're always welcome")}}.<br><br>

{{pick("No pressure"; "Just wanted you to know"; "Totally understand if you're happy where you are")}} - {{pick("just keeping the door open"; "just saying hi"; "wanted to stay in touch")}}.<br><br>

{{pick("Talk soon"; "Best")}},<br>
DJ<br><br>

--<br>
DJ Paris<br>
Kale Realty<br>
dj@kalerealty.com

</div>
```

---

#### Email #3 - Day 285: Personal Check-In (Route 2)

**Subject Lines:**
```
{{pick("Checking in"; "Just saying hi")}}, {{3.First Name}}
```

**Body:**
```html
<div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6;">

{{pick("Hey"; "Hi")}} {{3.First Name}},<br><br>

{{pick("It's been a while"; "Long time no talk"; "Hope all is well")}}.<br><br>

{{pick("Just wanted to check in"; "Thinking about you"; "Wanted to say hi")}} and see {{pick("how things are going"; "how you're doing"; "what you're up to")}}.<br><br>

{{pick("I've been building some new stuff"; "We've added some great tools"; "The team has grown")}} and {{pick("honestly"; "I'll be real"; "truthfully")}}, {{pick("I think you'd really like what we're doing now"; "things are different in a good way"; "we've gotten better")}}.<br><br>

{{pick("If you ever want to reconnect"; "If you're ever open to a conversation"; "If things change")}}, {{pick("I'd love to chat"; "reach out anytime"; "you know where to find me")}}. {{pick("We'd love to have you back"; "There's always a place for you"; "The door's always open")}}.<br><br>

{{pick("Hope you're well"; "Take care"; "Talk soon")}},<br>
DJ<br><br>

--<br>
DJ Paris<br>
Kale Realty<br>
dj@kalerealty.com

</div>
```

---

#### Module 5 (all routes): Email - Send
- **From:** `dj@kalerealty.com`
- **From Name:** `DJ Paris`
- **To:** `{{3.Email}}` (from Monday `email_mkyfnfx4`)
- **Subject:** (from route-specific subject)
- **Body (HTML):** (from route-specific body)

#### Module 6: Monday.com - Change Multiple Column Values
- **Board:** `18391489234`
- **Item ID:** `{{3.id}}`
- **Column Values:**
  - `date_mkyg2ebg` (Email Win-Back Date): `{{addDays(now; 90)}}`

#### Module 7: Monday.com - Create Update
- **Item ID:** `{{3.id}}`
- **Body:** `📧 Win-back email sent via Make\n\nSubject: {{email_subject}}\nMessage type: {{route_name}}`

---

#### Testing Checklist

- [ ] Set one test agent's Email Win-Back Date = today
- [ ] Run scenario manually
- [ ] Verify email arrives from dj@kalerealty.com
- [ ] Verify Email Win-Back Date updated to +90 days
- [ ] Verify update note created
- [ ] Test all 3 routes (change Win-Back Count to 0, 1, 2)
- [ ] Verify max 5 emails sent per run

---

#### Notes

- **Max 5 emails/day** protects dj@kalerealty.com sender reputation
- **15-day gap** ensures agents don't get SMS and email on same day
- **Spintax via pick()** creates natural variation - no two emails identical
- **Do Not Contact** flag is respected
- **Email Win-Back Date** auto-advances 90 days after each send

---

## BATCH 8: Rea's Newly Licensed Import (1 Scenario + Google Apps Script)

### Scenario 21: Google Sheets → Monday Newly Licensed Import

**Purpose:** Rea receives monthly AMP passer lists (newly licensed brokers). This automation:
1. Filters by Chicago-area cities only
2. Filters by broker license types only (excludes leasing agents)
3. Deduplicates by email
4. Creates leads in Monday.com "Newly Licensed Leads" board
5. Enrolls in Close CRM SMS workflow

**Components:**
- **Google Apps Script** (in Google Sheets) - handles filtering/deduping
- **Make.com Webhook** - receives clean data, creates Monday items

---

### Google Apps Script Setup

**Script location:** `rea/google-apps-script-import.js`

**Installation:**
1. Open Google Sheet with AMP passer CSV data
2. Go to **Extensions → Apps Script**
3. Delete existing code, paste contents of `rea/google-apps-script-import.js`
4. Update `MAKE_WEBHOOK_URL` with your webhook URL
5. Save and refresh sheet
6. New **"Rea Import"** menu appears

**Menu Options:**
| Menu Item | Description |
|-----------|-------------|
| Preview Import (Dry Run) | Shows what will be imported without sending |
| Import to Monday | Filters, dedupes, sends to Monday.com |
| Show Statistics | Displays license types and cities breakdown |

**Filters Applied:**
1. **License Type** - Only includes:
   - `IL Broker National Portion`
   - `IL Broker State Portion`
   - `IL Broker Reciprocity Examination`

2. **Chicago Area Cities** - ~150 approved cities (see script for full list)

3. **Required Data** - Must have First Name, Last Name, Email

4. **Email Deduplication** - Keeps first occurrence only

**CSV Column Requirements:**
| Column | Required | Notes |
|--------|----------|-------|
| `First Name` | Yes | |
| `Last Name` | Yes | |
| `Email` | Yes | Used for deduplication |
| `Phone` | No | |
| `City` | Yes | Used for geographic filtering |
| `Test Date` | No | |
| `Portion` | Yes | License type - used for filtering |

---

### Make.com Scenario

**Trigger:** Custom Webhook (from Google Apps Script)

**Board:** Newly Licensed Leads (`18391158354`)

**Column IDs:**
| Column | Column ID | Type |
|--------|-----------|------|
| Name | `name` | name |
| First Name | `text_mkybe1vc` | text |
| Last Name | `text_mkyb85z9` | text |
| Email | `email_mkybfqax` | email |
| Phone | `phone_mkyb4cr0` | phone |
| Lead Status | `color_mkybxbyk` | status |
| Import Date | `date_mkybk1hp` | date |
| Lead Owner | `multiple_person_mkyb4wzn` | people |
| Close CRM Lead ID | `text_mkyb1a5v` | text |

**Group IDs:**
| Group | ID |
|-------|-----|
| Never Responded | `group_mkyb6hgy` |
| Responded | `group_mkyb51b6` |
| Scheduled Appointments | `group_mkybxtds` |
| Initially Responded, Then Disappeared | `group_mkyb64mg` |

**User IDs:**
| Name | User ID |
|------|---------|
| Rea Endaya | `10995945` |

---

#### Make.com Module Flow

```
[Custom Webhook: Receive from Google Sheets]
        ↓
[Iterator: Loop through leads array]
        ↓
[Monday: Search by email (dedupe check)]
        ↓
[Router]
    ├── [Lead exists] → Log & skip
    └── [New lead] →
        ↓
[Monday: Create Item in "Never Responded" group]
        ↓
[Close CRM: Create Lead]
        ↓
[Close CRM: Enroll in SMS Sequence]
        ↓
[Monday: Store Close Lead ID]
        ↓
[Monday: Update status to "In Workflow"]
```

---

#### Module Details

**Module 1: Custom Webhook**
- Create webhook, copy URL to Google Apps Script

**Module 2: Iterator**
- Array: `{{1.leads}}`

**Module 3: Monday.com - Search Items**
- Board: `18391158354`
- Column: `email_mkybfqax`
- Value: `{{2.email}}`

**Module 4: Router**
- Route A: `{{length(3.items)}} > 0` → Skip (duplicate)
- Route B: Default → Create new lead

**Module 5: Monday.com - Create Item** (Route B)
```json
{
  "boardId": "18391158354",
  "groupId": "group_mkyb6hgy",
  "itemName": "{{2.firstName}} {{2.lastName}}",
  "columnValues": {
    "text_mkybe1vc": "{{2.firstName}}",
    "text_mkyb85z9": "{{2.lastName}}",
    "email_mkybfqax": {"email": "{{2.email}}", "text": "{{2.email}}"},
    "phone_mkyb4cr0": {"phone": "{{2.phone}}", "countryShortName": "US"},
    "color_mkybxbyk": {"label": "New Lead"},
    "date_mkybk1hp": {"date": "{{formatDate(now; 'YYYY-MM-DD')}}"},
    "multiple_person_mkyb4wzn": {"personsAndTeams": [{"id": 10995945, "kind": "person"}]}
  }
}
```

**Module 6: Close CRM - Create Lead**
```json
{
  "name": "{{2.firstName}} {{2.lastName}}",
  "contacts": [{
    "name": "{{2.firstName}} {{2.lastName}}",
    "emails": [{"email": "{{2.email}}", "type": "office"}],
    "phones": [{"phone": "{{2.phone}}", "type": "mobile"}]
  }],
  "custom_fields": {
    "monday_item_id": "{{5.id}}"
  }
}
```

**Module 7: Close CRM - Create Sequence Subscription**
- Sequence ID: `seq_7TUbe0qzdkzDqHMTy63BMb`
- Contact ID: `{{6.contacts[0].id}}`

**Module 8: Monday.com - Change Column Value**
- Store Close Lead ID: `{{6.id}}` in column `text_mkyb1a5v`

**Module 9: Monday.com - Change Column Value**
- Update status to "In Workflow"

---

#### Testing Checklist

- [ ] Create webhook in Make.com, copy URL
- [ ] Update Google Apps Script with webhook URL
- [ ] Test "Preview Import" with sample CSV
- [ ] Test "Import to Monday" with 2-3 test leads
- [ ] Verify Monday items created in "Never Responded" group
- [ ] Verify Close CRM leads created
- [ ] Verify SMS sequence enrollment
- [ ] Verify status shows "In Workflow"
- [ ] Test with full month's data
