# Monday.com Dashboard Configuration

This guide walks you through setting up dashboards to track funnel performance, conversion rates, and team activity.

---

## Dashboard 1: Pipeline Overview

**Purpose:** Bird's-eye view of all leads by status.

### Widgets to Add:

#### 1. Status Distribution (Battery/Chart)
- **Type:** Chart widget
- **Chart type:** Pie or Bar
- **Column:** Status
- **Shows:** Count of leads in each status

#### 2. Leads by Source (Pie Chart)
- **Type:** Chart widget
- **Chart type:** Pie
- **Column:** Lead Source
- **Shows:** Jennica SMS vs Instantly Email distribution

#### 3. Active Pipeline Count (Numbers)
- **Type:** Numbers widget
- **Filter:** Status NOT IN (Won, Lost, Dead, Hibernation)
- **Shows:** Total active leads being worked

#### 4. This Week's Activity (Chart)
- **Type:** Chart widget
- **Column:** Last Contact Date
- **Filter:** Last 7 days
- **Shows:** Activity trend

---

## Dashboard 2: Conversion Funnel

**Purpose:** Track conversion rates between stages.

### Widgets to Add:

#### 1. Funnel Visualization
- **Type:** Chart widget
- **Chart type:** Funnel (if available) or Stacked Bar
- **Stages to show:**
  1. New Lead (total ever)
  2. SMS Sent
  3. Replied
  4. Tool Offered
  5. Meeting Scheduled
  6. Won

#### 2. Conversion Rates (Numbers)
Create separate Number widgets for each:

| Metric | Calculation |
|--------|-------------|
| Reply Rate | Replied ÷ SMS Sent |
| Tool Accept Rate | Tool Offered ÷ Replied |
| Meeting Rate | Meeting Scheduled ÷ Tool Offered |
| Close Rate | Won ÷ Meeting Scheduled |
| Overall Conversion | Won ÷ New Lead |

**Note:** Monday.com native dashboards have limited calculation ability. For true conversion rates, you may need:
- Formula columns on the board
- Export to Google Sheets for analysis
- Third-party dashboard tool (e.g., Geckoboard, Databox)

#### 3. Won This Month (Numbers)
- **Type:** Numbers widget
- **Filter:** Status = Won AND Last Contact Date = This Month
- **Shows:** Closed deals this month

#### 4. Lost/Dead Analysis (Chart)
- **Type:** Chart widget
- **Filter:** Status IN (Lost, Dead - Negative Reply, Dead - Wrong Fit)
- **Shows:** Distribution of why leads didn't convert

---

## Dashboard 3: Team Performance

**Purpose:** Track Jennica, Ana, and DJ activity.

### Widgets to Add:

#### 1. Jennica's Activity
- **Filter:** Assigned To = Jennica
- **Metrics:**
  - SMS Sent this week
  - New leads added
  - Reply rate on her outreach

#### 2. Ana's Workload
- **Filter:** Assigned To = Ana
- **Metrics:**
  - Active leads (not in endpoint status)
  - Leads awaiting response (Next Action Date = Today or Past)
  - Meetings scheduled this week

#### 3. DJ's Pipeline
- **Filter:** Status IN (Meeting Scheduled, DJ Meeting Complete, Offer Extended)
- **Metrics:**
  - Meetings this week
  - Meeting outcomes (Hot/Warm/Cool/Cold)
  - Close rate

#### 4. Stale Leads Alert
- **Type:** Table widget
- **Filter:** Next Action Date < Today AND Status NOT IN (Won, Lost, Dead, Hibernation)
- **Shows:** Leads that need attention

---

## Dashboard 4: Source Performance

**Purpose:** Compare SMS vs Email path effectiveness.

### Widgets to Add:

#### 1. Source Comparison (Side-by-side)
| Metric | Jennica SMS | Instantly Email |
|--------|-------------|-----------------|
| Total Leads | Count | Count |
| Reply/Accept Rate | % | % |
| Meetings Booked | Count | Count |
| Won | Count | Count |
| Conversion Rate | % | % |

#### 2. Time to Conversion
- **Type:** Chart widget
- **Column:** Days in Status (cumulative)
- **Group by:** Lead Source
- **Shows:** Average time from first contact to Won

