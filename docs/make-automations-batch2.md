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

## Summary: All 15 Make.com Scenarios

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
