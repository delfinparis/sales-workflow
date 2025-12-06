# Jennica Superlative Leads Workflow - Deployment Guide

## Overview

This package contains everything needed to deploy the Jennica Superlative Leads workflow:

- **Monday.com CRM board structure** with all statuses, columns, and views
- **Make.com automation scenarios** for JustCall integration, status triggers, and notifications
- **Python utility scripts** for batch operations and data management

## Prerequisites

Before deploying, ensure you have:

1. **Monday.com CRM** subscription (not just Work Management)
2. **Make.com** account with sufficient operations
3. **JustCall** account with API access
4. **API Tokens:**
   - Monday.com: Admin > Connections > API
   - Make.com: Profile > API Access > Create Token
   - JustCall: Settings > API Keys

---

## Part 1: Monday.com Setup

### Step 1: Create the Leads Board

1. Go to Monday.com CRM
2. Create a new board called "Jennica Superlative Leads"
3. Open the **API Playground** (developers.monday.com/apps/playground)
4. Run the GraphQL mutations in `monday/01-create-columns.graphql`

### Step 2: Configure Columns

The board requires these columns (created via GraphQL or manually):

| Column | Type | Purpose |
|--------|------|---------|
| **CORE FIELDS** | | |
| Status | Status | Pipeline stage (18 statuses) |
| Lead Source | Dropdown | Jennica SMS / Instantly Email / Both |
| Priority | Dropdown | High (8-12 deals) / Medium (5-7) / Low (2-4) |
| Phone | Phone | Lead's phone number |
| Email | Email | Lead's email address |
| Assigned To | People | Jennica, Ana, or DJ |
| **TRACKING DATES** | | |
| First Contact Date | Date | When lead first entered funnel (set once) |
| Last Contact Date | Date | Most recent touch |
| Last Superlative Date | Date | When Jennica last sent congrats SMS |
| Next Action Date | Date | Scheduled follow-up |
| Next Action | Text | What to do next |
| **LEAD CONTEXT** | | |
| Superlative Type | Dropdown | New Listing / Pending / Closed Sale / Closed Rental / YoY Growth |
| Courted Profile | Link | Link to Courted.ai profile |
| Deal Count | Number | Annual transactions (2-12 range) |
| Notes | Long Text | Manual observations and history |
| Current Tasks | Long Text | Auto-populated prompts for current stage |
| **TIMEOUT & HIBERNATION** | | |
| Timeout Until | Date | For 30-day pause periods |
| Timeout Count | Number | How many times lead has timed out (3 = auto-hibernate) |
| Hibernation Until | Date | For 90-day cool-off periods |
| Do Not Contact | Checkbox | ⚠️ Jennica checks before SMS |
| **DEAD LEAD REVIEW** | | |
| Dead Until | Date | 1-year exclusion for negative replies |
| Review Eligible | Checkbox | Auto-checked when Dead Until passes |
| **CALENDLY INTEGRATION** | | |
| Meeting Date | Date | Auto-populated by Calendly app |
| Meeting URL | Link | Zoom/Meet link from Calendly |
| Calendly Cancel Link | Link | Link for lead to cancel |
| Calendly Reschedule Link | Link | Link for lead to reschedule |
| **INSTANTLY EMAIL** | | |
| Emailed By | Text | Instantly persona who emailed them |
| Tool Type | Dropdown | Which tool was offered |
| Voice Memo Sent | Checkbox | Ana checks after sending voice memo |
| **DJ MEETING FIELDS** | | |
| No Show Count | Number | Meeting no-shows (2 = auto-hibernate) |
| Meeting Outcome | Dropdown | Hot / Warm / Cool / Cold |
| Current Brokerage | Text | Where they hang their license |
| Why Considering Change | Long Text | Their pain points |
| Business Goals | Long Text | What they want to achieve |
| Timeline | Dropdown | When they might move |
| Objections | Long Text | Concerns raised in meeting |
| AI Meeting Notes | Long Text | Auto-populated by MeetGeek or Google Gemini |
| Lost Reason | Dropdown | Why lead was lost (for analysis) |

### Step 3: Configure Status Labels

Update the Status column with these labels (in order):

**Phase 1 - Jennica:**
- `New Lead` (gray)
- `SMS Sent` (light blue)
- `30-Day Timeout` (orange)

