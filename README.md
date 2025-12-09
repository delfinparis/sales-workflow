# Kale Realty Sales Workflow

Agent recruiting CRM and automation system for Kale Realty, powered by Monday.com, Make.com, and integrated tools.

## Overview

This system manages the agent recruiting pipeline with a structured handoff workflow:

```
Jennica (Research) -> Ana (Qualification) -> DJ (Closing)
```

### Team Roles

| Role | Person | Responsibility |
|------|--------|----------------|
| Research & Data Entry | Jennica | Courted lookups, lead enrichment, initial outreach |
| Qualification | Ana | Conversations, scheduling, nurturing |
| Closing | DJ | Recruiting meetings, offers, final decisions |
| Newly Licensed Leads | Rea | AMP program leads (separate board) |

## Tech Stack

- **CRM**: Monday.com (2 boards)
- **Automations**: Make.com (17 scenarios)
- **Phone/SMS**: JustCall
- **Scheduling**: Calendly
- **Cold Email**: Instantly
- **Training Docs**: Notion (synced from GitHub)

## Monday.com Boards

| Board | ID | Purpose |
|-------|-----|---------|
| Superlative Leads | `18390370563` | Main recruiting pipeline (Jennica/Ana/DJ) |
| Newly Licensed Leads | `18391158354` | AMP program leads (Rea) |
| JustCall Calls | `18387583881` | Call logging |
| JustCall SMS | `18387583880` | SMS logging |

## Repository Structure

```
docs/
  TRAINING_JENNICA.md    # Jennica's training guide
  TRAINING_ANA.md        # Ana's training guide
  TRAINING_REA.md        # Rea's training guide
  TRAINING_DJ.md         # DJ's training guide
  make-automations-batch2.md  # Make.com scenario documentation

scripts/
  import-to-monday.py         # Import leads from Close CRM
  backfill-activities.py      # Add activity history to Monday
  sync-close-status.py        # Sync statuses from Close
  sync-close-tasks.py         # Sync tasks from Close
  sync-close-fields.py        # Sync custom fields from Close
  sync-to-notion.py           # Sync training docs to Notion
  export-close-*.py           # Export scripts for Close data

notion/
  NOTION_SETUP.md        # Notion integration setup guide
```

## Make.com Automations

17 scenarios across 5 batches:

| Batch | Scenarios | Purpose |
|-------|-----------|---------|
| 1 | 1-8 | Core CRM (timestamps, ghost detection) |
| 2 | 9-11 | Lead scoring, days tracking |
| 3 | 12-15 | Win-back, re-engagement, referrals |
| 4 | 16 | Gmail/Gemini meeting notes |
| 5 | 17 | Instantly cold email responses |

See [make-automations-batch2.md](docs/make-automations-batch2.md) for full documentation.

## Key Integrations

### Instantly (Cold Email)
- Webhook fires when leads reply "interested"
- Routes to existing lead owner or creates new lead
- New leads assigned to Jennica for Courted lookup

### JustCall (Phone/SMS)
- Two-way sync with Monday.com
- Calls and SMS linked to lead records

### Calendly (Scheduling)
- Booking triggers Monday status updates
- Creates activity log entries

### Gemini (Meeting Notes)
- Auto-captures meeting notes from Gmail
- Posts to Monday lead updates

## Getting Started

### Prerequisites
- Python 3.8+
- `pip install requests notion-client`

### Environment Variables
```bash
NOTION_TOKEN=ntn_xxxxx  # For Notion sync
```

### Running Scripts
```bash
# Sync training docs to Notion
cd scripts && NOTION_TOKEN="your_token" python3 sync-to-notion.py

# Import from Close CRM (one-time)
python3 import-to-monday.py

# Backfill activities
python3 backfill-activities.py --board both
```

## Status Workflow

### Superlative Board (22 statuses)
Key statuses in pipeline order:
1. New Lead
2. Replied - Awaiting Ana
3. Ana Engaged
4. DJ Meeting Scheduled
5. DJ Meeting Complete
6. Offer Extended
7. Won / Lost - Competitor

### Newly Licensed Board (12 statuses)
Key statuses:
1. New Lead
2. In Workflow
3. Appointment Scheduled
4. Won / Chose Another Firm

## Documentation

- **Training Guides**: See `docs/TRAINING_*.md`
- **Make.com Setup**: See `docs/make-automations-batch2.md`
- **Notion Sync**: See `notion/NOTION_SETUP.md`
- **Session Log**: See `SESSION_LOG.md` for development history

## Contributing

This is a private repository for Kale Realty internal use.

---

Built with Monday.com, Make.com, and Claude Code.
