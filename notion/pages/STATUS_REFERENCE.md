# 🗂️ Status Reference Guide

> Every status explained - what it means and who handles it

---

## The Sales Funnel Flow

```
New Lead → SMS Sent → Replied → Ana Engaged → Tool Offered →
Relationship Building → Ask Made → Meeting Scheduled →
DJ Meeting Complete → Offer Extended → Won! 🎉
```

---

## Active Statuses

### 🟣 Jennica's Statuses

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **New Lead** | Fresh lead, never contacted | Search Courted for superlative, send SMS |
| **SMS Sent** | First text sent, waiting for reply | Wait for reply (auto-moves when they respond) |

### 🔵 Ana's Statuses

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **Replied - Awaiting Ana** | They replied! Hot lead! | Respond within 4 hours |
| **Ana Engaged** | You're in conversation | Build rapport, offer tools |
| **Tool Offered** | Sent them tools/resources | Follow up in 2-4 days |
| **Training Invited** | Invited to Thursday training | Wait for attendance, then follow up |
| **Relationship Building** | Trust established, digging deeper | Find pain points, prep for the ask |
| **Ask Made** | Asked about exploring options | If yes → schedule DJ. If no → hibernate |
| **Meeting Scheduled** | DJ meeting booked | Hand off to DJ |

### 🟢 DJ's Statuses

| Status | Meaning | Next Step |
|--------|---------|-----------|
| **DJ Meeting Complete** | Met with them | Evaluate: Hot/Warm/Cool/Cold |
| **Offer Extended** | Sent them an offer | Follow-up cadence (3/7/14/21/30 days) |
| **Won** | Signed! 🎉 | Celebrate! Onboard them |

---

## Pause Statuses

| Status | What It Means | When It Returns |
|--------|---------------|-----------------|
| **30-Day Timeout** | No reply after attempts | Returns to "New Lead" after 30 days |
| **Hibernation 90-Day** | Said "not now" | Returns to "New Lead" after 90 days |
| **No Show** | Missed DJ meeting | Ana reschedules or hibernates |

---

## Terminal Statuses (End of Road)

| Status | What It Means | Can We Re-Engage? |
|--------|---------------|-------------------|
| **Won** ✅ | They signed with Kale! | N/A - They're ours! |
| **Lost - Not Interested** | Clear rejection | Maybe in 1 year |
| **Lost - Competitor** | Joined another brokerage | Set win-back date (90 days) |
| **Lost - Not Qualified** | Not a fit for us | No |
| **Dead - Negative Reply** 💀 | Said stop/hostile | NEVER contact again (1 year minimum) |

---

## Status Change Rules

### Automatic Changes (Don't touch)
- `New Lead` → `In Workflow` (when sequence starts)
- `In Workflow` → `Replied` (when JustCall detects reply)
- `30-Day Timeout` → `New Lead` (after 30 days)
- `Hibernation` → `New Lead` (after 90 days)

### Manual Changes (You do these)
- Jennica: `New Lead` → `SMS Sent` (after sending)
- Ana: All transitions from `Replied` through `Meeting Scheduled`
- DJ: `Meeting Scheduled` → `DJ Meeting Complete` → `Offer Extended` → `Won`

---

## Quick Decision Tree

```
Did they reply?
├── Yes → Status: "Replied - Awaiting Ana"
├── No (7+ days) → Status: "30-Day Timeout"
└── Said "stop" → Status: "Dead - Negative Reply"

Did they engage after tools?
├── Yes → Status: "Relationship Building"
├── No (14+ days) → Status: "30-Day Timeout"

Did they say yes to meeting?
├── Yes → Status: "Meeting Scheduled"
├── "Not now" → Status: "Hibernation 90-Day"
└── "Never" → Status: "Lost - Not Interested"
```