**Phase 2 - Ana:**
- `Replied - Awaiting Ana` (purple)
- `Ana Engaged` (blue)
- `Tool Offered` (teal)
- `Tool Engaged` (green)
- `Training Invited` (lime)
- `Pain Point Identified` (yellow)
- `Relationship Building` (gold)
- `Ask Made` (orange)
- `Meeting Scheduled` (red)
- `DJ Meeting Complete` (maroon)

**Endpoints:**
- `Won` (dark green)
- `Lost - Not Interested` (dark gray)
- `Lost - Competitor` (dark red)
- `Lost - Not Qualified` (brown)
- `Dead - Negative Reply` (black)
- `Hibernation 90-Day` (light gray)

### Step 4: Create Views

Create these saved views:

1. **Jennica - Today's Hunt**
   - Filter: Status = "New Lead" AND Do Not Contact = unchecked
   - Sort: Last Contact Date (oldest first)
   - Columns: Name, Phone, Superlative Type, Courted Profile, Deal Count, Do Not Contact

2. **Jennica - Timeout Ending**
   - Filter: Status = "30-Day Timeout" AND Timeout Until <= Today
   - Sort: Timeout Until (oldest first)

3. **Ana - New Replies**
   - Filter: Status = "Replied - Awaiting Ana"
   - Sort: Last Contact Date (newest first)

4. **Ana - Today's Callbacks**
   - Filter: Next Action Date = Today
   - Sort: Next Action Date

5. **Ana - All Active**
   - Filter: Status NOT IN (Won, Lost*, Dead*, Hibernation*, New Lead, SMS Sent, 30-Day Timeout)
   - Group by: Status

6. **Pipeline Overview**
   - All items, grouped by Status
   - Show counts

### Step 5: Create Automations (Native Monday)

These automations run natively in Monday:

**Auto-assign Jennica for new leads:**
```
When Status changes to "SMS Sent"
→ Assign Jennica to Assigned To
→ Set Last Contact Date to Today
```

**Auto-assign Ana on reply:**
```
When Status changes to "Replied - Awaiting Ana"
→ Assign Ana to Assigned To
→ Notify Ana via email
```

**Timeout expiration check (daily):**
```
Every day at 8am
→ Find items where Status = "30-Day Timeout" AND Timeout Until <= Today
→ Change Status to "New Lead"
```

---

## Part 2: Calendly Event Management App

The Calendly Event Management app syncs meetings between Calendly and Monday.com. When a lead books with Ana or DJ, it auto-updates the Monday record.

### Prerequisites

- **Calendly Standard plan** (or higher) — free plan doesn't support webhooks
- **Monday.com CRM** with the board created
- **$12/month** for the Calendly Event Management app (14-day free trial)

### Step 1: Install the App

1. Go to Monday.com marketplace
2. Search for "Calendly Event Management"
3. Click Install
4. Select the workspace where your Leads board lives
5. Grant required permissions

### Step 2: Connect Calendly Account

