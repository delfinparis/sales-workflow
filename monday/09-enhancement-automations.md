# CRM Enhancement Automations

Automations for the 21 new columns added in the gap analysis.

**Board ID:** 18390370563 (Superlative Leads)

---

## New Column Reference

### Gap 1: Lead Scoring / Temperature
| Column | ID | Type |
|--------|-----|------|
| Temperature | `color_mkyce0h5` | Status (Cold/Warm/Hot) |
| Lead Score | `numeric_mkycbffy` | Number (0-100) |

### Gap 2: Why They'll Switch
| Column | ID | Type |
|--------|-----|------|
| Pain Points | `long_text_mkyctp3t` | Long Text |
| Pain Signals | `numeric_mkycmf31` | Number |
| Current Split | `text_mkycr936` | Text |
| Trigger Event | `color_mkyckhtm` | Status |

### Gap 3: Speed-to-Lead
| Column | ID | Type |
|--------|-----|------|
| Reply Received At | `date_mkyc9xa8` | Date |
| First Response At | `date_mkycjb4b` | Date |
| Response Time Mins | `numeric_mkycpyr8` | Number |

### Gap 4: Competitive Intelligence
| Column | ID | Type |
|--------|-----|------|
| Competitor Name | `color_mkyc4rpk` | Status |
| Competitor Reason | `text_mkycr5cc` | Text |
| Win-Back Date | `date_mkyct9n3` | Date |

### Gap 5: Referral Tracking
| Column | ID | Type |
|--------|-----|------|
| Referral Source | `color_mkych05` | Status |
| Referred By | `text_mkyc1gd2` | Text |

### Gap 6: Ghost Prevention
| Column | ID | Type |
|--------|-----|------|
| Ghost Risk | `color_mkyc52cw` | Status (Low/Medium/High/Ghosted) |
| Last Meaningful Reply | `date_mkyctpv2` | Date |
| Re-engagement Attempts | `numeric_mkyc534x` | Number |

### Gap 7: Pipeline Velocity
| Column | ID | Type |
|--------|-----|------|
| Stage Entry Date | `date_mkyck8r9` | Date |
| Days In Stage | `numeric_mkycxytk` | Number |
| First Contact Date | `date_mkycg4ew` | Date |
| Total Days in Pipeline | `numeric_mkycf1d6` | Number |

---

## Automation 1: Auto-Calculate Lead Score

**Purpose:** Calculate a lead score (0-100) based on engagement signals.

**Scoring Logic:**
| Signal | Points |
|--------|--------|
| Replied to SMS | +20 |
| Multiple replies | +10 per additional reply |
| Tool downloaded | +15 |
| Training attended | +20 |
| Voice memo sent | +5 |
| Meeting scheduled | +25 |
| Pain points mentioned | +5 per signal |
| Hot temperature | +10 |

### Make.com Scenario

