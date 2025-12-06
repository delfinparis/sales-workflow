# CRM Integration Automations

This document contains the automations needed to sync your Pipeline board with CRM Contacts and Deals.

---

## Board & Column Reference

### Board IDs
| Board | ID |
|-------|-----|
| Pipeline (Superlative Leads) | 18390370563 |
| CRM Contacts | 7569016308 |
| CRM Accounts | 7569016292 |
| CRM Deals | 7569016316 |

### Pipeline Board Key Columns
| Column | ID |
|--------|-----|
| Name | `name` |
| Email | `email_mky6p7cy` |
| Phone | `phone_mky6fr9j` |
| Status | `status` |
| Contact (link) | `board_relation_mkyahqt` |
| Account (link) | `board_relation_mkya34f` |
| Current Brokerage | `text_mky6grjs` |
| Deal Count | `numeric_mky68zwz` |
| Lead Source | `dropdown_mky6ctrz` |
| First Name | `text_mky6wn9s` |
| Last Name | `text_mky6whek` |

### CRM Contacts Key Columns
| Column | ID |
|--------|-----|
| Name | `name` |
| Email | `contact_email` |
| Phone | `contact_phone` |
| Accounts (link) | `contact_account` |
| Deals (link) | `contact_deal` |
| Current Brokerage | `text_mksa941v` |

### CRM Deals Key Columns
| Column | ID |
|--------|-----|
| Name | `name` |
| Stage | `deal_stage` |
| Deal Value | `deal_value` |
| Contacts (link) | `deal_contact` |
| Close Probability | `deal_close_probability` |
| Expected Close Date | `deal_expected_close_date` |

---

## Automation 1: Auto-Create Contact on New Pipeline Item

**Purpose:** When a new lead is added to Pipeline, automatically create or link a Contact record.

### Native Monday Automation

Go to Pipeline Board → Automate → Add Automation:

```
When an item is created
→ Create an item in Contacts board
→ And connect them in Contact column
```

**Configuration:**
1. Trigger: "When an item is created"
2. Action: "Create an item in another board"
3. Board: Contacts (7569016308)
4. Map columns:
   - Name → Name
   - Email → Email
   - Phone → Phone
   - Current Brokerage → current brokerage
5. Add action: "Connect boards"
6. Column: Contact (board_relation_mkyahqt)

### Make.com Alternative (More Control)

If native automation doesn't support all mappings, use Make.com:

```json
{
  "name": "Pipeline → Create Contact",
  "trigger": {
    "module": "monday.watchItems",
    "board_id": 18390370563
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 7569016308,
      "query": "{{email}}"
    },
    {
      "module": "monday.createItem",
      "condition": "if contact not found",
      "board_id": 7569016308,
      "item_name": "{{name}}",
      "column_values": {
        "contact_email": "{{email}}",
        "contact_phone": "{{phone}}",
        "text_mksa941v": "{{current_brokerage}}"
      }
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "board_relation_mkyahqt": "{{contact_item_id}}"
      }
    }
  ]
}
```

---

## Automation 2: Create Deal on Won Status

**Purpose:** When Pipeline status changes to "Won", create a Deal record.

### Native Monday Automation

Go to Pipeline Board → Automate → Add Automation:

```
When Status changes to "Won"
→ Create an item in Deals board
→ And connect the Contact
```

**Configuration:**
1. Trigger: "When status changes to something"
2. Status value: Won (index 16)
3. Action: "Create an item in another board"
4. Board: Deals (7569016316)
5. Map columns:
   - Name → "{Name} - Kale Realty"
   - Deal Value → (calculate from Deal Count × average commission)
   - Close Probability → 100
   - Expected Close Date → Today
6. Action: "Connect boards" (link Contact to Deal)

### Make.com Scenario

```json
{
  "name": "Won → Create Deal",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "status",
    "value": "Won"
  },
  "actions": [
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}"
    },
    {
      "module": "monday.createItem",
      "board_id": 7569016316,
      "item_name": "{{name}} - Kale Realty",
      "column_values": {
        "deal_value": "{{deal_count * 5000}}",
        "deal_close_probability": 100,
        "deal_expected_close_date": "{{today}}",
        "deal_stage": "Won"
      }
    },
    {
      "module": "monday.updateItem",
      "note": "Link Contact to Deal",
      "board_id": 7569016308,
      "item_id": "{{contact_item_id}}",
      "column_values": {
        "contact_deal": "{{deal_item_id}}"
      }
    }
  ]
}
```

---

## Automation 3: Duplicate Check on New Item

**Purpose:** When a new Pipeline item is created, check if the email/phone already exists.

### Make.com Scenario (Required - Native can't do this well)

