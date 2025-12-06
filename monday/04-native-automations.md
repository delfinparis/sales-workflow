# Monday.com Native Automations

These automations are configured directly in Monday.com (not Make.com).
Go to: Board > Automate (lightning bolt icon) > Add Automation

---

## Automation 1: Auto-Assign Ana on New Lead (Instantly Replies)

**Purpose:** When a NEW lead is created (from Instantly cold email reply), assign to Ana.

**Context:**
- Jennica's Courted superlative leads already exist in Monday (migrated from Close)
- Jennica manually looks up leads before sending SMS - no item creation needed
- The only NEW items come from Instantly email replies → these go directly to Ana

**Recipe:**
```
When item is created
→ Set Assigned To to Ana
→ Set Status to "Replied - Awaiting Ana"
```

**Setup:**
1. Click "Add Automation"
2. Search "When item is created"
3. Add action: "change column" > Assigned To > Ana
4. Add action: "change column" > Status > Replied - Awaiting Ana

**Note:** The Make.com Instantly webhook scenario should also set Lead Source = "Instantly" when creating the item. This native automation is a backup to ensure proper assignment.

---

## Automation 2: Track SMS Sent

**Purpose:** When Jennica marks SMS as sent, update timestamps.

**Recipe:**
```
When Status changes to "SMS Sent"
→ Set Last Contact Date to Today
```

**Setup:**
1. Click "Add Automation"
2. "When status changes to something" > SMS Sent
3. Add action: "Set date to today" > Last Contact Date

---

## Automation 3: Reply Received - Assign Ana

**Purpose:** When a lead replies, transfer to Ana.

**Recipe:**
```
When Status changes to "Replied - Awaiting Ana"
→ Set Assigned To to Ana
→ Notify Ana via email
→ Set Last Contact Date to Today
```

**Setup:**
1. Click "Add Automation"
2. "When status changes to something" > Replied - Awaiting Ana
3. Add action: "Assign" > Ana
4. Add action: "Notify" > Ana > "New lead reply: {item name}"
5. Add action: "Set date to today" > Last Contact Date

---

## Automation 4: 30-Day Timeout Trigger

**Purpose:** After no reply, pause lead for 30 days.

**Recipe:**
```
When Status changes to "30-Day Timeout"
→ Set Timeout Until to (Today + 30 days)
→ Set Assigned To to empty
```

**Setup:**
1. Click "Add Automation"
2. "When status changes to something" > 30-Day Timeout
3. Add action: Custom automation with formula (or use Make.com for date math)

**Note:** Monday's native automations have limited date math. For "Today + 30 days", you may need to use Make.com (see `03-timeout-manager.json`).

---

## Automation 5: Timeout Expiration Check (Daily)

**Purpose:** Return timed-out leads to the hunt pool.

**Recipe:**
```
Every day at 8:00 AM
→ Find items where Status = "30-Day Timeout" AND Timeout Until is past
→ Change Status to "New Lead"
```

**Setup:**
This requires a recurring automation + filter, which Monday handles via:
1. Click "Add Automation"
2. "Every time period" > Every Day at 8:00 AM
3. Condition: Status = 30-Day Timeout
4. Condition: Timeout Until < Today
5. Action: Change Status to New Lead

**Alternative:** Handle in Make.com with scheduled scenario.

---

## Automation 6: 90-Day Hibernation Check (Daily)

**Purpose:** Return hibernated leads to circulation.

**Recipe:**
```
Every day at 8:00 AM
→ Find items where Status = "Hibernation 90-Day" AND Hibernation Until is past
→ Change Status to "New Lead"
```

**Setup:**
Same pattern as Automation 5, but for Hibernation status.

---

## Automation 7: Track All Status Changes

**Purpose:** Log when status changes for audit trail.

**Recipe:**
```
When Status changes
→ Push to activity log (automatic in Monday)
→ Set Last Contact Date to Today
```

**Note:** Monday automatically logs status changes in the Activity Log. This automation just ensures Last Contact Date stays current.

---

## Automation 8: Won Notification

**Purpose:** Celebrate wins!

**Recipe:**
```
When Status changes to "Won"
→ Notify team channel
→ Send email to DJ
```

**Setup:**
1. "When status changes to something" > Won
2. Add action: Notify > [Team or Slack channel]
3. Add action: Send email > DJ > "New broker signed: {item name}"

---

## Automation 9: Meeting Scheduled Notification

**Purpose:** Alert DJ when meeting is booked.

**Recipe:**
```
When Status changes to "Meeting Scheduled"
→ Notify DJ
→ Send email with lead details
```

---

## Automation 10: Stale Lead Warning

**Purpose:** Flag leads that haven't been touched in 7+ days.

**Recipe:**
```
Every day at 9:00 AM
→ Find items where Last Contact Date < (Today - 7 days)
→ AND Status is in active Ana statuses
→ Notify Ana
```

