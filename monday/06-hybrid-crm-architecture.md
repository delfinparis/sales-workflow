# Hybrid CRM Architecture

This document describes the integration between Monday CRM's core entity boards and your custom Pipeline board.

---

## Board IDs Reference

| Board | ID | Purpose |
|-------|-----|---------|
| **Pipeline (Superlative Leads)** | 18390370563 | Primary workspace - Jennica/Ana/DJ workflow |
| **CRM Leads** | 7569016272 | Intake for non-Courted sources |
| **CRM Contacts** | 7569016308 | Master contact database |
| **CRM Accounts** | 7569016292 | Companies/Brokerages |
| **CRM Deals** | 7569016316 | Won deals & revenue tracking |
| **CRM Activities** | 7569016282 | Activity logging |

## Connection Column IDs (Pipeline Board)

| Column | ID | Connects To |
|--------|-----|-------------|
| Contact | `board_relation_mkyahqt` | CRM Contacts |
| Account | `board_relation_mkya34f` | CRM Accounts |

---

## Architecture Overview

```
                         MONDAY CRM CORE BOARDS
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │   ┌─────────────┐      ┌─────────────┐      ┌───────────┐  │
    │   │   LEADS     │      │  CONTACTS   │      │  ACCOUNTS │  │
    │   │   BOARD     │─────▶│   BOARD     │◀────▶│   BOARD   │  │
    │   │             │      │             │      │           │  │
    │   │ - Intake    │      │ - Master    │      │ - Company │  │
    │   │ - Scoring   │      │   database  │      │   records │  │
    │   │ - Duplicate │      │ - All leads │      │           │  │
    │   │   detection │      │   ever      │      │           │  │
    │   └──────┬──────┘      └─────────────┘      └───────────┘  │
    │          │                    ▲                            │
    │          │ Qualified          │ Sync                       │
    │          │ (Auto)             │ (Auto)                     │
    │          ▼                    │                            │
    └─────────────────────────────────────────────────────────────┘
              │                     │
              │                     │
              ▼                     │
    ┌─────────────────────────────────────────────────────────────┐
    │              YOUR CUSTOM PIPELINE BOARD                     │
    │                                                             │
    │   ┌───────────────────────────────────────────────────────┐ │
    │   │                JENNICA → ANA → DJ                     │ │
    │   │                                                       │ │
    │   │  New Lead → SMS Sent → Replied → Tool Offered → ...   │ │
    │   │                    ↓                                  │ │
    │   │              30-Day Timeout                           │ │
    │   │                    ↓                                  │ │
    │   │              Hibernation                              │ │
    │   │                                                       │ │
    │   │  [22 Custom Views for Jennica/Ana/DJ workflows]      │ │
    │   └───────────────────────────────────────────────────────┘ │
    │                          │                                  │
    │                          │ Won                              │
    │                          ▼                                  │
    └─────────────────────────────────────────────────────────────┘
              │
              │ Auto-create
              ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                       DEALS BOARD                           │
    │                                                             │
    │   - Deal Value (estimated commission)                       │
    │   - Close Probability                                       │
    │   - Forecast Value                                          │
    │   - Revenue tracking                                        │
    │   - Pipeline analytics                                      │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## Board Purposes

### 1. CRM Leads Board (Intake)
**Purpose:** Initial capture and qualification before entering pipeline

| What it does | Why use it |
|--------------|-----------|
| Capture from Courted.ai / Instantly | Centralized intake |
| Auto lead scoring | Prioritize high-value targets |
| Duplicate detection | Prevent contacting same person twice |
| "Existing account" indicator | Know if they're already in system |
| Basic qualification | Filter before entering pipeline |

**Columns to use:**
- Name, Email, Phone (default)
- Company (default)
- Lead Score (default - auto-calculated)
- Indications (default - duplicate/existing detection)
- Lead Source (add: Jennica SMS / Instantly Email)
- Deal Count (add: from Courted data)
- Courted Profile URL (add)

**Statuses:**
- New (just entered)
- Qualified → triggers move to Pipeline Board
- Unqualified → archive

---

### 2. Custom Pipeline Board (Your 22 Views)
**Purpose:** Active workflow management for Jennica → Ana → DJ

This is your existing board with all the detailed statuses:
- New Lead, SMS Sent, 30-Day Timeout
- Replied, Tool Offered, Training Invited
- Relationship Building, Ask Made
- Meeting Scheduled, DJ Meeting Complete
- Offer Extended, Nurture
- Won, Lost (3 types), Dead, Hibernation

**Connected to:**
- CRM Contacts Board (mirror contact info)
- CRM Accounts Board (mirror company info)
- CRM Deals Board (create deal when Won)

---

### 3. CRM Contacts Board (Master Database)
**Purpose:** Permanent record of every qualified contact

| What it stores | Why |
|----------------|-----|
| Contact info (name, email, phone) | Single source of truth |
| Link to Account | Company relationship |
| Activity history | Full timeline |
| All interactions | Audit trail |

**Sync from Pipeline Board:**
- When lead enters Pipeline → create/link Contact
- Updates sync bidirectionally

---

### 4. CRM Accounts Board (Companies)
**Purpose:** Company-level data (brokerages)

| What it stores | Why |
|----------------|-----|
| Brokerage name | Group agents by company |
| Company details | Industry intelligence |
| Multiple contacts per account | See all agents from same brokerage |

---

### 5. CRM Deals Board (Revenue)
**Purpose:** Track won deals and revenue forecasting

| What it stores | Why |
|----------------|-----|
| Deal Value | Estimated commission value |
| Close Probability | For forecasting |
| Forecast Value | Deal Value × Probability |
| Close Date | When they signed |
| Source attribution | Which channel won |

**Auto-created when:** Pipeline status → Won

---

## Data Flow

### Flow 1: New Lead Intake (Courted.ai / Instantly)

```
Courted.ai detects superlative
         │
         ▼