1. You must be **Owner or Admin** in Calendly (User role won't work)
2. Go to your Leads board > Click "Integrate" (top right)
3. Find Calendly Event Management in Templates tab
4. Click to authenticate with Calendly
5. Grant permissions

### Step 3: Configure "New Event" Automation

Set up: **When new event scheduled find it by email and update or create an item**

This finds existing leads by email and updates their meeting info.

**Mapping configuration:**

| Calendly Field | Monday Column |
|----------------|---------------|
| Name | (item name) |
| Email | Email |
| The moment the event was scheduled to start | Meeting Date |
| Meeting url | Meeting URL |
| Cancel event link | Calendly Cancel Link |
| Reschedule event link | Calendly Reschedule Link |

**Also set:**
- Status → "Meeting Scheduled" (on update)

### Step 4: Configure "Rescheduled" Automation

Set up: **When event rescheduled, update an item**

**Mapping:**
- Update Meeting Date
- Update Meeting URL (in case it changed)

### Step 5: Configure "Canceled" Automation

Set up: **When event canceled set status to something**

- Set Status → "Relationship Building" (they canceled, Ana re-engages)

### Step 6: Configure "No Show" Automation (IMPORTANT)

Set up: **When status changes to "No Show" marks Calendly scheduled event as a No Show**

This is the key automation — when DJ marks `No Show` in Monday, it automatically marks the no-show in Calendly too. **DJ only needs to update Monday, not both systems.**

**How it works:**
1. Meeting happens (or doesn't)
2. DJ changes Monday status: `Meeting Scheduled` → `No Show`
3. App automatically marks it as no-show in Calendly
4. Our Make.com automation handles the rest (notify Ana, track count, etc.)

### Step 7: Test the Integration

1. **Test booking:** Have someone book a test meeting via Calendly
2. **Verify:** Check that Monday item was found/created with meeting details
3. **Test reschedule:** Reschedule the meeting, verify Monday updates
4. **Test cancel:** Cancel the meeting, verify status changes
5. **Test no-show:** Change status to "No Show", verify Calendly reflects it

### Troubleshooting

**"Permission Denied" error when connecting:**
- You must be Owner or Admin in Calendly
- Check your role at: calendly.com/app/organization/users

**Item not created when event scheduled:**
- Verify the automation is active in Board Integrations
- Check Calendly plan is Standard or higher (not free)
- Check Integration Activity for error details

**Meeting URL not populated:**
- Ensure your Calendly event type has a meeting platform configured (Zoom, Google Meet, etc.)

---

## Part 3: Instantly Email Integration

Instantly handles cold email outreach with tool offers. When a lead replies "yes" and is marked interested, it syncs to Monday.

### Overview

```
Instantly Campaign (monthly tool offer email)
    ↓
Lead replies "yes"
    ↓
Team marks lead as "interested" in Instantly
    ↓
Instantly webhook fires → Make.com → Monday
    ↓
Monday: Status = Tool Offered, Ana notified, tasks created
    ↓
Ana sends intro SMS + voice memo
    ↓
Regular flow continues (Relationship Building → Ask → Meeting)
```

### Prerequisites

- **Instantly account** with API access (v2)
- **Make.com** with webhook capability
- **Leads bulk-imported to Monday** before campaign runs (matched by email)

### Step 1: Create Instantly API Key

1. Go to Instantly > Settings > Integrations > API
2. Create a new API key with scopes: `webhooks:all`, `emails:read`
3. Save the key securely

### Step 2: Create Instantly Webhook

**Option A: Via API**
```bash
curl -X POST https://api.instantly.ai/api/v2/webhooks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "target_hook_url": "YOUR_MAKE_WEBHOOK_URL",
    "event_type": "lead_interested"
  }'
```

**Option B: Via Instantly UI**
1. Go to Settings > Integrations > Webhooks
2. Add Webhook
3. Paste your Make.com webhook URL
4. Select event type: `lead_interested`

### Step 3: Import Make.com Scenario

1. Import `make/11-instantly-lead-interested.json`
2. Create a Custom Webhook in Make.com, copy the URL
3. Use that URL when creating the Instantly webhook
4. Replace placeholders:
   - `YOUR_BOARD_ID` - Monday board ID
   - `ANA_USER_ID` - Ana's Monday user ID
5. Configure connections (Monday, Email, Slack)

### Step 4: Configure Column Mapping

The scenario updates these columns when a lead says "yes":

| Column | Value |
|--------|-------|
| Status | Tool Offered |
| Lead Source | Instantly Email |
| Emailed By | Persona name (extracted from email) |
| Assigned To | Ana |
| Next Action | Send intro SMS + voice memo |
| Next Action Date | Today |
| Response Suggestions | Intro SMS template + tasks |
| Notes (Update) | Full email thread + Instantly link |

### Step 5: Test the Integration

1. Have a test lead in Monday (with email)
2. Send them a test email via Instantly
3. Reply "yes" from that email
4. Mark them as "interested" in Instantly Unibox
5. Verify Monday updates: status, assigned to, notes, etc.
6. Verify Ana gets Slack notification

### Collision Handling

**If lead is already being worked by Ana:**
- Status does NOT change
- A note is added: "FYI - this lead also received tool via email"
- Ana is notified but existing flow continues

**If lead is NOT found in Monday:**
- Ana is emailed with instructions to add manually
- Includes: lead email, persona, their reply, Instantly link

### Ana's Workflow for Instantly Leads

When notified of a new Instantly lead:

1. **Same day:** Send intro SMS
   ```
   Hi! [Persona] from our team just sent over the [tool] via email! 
   I'm Ana @ Kale (I work with D.J.) and I'll be reaching out 
   in the next few days to get your feedback! Thanks! :)
   ```

2. **Same day:** Send voice memo introducing herself

3. **Set follow-up date:** 2-4 days out

4. **Follow up:** Call for feedback → Relationship Building → regular flow

---

## Part 4: Make.com Setup

### Step 1: Import Scenarios

1. Go to Make.com > Scenarios
2. Click "..." menu > Import Blueprint
3. Import each JSON file from `make/` folder:
   - `01-juscall-sms-sent.json` - Tracks outbound SMS
   - `02-juscall-reply-received.json` - Handles incoming replies
   - `03-status-change-notifications.json` - Slack/email alerts
   - `04-hibernation-manager.json` - 90-day hibernation logic

### Step 2: Configure Connections

For each imported scenario, you'll need to configure:

**JustCall Connection:**
1. Click any JustCall module
2. Add connection > Enter API Key and Secret

**Monday.com Connection:**
1. Click any Monday module
2. Add connection > Authorize via OAuth or enter API token

**Slack Connection (optional):**
1. Click Slack module
2. Add connection > Authorize workspace

### Step 3: Set Webhooks

Some scenarios use webhooks. After import:

1. Open the scenario
2. Click the webhook module
3. Copy the webhook URL
4. Configure in JustCall (Settings > Webhooks):
   - SMS Sent webhook → `01-juscall-sms-sent` URL
   - SMS Received webhook → `02-juscall-reply-received` URL

### Step 4: Activate Scenarios

1. Review each scenario's logic
2. Test with a sample record
3. Toggle "Scheduling" to ON

---

## Part 3: JustCall Configuration

### Step 1: Webhook Setup

In JustCall > Settings > Integrations > Webhooks:

1. **Outbound SMS Webhook:**
   - Event: SMS Sent
   - URL: (from Make scenario 01)
   - Method: POST

2. **Inbound SMS Webhook:**
   - Event: SMS Received  
   - URL: (from Make scenario 02)
   - Method: POST

### Step 2: Phone Number Assignment

Ensure Jennica and Ana have dedicated phone numbers or a shared team number configured.

---

## Part 4: Testing Checklist

### Test 1: New Lead Flow
- [ ] Create test lead in Monday with Status = "New Lead"
- [ ] Manually send SMS via JustCall
- [ ] Verify Status changes to "SMS Sent"
- [ ] Verify Last Contact Date updates
- [ ] Verify Jennica is assigned

### Test 2: Reply Flow
- [ ] Send reply SMS to test number
- [ ] Verify Status changes to "Replied - Awaiting Ana"
- [ ] Verify Ana is assigned
- [ ] Verify Ana receives notification

### Test 3: Timeout Flow
- [ ] Set a lead to "30-Day Timeout" with Timeout Until = Yesterday
- [ ] Wait for daily automation (or trigger manually)
- [ ] Verify Status changes back to "New Lead"

### Test 4: Hibernation Flow
- [ ] Set a lead to "Hibernation 90-Day"
- [ ] Verify 90-day timer starts
- [ ] (Can't fully test without waiting 90 days - verify logic only)

---

## Maintenance

### Daily
- Jennica checks "Today's Hunt" view
- Ana checks "New Replies" and "Today's Callbacks" views

### Weekly
- Review "Pipeline Overview" for bottlenecks
- Check hibernation queue size
- Review lost reasons for patterns

### Monthly
- Analyze conversion rates by source (SMS vs Email)
- Adjust messaging based on feedback
- Clean up any stuck leads

---

## Troubleshooting

**SMS not triggering status change:**
1. Check JustCall webhook is active
2. Check Make scenario is running
3. Verify phone number matches Monday record

**Ana not getting notifications:**
1. Check Slack/email connection in Make
2. Verify Ana's email in Monday profile
3. Check notification scenario is active

**Timeout not resetting:**
1. Verify daily automation is active in Monday
2. Check Timeout Until date format
3. Manually trigger automation to test

---

## File Reference

```
jennica-workflow/
├── docs/
│   └── DEPLOYMENT_GUIDE.md (this file)
├── monday/
│   ├── 01-create-columns.graphql
│   ├── 02-create-statuses.graphql
│   ├── 03-create-views.graphql
│   └── 04-native-automations.md
├── make/
│   ├── 01-justcall-sms-sent.json
│   ├── 02-justcall-reply-received.json
│   ├── 03-status-change-notifications.json
│   └── 04-hibernation-manager.json
└── scripts/
    ├── bulk-import-leads.py
    ├── courted-monitor.py (future)
    └── requirements.txt
```