#### 3. Tool Type Performance
- **Type:** Chart widget
- **Column:** Tool Type
- **Shows:** Which tools lead to most conversions

---

## Dashboard 5: Meeting Intelligence

**Purpose:** Track DJ meeting outcomes and patterns.

### Widgets to Add:

#### 1. Meeting Outcomes Distribution
- **Type:** Pie chart
- **Column:** Meeting Outcome
- **Shows:** Hot / Warm / Cool / Cold / No Show breakdown

#### 2. Timeline Distribution
- **Type:** Bar chart
- **Column:** Timeline
- **Filter:** Status = DJ Meeting Complete
- **Shows:** When leads say they'll be ready

#### 3. Common Objections (Word Cloud or Table)
- **Type:** Table or Text widget
- **Column:** Objections
- **Shows:** Recurring themes in objections

#### 4. Current Brokerage Analysis
- **Type:** Chart widget
- **Column:** Current Brokerage
- **Shows:** Which brokerages are we pulling from most

---

## Setup Instructions

### Creating a Dashboard:

1. Click **"+"** next to your board name
2. Select **"Dashboard"**
3. Name it (e.g., "Pipeline Overview")
4. Click **"Add Widget"**
5. Choose widget type (Chart, Numbers, Table, etc.)
6. Configure data source and filters

### Tips:

- **Use filters liberally** — Every widget should have clear filters
- **Date ranges matter** — Use "This Week", "This Month", "Last 30 Days" for trending
- **Refresh regularly** — Dashboards update automatically but may lag slightly
- **Mobile view** — Check how dashboards look on mobile for quick checks

### Limitations:

- Monday.com dashboards can't do complex calculations (e.g., conversion percentages)
- For advanced analytics, consider:
  - Exporting to Google Sheets weekly
  - Using a BI tool like Geckoboard or Databox
  - Building a custom dashboard with Make.com → Google Sheets → Data Studio

---

## Key Metrics to Track Weekly

| Metric | Target | Owner |
|--------|--------|-------|
| SMS sent by Jennica | 50+/week | Jennica |
| Reply rate | 10%+ | Jennica |
| Ana response time | Same day | Ana |
| Meetings scheduled | 3+/week | Ana |
| DJ close rate | 30%+ | DJ |
| Overall funnel conversion | 5%+ | Team |

---

## Sample Dashboard Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE OVERVIEW                         │
├───────────────┬───────────────┬───────────────┬─────────────┤
│ Active Leads  │ This Week     │ Won This      │ Reply Rate  │
│     47        │ Activity: 23  │ Month: 3      │    12%      │
├───────────────┴───────────────┴───────────────┴─────────────┤
│                                                              │
│  ┌──────────────────────┐  ┌──────────────────────────────┐ │
│  │   STATUS BREAKDOWN   │  │     LEADS BY SOURCE          │ │
│  │   [Pie Chart]        │  │     [Pie Chart]              │ │
│  │                      │  │                              │ │
│  │ New Lead: 12         │  │ Jennica SMS: 65%             │ │
│  │ SMS Sent: 8          │  │ Instantly: 35%               │ │
│  │ Replied: 15          │  │                              │ │
│  │ Tool Offered: 7      │  │                              │ │
│  │ Meeting Sched: 3     │  │                              │ │
│  │ Other: 2             │  │                              │ │
│  └──────────────────────┘  └──────────────────────────────┘ │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                    STALE LEADS (Action Needed)               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Name          │ Status        │ Next Action │ Days     │ │
│  │ John Smith    │ Tool Offered  │ Follow up   │ 5 days   │ │
│  │ Jane Doe      │ Ana Engaged   │ Call back   │ 3 days   │ │
│  └────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```

---

## Integration with MeetGeek

When MeetGeek is connected, the "AI Meeting Notes" column will auto-populate after each DJ meeting. Configure MeetGeek to:

1. Match meetings to Monday items by attendee email
2. Push summary to the "AI Meeting Notes" column
3. Optionally create follow-up tasks

See `docs/AI_MEETING_NOTES_SETUP.md` for detailed configuration.
