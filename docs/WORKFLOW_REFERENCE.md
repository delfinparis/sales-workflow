# Jennica Superlative Leads Workflow — Complete Reference

This document covers every pathway, decision point, and edge case in the workflow. Use this when the diagram doesn't answer your question.

---

## Table of Contents

1. [Overview](#overview)
2. [Entry Path A: Jennica's Cold SMS (Courted Superlatives)](#entry-path-a-jennicas-cold-sms)
3. [Entry Path B: Instantly Cold Email (Tool Offers)](#entry-path-b-instantly-cold-email)
4. [Phase 2: Ana's Engagement](#phase-2-anas-engagement)
5. [Endpoints](#endpoints)
6. [Decision Points Reference](#decision-points-reference)
7. [Edge Cases & FAQ](#edge-cases--faq)
8. [Metrics & Success Criteria](#metrics--success-criteria)

---

## Overview

### The Goal
Convert "forgotten middle" real estate agents (2-12 deals/year) into Kale Realty brokers by building genuine relationships through value-first outreach.

### Two Entry Paths

| Path | Trigger | First Contact | Entry Point |
|------|---------|---------------|-------------|
| **A: Jennica SMS** | Courted.ai superlative | Congratulations SMS | `New Lead` → `SMS Sent` → `Replied` |
| **B: Instantly Email** | Monthly email campaign | Tool offer email | `Tool Offered` (when they say "yes") |

Both paths converge at Ana's engagement phase.

### The Strategy
1. **Catch them at a high point** — Courted.ai superlatives OR timely tool offer
2. **Open with value** — Congratulations OR free tool
3. **Earn the conversation** — Any positive reply = entry to active funnel
4. **Deliver more value** — Tools, training, genuine help
5. **Build relationship over time** — Watch for openings
6. **Make the ask when ready** — Natural recruiting conversation
7. **Let DJ close** — Meeting → signed broker

### Key Roles

| Role | Responsibilities | Tools |
|------|------------------|-------|
| **Jennica** | Daily Courted.ai monitoring, initial SMS outreach, managing hunt pool | Courted.ai, JustCall, Monday CRM |
| **Ana** | Relationship building, value delivery, recruiting conversations, Instantly lead follow-up | JustCall, Monday CRM, ChatGPT tools |
| **DJ** | Final recruiting meetings, closing | Calendly, Monday CRM |

---

## Entry Path A: Jennica's Cold SMS

*For leads discovered via Courted.ai superlatives*

### Entry: The Lead Pool

**Who's in the pool:**
- Real estate agents doing 2-12 deals per year
- Located in target markets
- Not currently affiliated with Kale
- Has presence on Courted.ai

**How they get there:**
- Bulk import from Courted.ai
- Manual addition when discovered
- Re-entry from hibernation/timeout

**Initial status:** `New Lead`

---

### Step 1: The Hunt

**Daily routine (Jennica, ~30-45 min):**

1. Open Courted.ai
2. Check for superlatives on agents in the pool:
   - New listings
   - Closed sales
   - Pending deals
   - Year-over-year growth
   - Awards/recognition
3. For each agent found:
   - **Search Monday by name or phone**
   - **Check the "Do Not Contact" checkbox**
   - ✓ Checked = STOP, do not SMS this person
   - ☐ Unchecked = Safe to proceed
4. Send up to 20 SMS per day (only to unchecked leads)

**SMS Template:**
```
Hey [First Name] - saw you just [got a new listing on X Street / closed on Y Ave / hit Z deals this year]. Amazing! Great job!
- Ana @ Kale
```

**Key principles:**
- Keep it short and genuine
- Reference the specific achievement
- No pitch, no ask
- Sign as Ana (even though Jennica sends)

**After sending:**
- Monday status → `SMS Sent`
- Last Contact Date → Today
- Assigned To → Jennica
- Superlative Type → [appropriate value]

---

### Step 2: Awaiting Reply

**Status:** `SMS Sent`

**What we're waiting for:** Any reply at all. Doesn't matter what they say — "Thanks!", "Who is this?", "Hey!" — it's all an opening.

**Timeframe:** 7 days before moving to timeout

**Possible outcomes:**

| Outcome | Trigger | Next Status |
|---------|---------|-------------|
| Positive/neutral reply | JustCall webhook detects inbound SMS | `Replied - Awaiting Ana` |
| Negative reply | Keywords detected: "stop", "unsubscribe", "not interested", etc. | `Dead - Negative Reply` |
| No reply after 7 days | Scheduled check (can be manual or automated) | `30-Day Timeout` |

---

### Step 3: Timeout Handling

**Status:** `30-Day Timeout`

**What happens:**
- Lead is paused from receiving new superlative SMS
- Timeout Until date set to Today + 30 days
- Unassigned (no owner during timeout)
- Note added: "Entered 30-day timeout - no reply received"

**When timeout expires:**
- Status returns to `New Lead`
- Back in hunt pool
- Jennica can SMS again on next superlative

**Timeout count tracking:**
- First timeout: Normal, try again
- Second timeout: Still okay, different superlative might work
- Third timeout: Consider moving to `Hibernation 90-Day`

**Decision point:** After 3 timeouts with no reply ever, the lead is cold. Move to 90-day hibernation to avoid wasting effort.

---

### Step 4: Negative Reply Handling

**Status:** `Dead - Negative Reply`

**Trigger keywords:**
- "stop"
- "unsubscribe"
- "remove me"
- "not interested"
- "leave me alone"
- "don't text me"
- "do not contact"
- Profanity/hostility

**What happens:**
- Immediate status change
- 1-year minimum before any re-contact
- Note logged with their exact response
- They will NOT receive superlative SMS during this period

**After 1 year:**
- Manual review required
- Do NOT auto-return to pool
- Only re-add if there's a compelling reason

---

## Entry Path B: Instantly Cold Email

*For leads receiving monthly tool offer emails*

### How It Works

1. **Lead pool in Instantly** — Bulk uploaded from Courted.ai (same list as Monday)
2. **Monthly campaign** — Tool offer emails sent from "fake personas"
3. **Lead replies "yes"** — Auto-reply sends tool link + mentions Ana
4. **Team marks "interested"** — Triggers webhook to Monday
5. **Ana follows up** — SMS intro + voice memo → regular flow

### The Email Sequence

**Initial email (from fake persona):**
```
Hey [Name],

D.J. from KeepingItRealPodcast just built this [tool name] that 
[does X benefit] and he'd love to get your feedback!

Want me to send it over?

[Persona Name]
```

**Auto-reply when they say "yes":**
```
Great! Here's the link: [tool URL]

Ana from our team is going to reach out over the next few days 
to get your feedback.

[Persona Name]
```

### Entry Status: `Tool Offered`

When a lead says "yes" and is marked interested in Instantly:

**What the automation does:**
1. Searches Monday by email
2. If found: Updates record with email thread, sets status, assigns Ana
3. If not found: Alerts Ana to add manually

**Column updates:**
- Status → `Tool Offered`
- Lead Source → `Instantly Email`
- Emailed By → Persona name (e.g., "Sarah")
- Assigned To → Ana
- Next Action → "Send intro SMS + voice memo"
- Next Action Date → Today
- Response Suggestions → Intro SMS template + task checklist
- Notes → Full email thread + Instantly link

### Ana's Instantly Lead Workflow

**Same day as they say "yes":**

1. **Send intro SMS:**
   ```
   Hi! [Persona] from our team just sent over the [tool] via email! 
   I'm Ana @ Kale (I work with D.J.) and I'll be reaching out 
   in the next few days to get your feedback! Thanks! :)
   ```

2. **Send voice memo** introducing herself

3. **Set follow-up date** — 2-4 days out

**Then:** Follow up for feedback → Relationship Building → regular flow

### Collision Handling

**What if lead is already being worked by Ana?**

If the lead is in an active Ana status (Ana Engaged, Tool Offered, Relationship Building, etc.):
- Status does NOT change
- A note is added to their record
- Ana is notified: "FYI - they also got tool via email"
- Existing conversation flow continues uninterrupted

### Convergence with SMS Path

After Ana's intro SMS + voice memo, Instantly leads follow the same flow as SMS leads:
- Follow up for tool feedback
- Move to `Relationship Building`
- Use pivot questions to deepen connection
- Watch for openings
- Make the ask when ready

---

## Phase 2: Ana's Engagement

### Entry Points

Ana receives leads from two paths:

| Path | Entry Status | Ana's First Action |
|------|--------------|-------------------|
| Jennica SMS | `Replied - Awaiting Ana` | Respond to their reply with contextual message |
| Instantly Email | `Tool Offered` | Send intro SMS + voice memo |

### Entry: The Reply (SMS Path)

**Status:** `Replied - Awaiting Ana`

**What triggers this:**
- Any non-negative SMS reply to Jennica's outreach
- JustCall webhook fires
- Make.com automation updates Monday

**Immediate actions:**
- Assigned To → Ana
- Ana notified via Slack/email
- Reply text logged in Notes
- Last Contact Date updated

**Ana's response time target:** Same day, within 4 hours if possible

---

### Step 5: Initial Engagement

**Status:** `Ana Engaged`

**Ana's first message goals:**
- Acknowledge their reply warmly
- Keep conversation going
- Start identifying what might help them

**Example responses:**

*If they said "Thanks!":*
```
Of course! You've been crushing it lately. 
Hey quick question - do you use any AI tools in your business yet?
```

*If they said "Who is this?":*
```
Hey! I'm Ana from Kale Realty. I just like to reach out 
when I see agents doing great work. No agenda - just wanted to say congrats!
```

*If they asked a question:*
```
[Answer their question genuinely]
...
By the way, how long have you been in the business?
```

**Key principle:** No pitch yet. We're just two people talking.

---

### Step 6: Value Delivery (Parallel Paths)

Ana has two primary value offerings, used based on what resonates:

#### Path A: Tool Offering

**Statuses:** `Tool Offered` → `Relationship Building`

**The tool:** Custom ChatGPT prompts for real estate agents (listing descriptions, client emails, market analysis, etc.)

**How to offer:**
```
Hey - random question. Do you ever use ChatGPT for your business?
I've got this set of prompts specifically for agents that saves a ton of time.
Happy to share if you're interested.
```

**If they say yes — Ana's checklist (auto-populated in Monday):**

1. ☐ Send ChatGPT tool link via SMS
2. ☐ Send voice memo introducing yourself
3. ☐ Set "Next Action Date" for follow-up call (Ana decides when — typically 2-4 days)
4. ☐ Confirm "Next Action" field has the plan

**Voice memo content:**
```
Hey [Name], it's Ana from Kale! I just sent you that ChatGPT tool 
I mentioned. Take it for a spin and let me know what you think. 
I'll give you a call in a few days to see how it's working for you. 
Talk soon!
```

**Auto-populated Next Action:**
```
Call for tool feedback → if no answer, SMS: "Hey! Did you get a chance to try that tool?"
```

**⚠️ Reminder system:** If Ana doesn't set a Next Action Date within 10 minutes, she gets a Slack/email ping reminding her.

**Follow-up call (on Next Action Date):**
- Call first
- If no answer: SMS "Hey! Did you get a chance to try that tool?"
- Listen for their response

**After tool follow-up → Move to `Relationship Building`**

The tool outcome doesn't matter — whether they used it or not, Ana pivots to relationship building.

#### Path B: Training Invitation

**Statuses:** `Training Invited` → `Relationship Building`

**The training:** Thursday training sessions on topics relevant to agents

**How to invite:**
```
We do this Thursday training thing - totally free, no pitch - 
just useful stuff for agents. This week is [topic]. 
Want me to send you the link?
```

**After training (or if they skip) → Move to `Relationship Building`**

Same as tool — attendance doesn't gate progress. It's a conversation starter.

---

### Step 7: Relationship Building

**Status:** `Relationship Building`

**This is where the real work happens.** Ana is deepening the connection, learning about their business, and watching for the right moment to make the ask.

**Entry points:**
- After tool follow-up (used it or not)
- After training invite (attended or not)
- Any time Ana wants to deepen the relationship

**Response Suggestions auto-populated:**

```
📋 AFTER TOOL FOLLOW-UP:

If they used it:
"Awesome, glad it helped! QQ - [pivot below]"

If they didn't use it:
"No problem! QQ - [pivot below]"

💡 PIVOT OPTIONS (pick one):

📅 EVENT INVITE:
"Hey, we have [event] coming up on [date]. Thought you might find it useful - want me to send the link?"

💬 MARKET QUESTION:
"How's the [their area] market treating you lately?"

🎯 GOALS QUESTION:
"What's your focus for the rest of the year?"

😤 CHALLENGES QUESTION:
"What's the biggest headache in your business right now?"

📊 BUSINESS QUESTION:
"Are you mostly working buyers or sellers these days?"
```

**What Ana is listening for:**
- Pain points with current brokerage
- Frustrations with support/training/tech
- Openness to change
- Gratitude moments ⚡

**Duration:** Could be days, weeks, or months. Don't rush it.

**Next step:** When rapport is strong and moment is right → `Ask Made`

---

### Step 8: Making The Ask

**Status:** `Ask Made`

**When to ask:**
- Strong rapport established
- They've received real value
- They've expressed pain with current situation
- Natural opening in conversation

**The Ask:**
```
Hey [Name] - this might be out of left field, but...
have you ever thought about making a change? 
Like, exploring other brokerages?

No pressure at all - I just think someone with your skills 
deserves better support than what you've described.
```

**Possible responses:**

| Response | Meaning | Next Step |
|----------|---------|-----------|
| "Actually, yeah..." | Interested | Schedule DJ meeting |
| "I've thought about it" | Warm | Explore further, address concerns |
| "Not really" | Neutral | Back to relationship building |
| "No, I'm happy" | Cold | Acknowledge, don't push, hibernation if repeated |
| "Stop asking" | Negative | Apologize, move to Lost |

---

### Step 9: The Meeting

**Status:** `Meeting Scheduled` → `DJ Meeting Complete` or `No Show`

**What happens:**
- Ana introduces DJ
- Meeting scheduled (virtual or in-person)
- Ana provides DJ with context (notes, pain points, history)
- DJ runs the recruiting conversation

**DJ's meeting:**
- Understand their goals
- Present Kale's value proposition
- Address concerns
- Make the offer

**After the meeting:**
- DJ updates Monday
- Status → `DJ Meeting Complete`
- Notes added with outcome and next steps

---

### No Show Handling

**Status:** `No Show`

**When this happens:** Lead was scheduled to meet with DJ but didn't show up.

**DJ's process (simplified with Calendly app):**
1. Meeting time arrives, lead doesn't show
2. Wait ~15 min (reasonable grace period)
3. Change Monday status: `Meeting Scheduled` → `No Show`
4. **That's it.** The Calendly Event Management app automatically marks it as no-show in Calendly.

**What the automation does:**

| No Show Count | Action |
|---------------|--------|
| 1st no-show | Assign Ana, notify her, set follow-up prompts, Next Action Date = today |
| 2nd no-show | **Auto-hibernate** — straight to `Hibernation 90-Day`, no follow-up |

**Ana's follow-up (1st no-show only):**

Response suggestions auto-populated:
```
"Hey [Name]! We missed you earlier - hope everything's okay. 
Want to find another time that works better?"

"Hey! No worries about today. Let me know when you're free 
and we can reschedule."
```

**Key principles:**
- Be friendly, not guilt-trippy
- Stuff happens — assume good intent
- If they reschedule → back to `Meeting Scheduled` (No Show Count stays at 1)
- If they ghost after 3 days → one more attempt → then manual Hibernation

**2nd no-show = automatic hibernation.** No follow-up, no second chances. They're not ready.

---

### Offer Extended 🎯

**Status:** `Offer Extended`

**What it means:** DJ has made a formal offer after a successful meeting.

**What happens when entering this status:**
- `Offer Date` set to today
- All Day X Follow-up Done checkboxes reset
- `Current Tasks` populated with follow-up cadence guide
- `Next Action` set to "Day 3 follow-up call"
- `Next Action Date` set to today + 3 days
- DJ notified via Slack
- If not Facebook Connected, prompt to connect

**Follow-up Cadence:**

| Day | Approach | Checkbox |
|-----|----------|----------|
| Day 3 | Check-in call, surface objections | Day 3 Follow-up Done |
| Day 7 | Add value (content, event, reference) | Day 7 Follow-up Done |
| Day 14 | Direct conversation about decision | Day 14 Follow-up Done |
| Day 21 | Create urgency, address blockers | Day 21 Follow-up Done |
| Day 30+ | Decision time | Escalation alert |

**DJ's role:**
- System reminds at each milestone
- DJ decides how to approach each contact
- DJ checks box after each follow-up
- System tracks but DJ has full control

**Exit paths from Offer Extended:**
- `Won` → They signed!
- `Lost - Not Interested` → Declined the offer
- `Lost - Competitor` → Went with another brokerage
- `Nurture (Post-Meeting)` → Need more relationship building
- `Hibernation 90-Day` → Not the right time, check back later

---

### Nurture (Post-Meeting) 🤝

**Status:** `Nurture (Post-Meeting)`

**What it means:** Lead met with DJ, outcome was Warm, needs more relationship building before another ask.

**How leads get here:**
- DJ sets Meeting Outcome = "Warm - Needs Follow-up"
- Automation changes status and assigns to Ana

**Ana's goal:** Become their friend. Not selling, just genuine relationship.

**Nurture activities:**
- Casual check-ins (not about brokerage)
- Invite to Thursday training events
- Share relevant content/articles
- Watch for life updates (Social Intel)
- Be a resource, not a salesperson

**Signs they're warming up:**
- Asking questions about Kale unprompted
- Mentioning frustrations with current brokerage
- Engaging more frequently
- Life circumstances changing (moving, team growing, etc.)

**When ready:** Ana flags for DJ for another meeting → status back to `Meeting Scheduled` with `Second Meeting Purpose` filled in.

---

## Endpoints

### Won ✅

**Status:** `Won`

**What it means:** They signed with Kale!

**Actions:**
- Celebrate (Slack notification, team update)
- Capture attribution (which path worked?)
- Onboarding handoff
- Ana sends congratulations

**This is terminal.** Lead exits the recruitment funnel.

---

### Lost Variants ❌

**Status options:**
- `Lost - Not Interested` — Declined after hearing pitch
- `Lost - Competitor` — Signed with different brokerage
- `Lost - Not Qualified` — Outside target range or bad fit

**Required:** Select Lost Reason dropdown for analysis

**Actions:**
- Note why they were lost
- Capture any feedback
- Terminal status (but see re-engagement below)

**Re-engagement possibility:** After 6-12 months, circumstances change. Can manually re-add to pool if there's a reason to try again.

---

### Dead - Negative Reply 💀

**Status:** `Dead - Negative Reply`

**What it means:** They explicitly asked to stop contact

**Duration:** 1 year minimum, no automatic return

**What happens when entering this status:**
- `Do Not Contact` checkbox → checked
- `Dead Until` date → Today + 365 days
- `Review Eligible` checkbox → unchecked
- Note added explaining the opt-out

**After 1 year:**
- Daily automation checks if `Dead Until` has passed
- If yes: `Review Eligible` checkbox → checked
- Lead does NOT auto-return to pool
- Appears in "Dead - Ready for Review" view
- Human must manually review and decide

**Manual review process:**
1. Check Notes — what exactly did they say?
2. Was it a soft "not interested" or hard "never contact me"?
3. Any threats, profanity, or spam reports? → Do not re-engage
4. Polite opt-out + circumstances may have changed? → Consider re-engagement
5. If re-engaging: Uncheck `Do Not Contact`, uncheck `Review Eligible`, change Status to `New Lead`
6. If not re-engaging: Leave as-is, add note, optionally extend `Dead Until` another year

**Legal note:** Respect opt-out requests. This isn't just good manners — there are legal implications (TCPA).

---

### Hibernation 90-Day ❄️

**Status:** `Hibernation 90-Day`

**What it means:** Not a hard no, just not the right time

**Used when:**
- "Ask Made" but they said "not right now"
- Multiple timeouts with no engagement
- Post-meeting "I need to think about it"
- Any situation where pausing makes sense

**What happens:**
- Hibernation Until set to Today + 90 days
- Unassigned
- Note added explaining why

**When it expires:**
- Status returns to `New Lead`
- Back in Jennica's hunt pool
- Fresh start with new superlative

---

## Decision Points Reference

The complete list of decision points in the workflow:

### Phase 1 Decisions

| # | Decision | Options | Who Decides |
|---|----------|---------|-------------|
| 1 | Is this agent in our target range? | Yes → Pool / No → Skip | Data/filters |
| 2 | Do they have a superlative today? | Yes → SMS / No → Check tomorrow | Jennica |
| 3 | Are they in timeout? | Yes → Skip / No → Proceed | Monday automation |
| 4 | Did they reply? | Yes → Ana / No → Wait | JustCall webhook |
| 5 | Is the reply negative? | Yes → Dead / No → Ana | Keyword detection |
| 6 | Has it been 7+ days? | Yes → Timeout / No → Wait | Scheduled check |
| 7 | How many timeouts? | <3 → New Lead / 3+ → Hibernation | Counter |

### Phase 2 Decisions

| # | Decision | Options | Who Decides |
|---|----------|---------|-------------|
| 8 | What value to offer? | Tool / Training / Both | Ana (based on convo) |
| 9 | Did they engage with tool? | Yes → Tool Engaged / No → Follow up | Ana observation |
| 10 | Did they attend training? | Yes → Note it / No → Follow up | Ana observation |
| 11 | Is there a gratitude moment? | Yes → Pivot deeper / No → Keep delivering | Ana judgment |
| 12 | What are their pain points? | [Various] → Address specifically | Ana discovery |
| 13 | Is rapport strong enough? | Yes → Consider Ask / No → Keep building | Ana judgment |
| 14 | Is this the right moment? | Yes → Make Ask / No → Wait | Ana judgment |
| 15 | How did they respond to Ask? | Interested / Warm / Neutral / Cold / Negative | Their response |
| 16 | Should we schedule DJ? | Yes → Schedule / No → Back to building | Ana judgment |
| 17 | Meeting outcome? | Won / Lost / Need time | DJ report |

### Exit Decisions

| # | Decision | Options | Who Decides |
|---|----------|---------|-------------|
| 18 | Lost reason? | Not interested / Competitor / Not qualified | DJ/Ana |
| 19 | Hibernation or Lost? | Soft no → Hibernate / Hard no → Lost | Context |
| 20 | Re-engage from Lost? | Yes → Manual re-add / No → Leave | Manual review |

---

## Edge Cases & FAQ

### Q: What if they reply during timeout?

**A:** If positive reply → `Replied - Awaiting Ana` (timeout cancelled)
If negative reply → `Dead - Negative Reply`

The timeout is for *us* not contacting *them*. If they reach out, we respond.

---

### Q: What if they reply negatively after being in Ana's pipeline?

**A:** Depends on the relationship stage:

- Early (just replied): → `Dead - Negative Reply`
- Mid (tool/training): → `Lost - Not Interested` + note
- Late (after Ask): → `Lost - Not Interested` + note

Use "Dead" only for explicit opt-out language. Use "Lost" for rejection of recruiting pitch.

---

### Q: What if the same person is in both SMS and Email (Instantly) funnels?

**A:** Lead Source should be marked "Both". Ana handles them with awareness of both touchpoints. Don't double-contact on the same day.

---

### Q: What if they ghost mid-conversation?

**A:** 
- Day 3: Follow up
- Day 7: Second follow up
- Day 14: "Hey, no worries if now isn't a good time. I'll check back in a few weeks."
- Then: `Hibernation 90-Day`

---

### Q: What if they say "not now" to the Ask?

**A:**
```
Totally get it. No pressure at all. I'm here whenever/if ever 
you want to chat about it. In the meantime, let me know if 
there's anything else I can help with!
```
Status → `Hibernation 90-Day` (not Lost — door is open)

---

### Q: What if they sign with a competitor?

**A:** `Lost - Competitor`, note which brokerage, note any feedback. They're terminal for now, but agents move around — could revisit in 1-2 years.

---

### Q: How do we handle re-entry from hibernation?

**A:** They return to `New Lead` status. Jennica treats them like any other lead in the pool. The previous conversation history is preserved in Notes — Ana will see it if they reply again.

---

### Q: What if Jennica accidentally SMS someone in timeout?

**A:** The Monday view should prevent this, but if it happens:
- If they reply positively: Great, proceed normally
- If they reply negatively: Apologize briefly, move to Dead
- If no reply: Update the timeout date, add note

---

### Q: What's the max number of times someone can cycle through?

**A:** No hard limit, but use judgment:
- 2-3 hibernation cycles with no progress = consider permanent removal
- If they've explicitly said "no" multiple times = stop

---

## Metrics & Success Criteria

### Key Metrics to Track

**Volume Metrics:**
| Metric | Target | Measured |
|--------|--------|----------|
| SMS sent per day | 20 | Daily |
| Reply rate | 10-20% | Weekly |
| New leads to Ana per week | 15-25 | Weekly |

**Conversion Metrics:**
| Metric | Target | Measured |
|--------|--------|----------|
| Reply → Tool Engaged | 60%+ | Monthly |
| Tool Engaged → Pain Point | 50%+ | Monthly |
| Pain Point → Ask Made | 40%+ | Monthly |
| Ask Made → Meeting | 30%+ | Monthly |
| Meeting → Won | 25%+ | Monthly |

**Efficiency Metrics:**
| Metric | Target | Measured |
|--------|--------|----------|
| Days from Reply to Won | <60 | Per win |
| Cost per Won | Track | Monthly |
| Hibernation return rate | Track | Quarterly |

### Success Criteria by Role

**Jennica succeeds when:**
- 20 quality SMS sent daily
- <5% sent to wrong targets
- Clean Monday data maintenance

**Ana succeeds when:**
- Same-day response to replies
- High tool/training engagement
- Pipeline moving forward (not stuck)
- Quality notes on every lead

**DJ succeeds when:**
- Prepared for every meeting
- High meeting-to-close rate
- Clear feedback to Ana on losses

---

## Changelog

| Date | Change | Author |
|------|--------|--------|
| 2024-XX-XX | Initial workflow documentation | [Name] |
| | | |

---

## Questions?

If something isn't covered here, add it to the FAQ section for future reference.