**Active Ana statuses:** Ana Engaged, Tool Offered, Tool Engaged, Training Invited, Pain Point Identified, Relationship Building

---

## Automation 11: Do Not Contact Checkbox (CRITICAL)

**Purpose:** Automatically manage the "Do Not Contact" checkbox so Jennica has an instant visual cue.

⚠️ **This is essential.** Without this, Jennica could accidentally SMS leads in timeout.

### Option A: Native Monday Automations (Multiple recipes needed)

**Recipe 11a - Check box on timeout:**
```
When Status changes to "30-Day Timeout"
→ Check "Do Not Contact"
```

**Recipe 11b - Check box on hibernation:**
```
When Status changes to "Hibernation 90-Day"
→ Check "Do Not Contact"
```

**Recipe 11c - Check box on dead:**
```
When Status changes to "Dead - Negative Reply"
→ Check "Do Not Contact"
```

**Recipe 11d - Check box on any lost:**
```
When Status changes to "Lost - Not Interested"
→ Check "Do Not Contact"
```
(Repeat for "Lost - Competitor" and "Lost - Not Qualified")

**Recipe 11e - Check box on won:**
```
When Status changes to "Won"
→ Check "Do Not Contact"
```

**Recipe 11f - UNCHECK box on New Lead:**
```
When Status changes to "New Lead"
→ Uncheck "Do Not Contact"
```

### Option B: Make.com Automation (Recommended)

Use the scenario in `make/05-do-not-contact-manager.json` — it handles all status changes in one scenario with cleaner logic.

### Why This Matters

| Scenario | Without checkbox | With checkbox |
|----------|-----------------|---------------|
| Jennica finds superlative on Courted | Must search Monday, check status, interpret | Glance at checkbox ✓ or empty |
| Lead in 30-day timeout | Could accidentally SMS | Checkbox ✓ = stop |
| Lead returns from hibernation | Must verify status changed | Checkbox empty = safe |

The checkbox is a **failsafe** that works even if Jennica is moving fast.

---

## Mirror Column Setup (for CRM entity linking)

If using Monday CRM's Contact/Account entities, create mirror columns:

1. Go to Columns > Add Column > Connect Boards
2. Link to "Contacts" board (CRM entity)
3. Add Mirror columns to pull:
   - Contact email
   - Contact phone
   - Account name
   - Account details

This lets you maintain lead pipeline separate from master contact database while keeping data synced.

---

## Automation 11: DJ Daily Meeting Reminder

**Purpose:** Remind DJ at end of day to mark all meetings as show or no-show.

**Recipe:**
```
Every day at 5:00 PM
→ Notify DJ
→ "Reminder: Did you mark all today's meetings as show or no-show? 
   Update status in Monday: Meeting Scheduled → DJ Meeting Complete or No Show"
```

**Setup:**
1. Go to board automations
2. Click "Add Automation"
3. Search for "Every time period notify"
4. Configure:
   - Time period: Every day
   - Time: 5:00 PM
   - Person: [Select DJ]
   - Message: "Reminder: Did you mark all today's meetings as show or no-show? Update status: Meeting Scheduled → DJ Meeting Complete or No Show"

**Note:** This is a simple time-based reminder, no conditions needed.

---

## Automation 12: Calendly No-Show Sync (via Calendly Event Management App)

**Purpose:** When DJ marks a lead as No Show in Monday, automatically mark as no-show in Calendly.

**This is configured in the Calendly Event Management app, not native Monday automations.**

**Recipe (in Calendly Event Management app):**
```
When status changes to "No Show" 
→ marks Calendly scheduled event as a No Show
```

**Setup:**
1. Go to Board Integrations
2. Find Calendly Event Management app
3. Add the automation: "When status changes to something marks Calendly scheduled event as a No Show"
4. Configure: Status = "No Show"

**Why this matters:**
- DJ only updates Monday, not both systems
- Calendly's no-show tracking stays in sync
- Stops Calendly's native follow-up workflows
- Single source of truth

---

## Automation 13: Set First Contact Date

**Purpose:** Record when a lead was first contacted (for days-to-close metrics).

**Recipe:**
```
When Status changes from "New Lead" to anything else
AND First Contact Date is empty
→ Set First Contact Date to Today
```

**Setup:**
This requires a condition check that Monday native automations can handle:
1. Click "Add Automation"
2. "When status changes"
3. From: New Lead, To: Any status
4. Add condition: "Only if First Contact Date is empty"
5. Action: Set First Contact Date to Today

**Note:** This only fires once - the condition ensures it doesn't overwrite.

---

## Automation 14: Set Last Superlative Date

**Purpose:** Track when Jennica last sent a congratulations SMS (for re-entry timing).

**Recipe:**
```
When Status changes to "SMS Sent"
→ Set Last Superlative Date to Today
```