```json
{
  "name": "Calculate Lead Score",
  "description": "Recalculates lead score when engagement signals change",
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
      "columns": [
        "status",
        "color_mkyce0h5",
        "numeric_mkycmf31",
        "checkbox_mky6rxjz"
      ]
    },
    {
      "module": "tools.setVariables",
      "variables": {
        "score": 0
      }
    },
    {
      "module": "tools.calculate",
      "calculations": [
        {
          "name": "status_points",
          "formula": "SWITCH(status, 'SMS Sent', 0, 'Replied', 20, 'Ana Engaged', 30, 'Tool Offered', 45, 'Training Invited', 50, 'Relationship Building', 60, 'Ask Made', 75, 'Meeting Scheduled', 90, 'Won', 100, 0)"
        },
        {
          "name": "temperature_points",
          "formula": "SWITCH(temperature, 'Cold', 0, 'Warm', 10, 'Hot', 20, 0)"
        },
        {
          "name": "pain_points",
          "formula": "pain_signals * 5"
        },
        {
          "name": "total_score",
          "formula": "MIN(100, status_points + temperature_points + pain_points)"
        }
      ]
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

### Visual Workflow
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Status/Temp/    │────▶│ Calculate Score │────▶│ Update Lead     │
│ Pain Changes    │     │ Based on Rules  │     │ Score Column    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

---

## Automation 2: Auto-Update Temperature

**Purpose:** Automatically update Temperature based on engagement level.

**Temperature Logic:**
| Condition | Temperature |
|-----------|-------------|
| New Lead, SMS Sent | Cold |
| Replied, Ana Engaged | Warm |
| Tool Offered, Training Invited, Relationship Building | Warm |
| Ask Made, Meeting Scheduled | Hot |
| Hibernation, Timeout | Cold |

### Make.com Scenario

```json
{
  "name": "Auto-Update Temperature",
  "description": "Sets temperature based on current status",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status"
  },
  "actions": [
    {
      "module": "tools.switch",
      "value": "{{new_status}}",
      "cases": [
        {
          "pattern": "New Lead|SMS Sent|30-Day Timeout|Hibernation.*",
          "result": "Cold"
        },
        {
          "pattern": "Replied.*|Ana Engaged|Tool Offered|Training Invited|Relationship Building",
          "result": "Warm"
        },
        {
          "pattern": "Ask Made|Meeting Scheduled|Offer Extended",
          "result": "Hot"
        }
      ],
      "default": "Cold"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "color_mkyce0h5": {
          "label": "{{temperature}}"
        }
      }
    }
  ]
}
```

### Native Monday Alternative

You can also set this up in Monday native automations:

```
Automation 2a:
When Status changes to "New Lead" OR "SMS Sent" OR "30-Day Timeout"
→ Change Temperature to "Cold"

Automation 2b:
When Status changes to "Replied - Awaiting Ana" OR "Ana Engaged" OR "Tool Offered"
→ Change Temperature to "Warm"

Automation 2c:
When Status changes to "Ask Made" OR "Meeting Scheduled" OR "Offer Extended"
→ Change Temperature to "Hot"
```

---

## Automation 3: Track Speed-to-Lead

**Purpose:** Capture reply timestamp and calculate response time when Ana responds.

### Make.com Scenario 3a: Capture Reply Time

```json
{
  "name": "Capture Reply Timestamp",
  "description": "When status changes to Replied, capture the timestamp",
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
        }
      }
    }
  ]
}
```

### Make.com Scenario 3b: Calculate Response Time

```json
{
  "name": "Calculate Response Time",
  "description": "When status changes from Replied to Ana Engaged, calculate response time",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status",
    "previous_value": "Replied - Awaiting Ana",
    "new_value": "Ana Engaged"
  },
  "actions": [
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "columns": ["date_mkyc9xa8"]
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
        "numeric_mkycpyr8": "{{(now - reply_received_at) / 60000}}"
      }
    }
  ]
}
```

### Visual Workflow
```
Lead Replies          Ana Responds          Metrics Updated
     │                     │                     │
     ▼                     ▼                     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────────────┐
│ Status →    │     │ Status →    │     │ Response Time Mins  │
│ "Replied"   │────▶│ "Engaged"   │────▶│ = Now - Reply Time  │
└─────────────┘     └─────────────┘     └─────────────────────┘
     │
     ▼