┌─────────────────────┐
│    CRM LEADS BOARD  │
│                     │
│ 1. Check duplicates │ ──▶ Already exists? Skip or merge
│ 2. Auto lead score  │
│ 3. Qualify          │
└─────────────────────┘
         │
         │ Status → Qualified
         ▼
┌─────────────────────┐
│   PIPELINE BOARD    │
│                     │
│ Status: New Lead    │
│ Assigned: Jennica   │
│ Contact: [linked]   │
└─────────────────────┘
         │
         │ (Auto)
         ▼
┌─────────────────────┐     ┌─────────────────────┐
│   CONTACTS BOARD    │────▶│   ACCOUNTS BOARD    │
│                     │     │                     │
│ - Name              │     │ - Brokerage name    │
│ - Email             │     │                     │
│ - Phone             │     │                     │
│ - Pipeline link     │     │                     │
└─────────────────────┘     └─────────────────────┘
```

### Flow 2: Pipeline to Won

```
┌─────────────────────┐
│   PIPELINE BOARD    │
│                     │
│ Status: DJ Meeting  │
│ Complete            │
│         │           │
│         ▼           │
│ Status → Won        │
└─────────────────────┘
         │
         │ (Auto)
         ▼
┌─────────────────────┐
│    DEALS BOARD      │
│                     │
│ Deal Value: $X      │
│ Close Date: Today   │
│ Contact: [linked]   │
│ Source: Jennica SMS │
└─────────────────────┘
```

### Flow 3: Hibernation Return

```
┌─────────────────────┐
│   PIPELINE BOARD    │
│                     │
│ Status: Hibernation │
│ 90-Day              │
│         │           │
│  (90 days pass)     │
│         │           │
│         ▼           │
│ Status → New Lead   │ ──▶ Contact Board unchanged
│                     │     (still has history)
└─────────────────────┘
```

---

## Connection Setup

### Step 1: Connect Pipeline Board to Contacts

```graphql
# Add Connect Boards column to Pipeline Board
mutation {
  create_column(
    board_id: 18390370563
    title: "Contact"
    column_type: board_relation
    defaults: "{\"boardIds\":[CONTACTS_BOARD_ID]}"
  ) { id }
}
```

### Step 2: Connect Pipeline Board to Accounts

```graphql
# Add Connect Boards column to Pipeline Board
mutation {
  create_column(
    board_id: 18390370563
    title: "Account"
    column_type: board_relation
    defaults: "{\"boardIds\":[ACCOUNTS_BOARD_ID]}"
  ) { id }
}
```

### Step 3: Mirror Key Fields from Contacts

After connecting, add Mirror columns to pull:
- Email (from Contacts)
- Phone (from Contacts)
- Account Name (from Contacts → Account)

---

## Automations Required

### Automation 1: Leads → Pipeline (on Qualified)

**Trigger:** CRM Leads Board status → Qualified

**Actions:**
1. Create item in Pipeline Board with:
   - Name = Lead name
   - Status = New Lead
   - Lead Source = [from leads board]
   - Deal Count = [from leads board]
   - Courted Profile = [from leads board]
2. Create/find Contact in Contacts Board
3. Link Contact to Pipeline item
4. Link Account to Pipeline item (if exists)

**Platform:** Make.com (CRM board automations are limited)

### Automation 2: Pipeline → Contacts Sync

**Trigger:** New item in Pipeline Board

**Actions:**
1. Check if Contact exists (by email)
2. If not, create Contact with:
   - Name, Email, Phone
   - Account link (by company name)
3. Link Contact to Pipeline item

**Platform:** Make.com

### Automation 3: Won → Deals

**Trigger:** Pipeline status → Won

**Actions:**
1. Create Deal in Deals Board with:
   - Name = "[Contact Name] - Kale Realty"
   - Deal Value = [estimate from Deal Count]
   - Close Probability = 100%
   - Close Date = Today
   - Contact = [linked]
   - Source = Lead Source
2. Update Contact status

**Platform:** Native Monday or Make.com

### Automation 4: Contact Info Sync

**Trigger:** Email or Phone changes in Pipeline Board

**Actions:**
1. Update linked Contact record

**Platform:** Native Monday (via Mirror columns or automation)

---

## Column Mapping

### CRM Leads Board → Pipeline Board

| Leads Board Column | Pipeline Board Column | Sync Direction |
|-------------------|----------------------|----------------|
| Name | Name | → |
| Email | Email | → |
| Phone | Phone | → |
| Company | Current Brokerage | → |
| Lead Score | Priority | → (mapped) |
| Lead Source (add) | Lead Source | → |
| Deal Count (add) | Deal Count | → |
| Courted Profile (add) | Courted Profile | → |

### Pipeline Board → Contacts Board

| Pipeline Column | Contacts Column | Sync Direction |
|----------------|-----------------|----------------|
| Name | Name | ↔ |
| Email | Email | ↔ |
| Phone | Phone | ↔ |
| Current Brokerage | Account (link) | → |

### Pipeline Board → Deals Board

| Pipeline Column | Deals Column | Sync Direction |
|----------------|--------------|----------------|
| Name | Deal Name | → |
| Deal Count | Deal Value (calculated) | → |
| Lead Source | Source | → |
| Won Date | Close Date | → |
| Contact (link) | Contact (link) | → |

---

## Implementation Checklist

### Phase 1: Board Setup

- [ ] Get CRM Leads Board ID
- [ ] Get CRM Contacts Board ID
- [ ] Get CRM Accounts Board ID
- [ ] Get CRM Deals Board ID
- [ ] Add custom columns to Leads Board:
  - [ ] Lead Source (dropdown)
  - [ ] Deal Count (number)
  - [ ] Courted Profile URL (link)

### Phase 2: Connections

- [ ] Add "Contact" Connect Boards column to Pipeline Board
- [ ] Add "Account" Connect Boards column to Pipeline Board
- [ ] Add Mirror columns for Email, Phone from Contact
- [ ] Test connections work

### Phase 3: Automations

- [ ] Build Make.com scenario: Leads → Pipeline (on Qualified)
- [ ] Build Make.com scenario: Pipeline → Contact Sync
- [ ] Build automation: Won → Create Deal
- [ ] Test all automations

### Phase 4: Views & Dashboards

- [ ] Add "Lead Score" view to Pipeline Board
- [ ] Update dashboards to include Deals revenue data
- [ ] Create Contacts Board view for "Active Pipeline Contacts"

---

## Benefits of Hybrid Approach

| Feature | Custom Only | Hybrid |
|---------|-------------|--------|
| Lead scoring | Manual | Auto |
| Duplicate detection | Manual | Auto |
| Contact history | Limited | Full |
| Company grouping | None | Accounts |
| Revenue tracking | Basic | Full forecasting |
| Your custom workflow | Yes | Yes |
| 22 role-based views | Yes | Yes |
| Timeout/hibernation | Yes | Yes |

---

## What You Keep

Your custom Pipeline Board keeps:
- All 22 views (Jennica, Ana, DJ workflows)
- All custom statuses (New Lead → Won/Lost/Dead/Hibernation)
- All custom columns (Timeout Count, No Show Count, etc.)
- All automations (Make.com scenarios)
- Do Not Contact checkbox logic
- Meeting prep reminders
- Offer follow-up cadence

---

## What You Gain

From CRM integration:
- **Lead Scoring:** Auto-prioritize based on title, company size, deal count
- **Duplicate Detection:** Never SMS the same person twice by accident
- **Existing Account Warning:** Know if they're already in your system
- **Master Contact Database:** Every lead ever, with full history
- **Company Intelligence:** See all agents from same brokerage
- **Revenue Forecasting:** Deal Value × Probability projections
- **Pipeline Analytics:** Built-in CRM dashboards