**Setup:**
1. Click "Add Automation"
2. "When status changes to SMS Sent"
3. Action: Set Last Superlative Date to Today

---

## Automation Summary Table

| # | Trigger | Action | Platform |
|---|---------|--------|----------|
| 1 | Item created | Assign Ana, set Replied - Awaiting Ana | Monday |
| 2 | Status → SMS Sent | Set Last Contact Date, Last Superlative Date | Monday |
| 3 | Status → Replied | Assign Ana, notify, timestamp | Monday |
| 4 | Status → 30-Day Timeout | Set Timeout Until (+30 days), increment count | Make.com |
| 5 | Daily + Timeout expired | Status → New Lead | Monday/Make |
| 6 | Daily + Hibernation expired | Status → New Lead, reset Timeout Count | Monday/Make |
| 7 | Any status change | Update Last Contact Date | Monday |
| 8 | Status → Won | Notify team, email DJ | Monday |
| 9 | Status → Meeting Scheduled | Notify DJ, populate prep questions | Monday |
| 10 | Daily + stale leads | Notify Ana | Make.com |
| 11 | Daily at 5pm | Remind DJ to mark show/no-show | Monday |
| 12 | Status → No Show | Mark no-show in Calendly | Calendly App |
| 13 | Status leaves New Lead | Set First Contact Date (once) | Monday |
| 14 | Status → SMS Sent | Set Last Superlative Date | Monday |
| 15 | Meeting 24h/1h/10min away + Prep not done | Remind DJ to prep | Make.com |
| 16 | DJ Meeting Complete + 24h + fields empty | Nag DJ to process | Make.com |
| 17 | Daily 5pm | Summary of DJ's incomplete processing | Make.com |
| 18 | Status → Offer Extended | Set Offer Date, reset checkboxes, start cadence | Make.com |
| 19 | Daily 9am + Offer Extended | Check follow-up cadence, remind DJ | Make.com |
| 20 | Meeting Outcome → Warm | Status → Nurture, assign Ana, notify | Make.com |
| 21 | Queue for Event Invite checked | Send individual SMS via JustCall API | Make.com |
| 22 | Day 3/7/14/21 checkbox checked | Set Last Offer Follow-up date | Monday |

---

## DJ-Specific Automation Details

### Meeting Prep Reminders (Make.com #16)

**Trigger:** Every 15 minutes, checks for Meeting Scheduled leads

**Alerts:**
- **24 hours before:** Full prep reminder with context
- **1 hour before:** Urgent reminder with quick facts
- **10 minutes before:** Final ping with meeting link

**Condition:** Only fires if `Meeting Prep Done` is unchecked

### Post-Meeting Processing Nag (Make.com #17)

**Trigger:** Hourly check + Daily 5pm summary

**24-Hour Nag:** If DJ Meeting Complete status and Meeting Outcome is empty for 24+ hours

**Daily 5pm Summary:** Count of leads needing processing, count in Offer Extended

### Offer Extended Setup (Make.com #21)

**Trigger:** Status changes to Offer Extended

**Actions:**
1. Set Offer Date = Today
2. Reset all Day X Follow-up Done checkboxes
3. Populate Current Tasks with follow-up cadence guide
4. Set Next Action = "Day 3 follow-up call"
5. Set Next Action Date = Today + 3 days
6. Log in Updates with full timeline
7. Notify DJ via Slack
8. If not Facebook Connected, suggest connecting

### Offer Follow-up Reminders (Make.com #18)

**Trigger:** Daily at 9am

**Stages:**
- **Day 3:** Check-in call, surface objections
- **Day 7:** Add value (share content, invite to event, offer reference)
- **Day 14:** Direct conversation about decision status
- **Day 21:** Create urgency, address specific blockers
- **Day 30+:** Escalation - decide: close, nurture, or hibernate

**Logic:** Each stage requires previous stage checkbox to be complete

### Warm Lead Handback (Make.com #20)

**Trigger:** Meeting Outcome changes to "Warm - Needs Follow-up"

**Actions:**
1. Status → Nurture (Post-Meeting)
2. Assigned To → Ana
3. Populate Current Tasks with nurture prompts
4. Log handback in Updates
5. Notify Ana via Slack with context

---

## Calendly Event Management App Automations

These are configured separately in the Calendly Event Management app (Board > Integrate > Calendly Event Management):

| Trigger | Action |
|---------|--------|
| New Calendly event scheduled | Find lead by email, update Meeting Date/URL/Links, set Status to Meeting Scheduled |
| Calendly event rescheduled | Update Meeting Date/URL on existing item |
| Calendly event canceled | Set Status to Relationship Building |
| Monday status → No Show | Mark as no-show in Calendly |

---

## Custom Automation Recipes

For complex logic not supported natively, use Make.com. The scenarios in `/make/` folder handle:

- JustCall webhook → Monday status update
- Date math (Today + N days)
- Conditional logic based on multiple fields
- External service integration