Reply Received At
= NOW()
```

---

## Automation 4: Ghost Risk Detection

**Purpose:** Auto-update Ghost Risk based on days since last meaningful reply.

**Ghost Risk Logic:**
| Days Since Reply | Ghost Risk |
|------------------|------------|
| 0-3 days | Low |
| 4-7 days | Medium |
| 8-14 days | High |
| 15+ days | Ghosted |

### Make.com Scenario (Scheduled - Daily)

```json
{
  "name": "Update Ghost Risk (Daily)",
  "description": "Runs daily to check all active leads for ghost risk",
  "trigger": {
    "module": "schedule",
    "interval": "daily",
    "time": "08:00"
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "query": {
        "rules": [
          {
            "column_id": "status",
            "compare_value": ["Ana Engaged", "Tool Offered", "Relationship Building", "Ask Made"]
          }
        ]
      }
    },
    {
      "module": "iterator",
      "array": "{{items}}"
    },
    {
      "module": "tools.calculate",
      "formula": "(now - last_meaningful_reply) / 86400000"
    },
    {
      "module": "tools.switch",
      "value": "{{days_since_reply}}",
      "cases": [
        {"pattern": "0-3", "result": "Low"},
        {"pattern": "4-7", "result": "Medium"},
        {"pattern": "8-14", "result": "High"},
        {"pattern": "15+", "result": "Ghosted"}
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

### Make.com Scenario 4b: Update Last Meaningful Reply

```json
{
  "name": "Track Meaningful Reply",
  "description": "When a note is added that indicates a reply, update Last Meaningful Reply",
  "trigger": {
    "module": "monday.watchUpdates",
    "board_id": 18390370563
  },
  "actions": [
    {
      "module": "tools.textParser",
      "input": "{{update_body}}",
      "pattern": "(replied|responded|said|texted back|called back)"
    },
    {
      "module": "monday.updateItem",
      "condition": "pattern_matched",
      "board_id": 18390370563,
      "item_id": "{{item_id}}",
      "column_values": {
        "date_mkyctpv2": {
          "date": "{{now | date: 'YYYY-MM-DD'}}"
        },
        "color_mkyc52cw": {
          "label": "Low"
        }
      }
    }
  ]
}
```

---

## Automation 5: Pipeline Velocity Tracking

**Purpose:** Track how long leads spend in each stage.

### Make.com Scenario 5a: Set Stage Entry Date on Status Change

```json
{
  "name": "Track Stage Entry",
  "description": "When status changes, record the stage entry date",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status"
  },
  "actions": [
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "date_mkyck8r9": {
          "date": "{{now | date: 'YYYY-MM-DD'}}"
        },
        "numeric_mkycxytk": 0
      }
    }
  ]
}
```

### Make.com Scenario 5b: Update Days In Stage (Daily)

```json
{
  "name": "Update Days In Stage (Daily)",
  "description": "Runs daily to update days in stage for all active leads",
  "trigger": {
    "module": "schedule",
    "interval": "daily",
    "time": "06:00"
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "query": {
        "rules": [
          {
            "column_id": "status",
            "compare_value": ["!Won", "!Dead.*", "!Lost.*"]
          }
        ]
      }
    },
    {
      "module": "iterator",
      "array": "{{items}}"
    },
    {
      "module": "tools.calculate",
      "formula": "FLOOR((now - stage_entry_date) / 86400000)"
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

### Make.com Scenario 5c: Set First Contact Date

```json
{
  "name": "Set First Contact Date",
  "description": "When status changes from New Lead to SMS Sent, set first contact date",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status",
    "previous_value": "New Lead",
    "new_value": "SMS Sent"
  },
  "actions": [
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "date_mkycg4ew": {
          "date": "{{now | date: 'YYYY-MM-DD'}}"
        }
      }
    }
  ]
}
```

### Make.com Scenario 5d: Calculate Total Days on Close

```json
{
  "name": "Calculate Total Pipeline Days",
  "description": "When lead is Won or Lost, calculate total days in pipeline",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status",
    "value": ["Won", "Lost.*", "Dead.*"]
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
      "formula": "FLOOR((now - first_contact_date) / 86400000)"
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

## Automation 6: Competitive Win-Back Reminders

**Purpose:** When a lead goes to a competitor, set a win-back date and get reminded.

### Make.com Scenario 6a: Set Win-Back Date

```json
{
  "name": "Set Win-Back Date",
  "description": "When competitor is selected, auto-set win-back date 90 days out",
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

### Make.com Scenario 6b: Win-Back Reminder (Daily)

```json
{
  "name": "Win-Back Reminder (Daily)",
  "description": "Daily check for leads whose win-back date is today",
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
            "compare_value": "{{today}}"
          }
        ]
      }
    },
    {
      "module": "iterator",
      "array": "{{items}}"
    },
    {
      "module": "monday.createUpdate",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "body": "🔔 WIN-BACK REMINDER: It's been 90 days since {{name}} went to {{competitor_name}}. Time to check in and see how it's going!"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{item.id}}",
      "column_values": {
        "status": {
          "label": "Win-Back Attempt"
        }
      }
    }
  ]
}
```

---

## Automation 7: Re-engagement Counter

**Purpose:** Track how many times we've tried to re-engage a ghosting lead.

### Make.com Scenario

```json
{
  "name": "Increment Re-engagement Counter",
  "description": "When a re-engagement note is added, increment the counter",
  "trigger": {
    "module": "monday.watchUpdates",
    "board_id": 18390370563
  },
  "actions": [
    {
      "module": "tools.textParser",
      "input": "{{update_body}}",
      "pattern": "(re-?engage|follow.?up|checking in|ping|reaching out again)"
    },
    {
      "module": "monday.getItem",
      "condition": "pattern_matched",
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

## Automation 8: Auto-Set Referral Source

**Purpose:** Based on how the lead was added, auto-set the referral source.

### Make.com Scenario

```json
{
  "name": "Auto-Set Referral Source",
  "description": "When new item created, determine source and set it",
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

## Summary: All New Automations

### Event-Triggered (Make.com)
| # | Name | Trigger | Action |
|---|------|---------|--------|
| 1 | Calculate Lead Score | Status/Temp/Pain changes | Update Lead Score |
| 2 | Auto-Update Temperature | Status changes | Set Temperature |
| 3a | Capture Reply Time | Status → Replied | Set Reply Received At |
| 3b | Calculate Response Time | Status → Ana Engaged | Set First Response At + Response Time |
| 5a | Track Stage Entry | Any status change | Set Stage Entry Date, reset Days In Stage |
| 5c | Set First Contact Date | New Lead → SMS Sent | Set First Contact Date |
| 5d | Calculate Total Days | Status → Won/Lost | Set Total Days in Pipeline |
| 6a | Set Win-Back Date | Competitor set | Set Win-Back Date +90 days |
| 7 | Re-engagement Counter | Note with re-engage keyword | Increment counter |
| 8 | Auto-Set Referral Source | Item created | Set Referral Source from Lead Source |

### Scheduled (Make.com - Daily)
| # | Name | Schedule | Action |
|---|------|----------|--------|
| 4 | Ghost Risk Detection | Daily 8am | Update Ghost Risk for active leads |
| 5b | Days In Stage | Daily 6am | Update Days In Stage for all leads |
| 6b | Win-Back Reminder | Daily 9am | Notify on win-back date leads |

### Native Monday Alternatives
| # | Name | Can be Native? |
|---|------|---------------|
| 2 | Temperature Update | Yes - 3 separate automations |
| 3a | Capture Reply Time | Partial - date only, not time |
| 5a | Stage Entry Date | Yes - one automation |

---

## Implementation Checklist

### Phase 1: Core Automations (Do First)
- [ ] Automation 5a: Stage Entry Date on status change
- [ ] Automation 5c: First Contact Date on SMS Sent
- [ ] Automation 2: Temperature auto-update (native or Make)
- [ ] Automation 3a: Capture Reply Timestamp

### Phase 2: Daily Scheduled Jobs
- [ ] Automation 4: Ghost Risk Detection (daily)
- [ ] Automation 5b: Days In Stage update (daily)
- [ ] Automation 6b: Win-Back Reminders (daily)

### Phase 3: Advanced
- [ ] Automation 1: Lead Score calculation
- [ ] Automation 3b: Response Time calculation
- [ ] Automation 5d: Total Days on close
- [ ] Automation 6a: Auto Win-Back Date
- [ ] Automation 7: Re-engagement Counter
- [ ] Automation 8: Referral Source auto-set

---

## Testing Checklist

### Test Lead Score
- [ ] Change status → verify Lead Score updates
- [ ] Change Temperature → verify Lead Score updates
- [ ] Add pain signal → verify Lead Score increases

### Test Temperature
- [ ] New lead → verify Temperature = Cold
- [ ] Status → Replied → verify Temperature = Warm
- [ ] Status → Ask Made → verify Temperature = Hot

### Test Speed-to-Lead
- [ ] Status → Replied → verify Reply Received At set
- [ ] Status → Ana Engaged → verify First Response At set
- [ ] Verify Response Time Mins calculated correctly

### Test Ghost Risk
- [ ] Wait until daily job runs
- [ ] Check leads with old Last Meaningful Reply
- [ ] Verify Ghost Risk updated correctly

### Test Pipeline Velocity
- [ ] Change status → verify Stage Entry Date updated
- [ ] Wait for daily job → verify Days In Stage incremented
- [ ] Close lead → verify Total Days calculated

### Test Win-Back
- [ ] Set Competitor Name → verify Win-Back Date = today + 90
- [ ] On win-back date → verify notification created
