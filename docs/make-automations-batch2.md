# Make.com Automations - Batch 2

**Board ID:** `18390370563` (Superlative Leads)

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