```json
{
  "name": "Duplicate Check",
  "trigger": {
    "module": "monday.watchItems",
    "board_id": 18390370563
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 18390370563,
      "query": "{{email}}",
      "exclude_id": "{{trigger_item_id}}"
    },
    {
      "module": "tools.ifCondition",
      "condition": "results.length > 0"
    },
    {
      "module": "monday.updateItem",
      "if_true": true,
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "long_text_mky6bj1v": "⚠️ DUPLICATE: This email exists on item {{duplicate_item_id}}"
      }
    },
    {
      "module": "slack.sendMessage",
      "if_true": true,
      "channel": "#leads",
      "message": "Duplicate lead detected: {{name}} ({{email}}) - already exists as {{duplicate_item_name}}"
    }
  ]
}
```

---

## Automation 4: Sync Contact Updates

**Purpose:** When contact info changes in Pipeline, update the Contact record.

### Native Monday Automation

```
When Email changes
→ Mirror to connected Contact
```

**Note:** This may happen automatically if you set up two-way connection. Test first.

### Make.com Scenario (if needed)

```json
{
  "name": "Sync Contact Updates",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "columns": ["email_mky6p7cy", "phone_mky6fr9j"]
  },
  "actions": [
    {
      "module": "monday.getItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "columns": ["board_relation_mkyahqt"]
    },
    {
      "module": "monday.updateItem",
      "board_id": 7569016308,
      "item_id": "{{contact_id}}",
      "column_values": {
        "contact_email": "{{new_email}}",
        "contact_phone": "{{new_phone}}"
      }
    }
  ]
}
```

---

## Automation 5: Link to Existing Account (Brokerage)

**Purpose:** When Current Brokerage is set, find or create the Account record.

### Make.com Scenario

```json
{
  "name": "Link Brokerage Account",
  "trigger": {
    "module": "monday.watchColumnValues",
    "board_id": 18390370563,
    "column_id": "text_mky6grjs"
  },
  "actions": [
    {
      "module": "monday.searchItems",
      "board_id": 7569016292,
      "query": "{{current_brokerage}}"
    },
    {
      "module": "tools.ifCondition",
      "condition": "results.length === 0"
    },
    {
      "module": "monday.createItem",
      "if_true": true,
      "board_id": 7569016292,
      "item_name": "{{current_brokerage}}"
    },
    {
      "module": "monday.updateItem",
      "board_id": 18390370563,
      "item_id": "{{trigger_item_id}}",
      "column_values": {
        "board_relation_mkya34f": "{{account_item_id}}"
      }
    }
  ]
}
```

---

## Native Monday Automations Summary

Set these up in Pipeline Board → Automate:

| # | Trigger | Action |
|---|---------|--------|
| 1 | Item created | Create Contact + Connect |
| 2 | Status → Won | Create Deal + Connect |
| 3 | Status → Won | Notify team (Slack/Email) |
| 4 | Email changes | Update connected Contact (if not auto) |

---

## Make.com Scenarios Summary

Create these in Make.com:

| # | Name | Trigger | Purpose |
|---|------|---------|---------|
| 1 | Pipeline → Contact | New Pipeline item | Create/link Contact with duplicate check |
| 2 | Won → Deal | Status = Won | Create Deal with revenue calculation |
| 3 | Duplicate Check | New Pipeline item | Flag duplicates in Notes |
| 4 | Sync Contact | Email/Phone change | Update Contact record |
| 5 | Link Account | Brokerage set | Find/create Account record |

---

## Testing Checklist

### Test 1: New Lead Flow
- [ ] Create new item in Pipeline
- [ ] Verify Contact created in Contacts board
- [ ] Verify Contact column linked in Pipeline
- [ ] Check for duplicate detection if email exists

### Test 2: Won Flow
- [ ] Change Pipeline status to Won
- [ ] Verify Deal created in Deals board
- [ ] Verify Deal linked to Contact
- [ ] Check Deal Value calculation

### Test 3: Account Linking
- [ ] Set Current Brokerage on Pipeline item
- [ ] Verify Account created (if new) or found (if exists)
- [ ] Verify Account column linked in Pipeline

### Test 4: Data Sync
- [ ] Update Email in Pipeline
- [ ] Verify Contact email updated
- [ ] Update Phone in Pipeline
- [ ] Verify Contact phone updated

---

## Estimated Deal Value Calculation

For the "Won → Deal" automation, calculate Deal Value based on Deal Count:

| Deal Count | Estimated Annual GCI | Deal Value |
|------------|---------------------|------------|
| 2-4 deals | $20,000 - $40,000 | $30,000 |
| 5-7 deals | $50,000 - $70,000 | $60,000 |
| 8-12 deals | $80,000 - $120,000 | $100,000 |

Formula: `Deal Value = Deal Count × $10,000` (adjust based on your actual averages)

This gives you pipeline forecasting in the Deals board.
