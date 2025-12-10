# Former Agent Win-Back Campaign

Automated outreach to former agents on a staggered quarterly cadence.

## Schedule (Staggered SMS + Email)

| Day | Channel | Message Theme |
|-----|---------|---------------|
| 90  | SMS     | AI Tool Feedback Request |
| 105 | Email   | AI Tool Feedback (expanded) |
| 180 | SMS     | We'd Love You Back |
| 195 | Email   | What's New at Kale |
| 270 | SMS     | New Feature Announcement |
| 285 | Email   | Personal Check-In |

**Spacing:** 15 days between SMS and Email touchpoints

---

## SMS Messages (via JustCall - GitHub Actions)

Runs daily at 10 AM CT. Sends to agents where `Win-Back Date = today`.

### SMS #1 - Day 90: AI Tool Feedback
```
{Hey|Hi} {first_name} - {hope all is well|hope you're doing great|how's it going}! I just launched this listing description AI tool and would love your feedback. It researches your neighborhood and rewrites listings to get more showings.

Try it free: listing.joinkale.com

{Let me know what you think|Would love your thoughts|Curious what you think}? {No strings - just want honest feedback|Just looking for honest feedback} from someone who knows their stuff.

- DJ
```

### SMS #2 - Day 180: We'd Love You Back
```
{Hey|Hi} {first_name} - just wanted to {check in|reach out|say hi}. {Miss having you around|Been thinking about the old crew|Hope the new gig is treating you well}. {If things ever change|If you ever want to chat|If you're ever curious about what's new}, {my door's always open|you know where to find me|just reach out}.

- DJ
```

### SMS #3 - Day 270: New Feature
```
{Hey|Hi} {first_name} - {it's been a while|long time no talk|hope you're killing it out there}. {We've been making some changes here at Kale|Lot of new stuff happening at Kale|Things are evolving here} and {I thought of you|wanted to let you know|figured you might be curious}. {Let me know if you ever want to catch up|Would love to chat sometime|Reach out if you want to hear about it}.

- DJ
```

---

## Email Messages (via Make - max 5/day from dj@kalerealty.com)

Make scenario watches Monday.com for agents where `Email Win-Back Date = today`.

### Email #1 - Day 105: AI Tool Feedback (Expanded)

**Subject Lines (rotate):**
- `{Quick question|Curious what you think|Need your expert opinion}, {first_name}`
- `{Built something new|New tool} - {want your feedback|would love your take}`
- `{first_name} - {got a minute|quick favor}?`

**Body:**
```
{Hey|Hi} {first_name},

{Hope you're doing well|Hope things are going great|How's everything going}!

I {just built|recently launched|put together} this AI tool that {rewrites listing descriptions|helps agents write better listings|generates listing copy} - it actually {researches the neighborhood|pulls local data|analyzes the area} and {creates descriptions that get more showings|writes copy that converts|generates high-performing content}.

{I know you always had an eye for good marketing|You always knew what worked|You've got great instincts for this stuff}, so I'd {really value your feedback|love to hear what you think|appreciate your honest take}.

{Here's the link|Check it out|Try it here}: listing.joinkale.com

{No strings attached|Totally free|No commitment} - just {looking for honest feedback|want to know if it's actually useful|curious if it helps}.

{Thanks|Appreciate it},
DJ

--
DJ Paris
Kale Realty
dj@kalerealty.com
```

### Email #2 - Day 195: What's New at Kale

**Subject Lines (rotate):**
- `{Things have changed|Lot happening} at Kale, {first_name}`
- `{Quick update|Wanted to share} - {we've been busy|some news}`
- `{first_name} - {thought of you|you crossed my mind}`

**Body:**
```
{Hey|Hi} {first_name},

{Wanted to reach out|Just thinking about you|Hope you're killing it out there}.

{We've made some changes at Kale|Things have evolved here|A lot has happened since you left} - {new tools|better systems|some cool stuff} that {I think you'd appreciate|might interest you|you'd probably like}.

{If you're ever curious|If things change on your end|If you ever want to chat}, {I'd love to catch up|my door's open|just reach out}. {We'd love to have you back|Always a spot for you here|You're always welcome}.

{No pressure|Just wanted you to know|Totally understand if you're happy where you are} - {just keeping the door open|just saying hi|wanted to stay in touch}.

{Talk soon|Best},
DJ

--
DJ Paris
Kale Realty
dj@kalerealty.com
```

### Email #3 - Day 285: Personal Check-In

**Subject Lines (rotate):**
- `{Checking in|Just saying hi}, {first_name}`
- `{How's it going|How are things}, {first_name}?`
- `{first_name} - {been a while|long time}`

**Body:**
```
{Hey|Hi} {first_name},

{It's been a while|Long time no talk|Hope all is well}.

{Just wanted to check in|Thinking about you|Wanted to say hi} and see {how things are going|how you're doing|what you're up to}.

{I've been building some new stuff|We've added some great tools|The team has grown} and {honestly|I'll be real|truthfully}, {I think you'd really like what we're doing now|things are different in a good way|we've gotten better}.

{If you ever want to reconnect|If you're ever open to a conversation|If things change}, {I'd love to chat|reach out anytime|you know where to find me}. {We'd love to have you back|There's always a place for you|The door's always open}.

{Hope you're well|Take care|Talk soon},
DJ

--
DJ Paris
Kale Realty
dj@kalerealty.com
```

---

## Monday.com Column Setup

### Former Agents Board (ID: 18391489234)

| Column | Column ID | Type | Purpose |
|--------|-----------|------|---------|
| Win-Back Date | `date_mkygkfv` | Date | Next SMS date (auto-updates +90 days after send) |
| Email Win-Back Date | `date_mkyg2ebg` | Date | Next email date (set to Win-Back Date + 15 days) |
| Win-Back Count | `numeric_mkyg19jw` | Number | Tracks which message in sequence (0, 1, 2...) |
| Do Not Contact | `boolean_mkygt8d2` | Checkbox | Skip all outreach if checked |
| First Name | `text_mkyfws0a` | Text | Agent's first name for personalization |
| Email | `email_mkyfnfx4` | Email | Agent's email for Make scenario |
| Phone | `phone_mkyfkn1f` | Phone | Agent's phone for SMS |

---

## Setup Instructions

**Columns already created** - skip to Step 3 (Make scenario).

### Step 1: Create Email Win-Back Date Column

Run the setup script to create the column on Monday.com:
```bash
MONDAY_API_KEY=your_key python3 scripts/setup-email-winback-column.py
```

Then update `scripts/send-winback-sms.py` line 31 with the returned column ID.

### Step 2: Update SMS Script Column ID

Edit `scripts/send-winback-sms.py`:
```python
EMAIL_WINBACK_DATE_COL = "date_XXXXXX"  # Replace with actual column ID from Step 1
```

### Step 3: Create Make.com Scenario

Create a new scenario in Make with these modules:

#### Module 1: Schedule Trigger
- **Type:** Schedule
- **Interval:** Every day at 10:00 AM (CT)

#### Module 2: Monday.com - Search Items
- **Connection:** Your Monday.com connection
- **Board ID:** `18391489234` (Former Agents)
- **Filter:**
  ```
  Email Win-Back Date = {{formatDate(now; "YYYY-MM-DD")}}
  AND Do Not Contact != true
  ```
- **Limit:** `5` (max emails per day to protect sender reputation)

#### Module 3: Iterator
- **Array:** Results from Module 2

#### Module 4: Set Variable - Process Spintax
Create these variables with the **Set Variable** module:

**Variable: `processed_subject`**
Use this formula (choose Email #1, #2, or #3 based on Win-Back Count % 3):
```
{{switch(mod(3.Win-Back Count; 3);
  0; replace(replace("{{pick('Quick question'; 'Curious what you think'; 'Need your expert opinion')}}, {{3.First Name}}"; "{{3.First Name}}"; 3.First Name); ""; "");
  1; replace("{{pick('Things have changed'; 'Lot happening')}} at Kale, {{3.First Name}}"; "{{3.First Name}}"; 3.First Name);
  2; replace("{{pick('Checking in'; 'Just saying hi')}}, {{3.First Name}}"; "{{3.First Name}}"; 3.First Name)
)}}
```

**Variable: `processed_body`**
*(Copy the appropriate email body spintax from above and use Make's `pick()` function to randomize)*

**Simplified approach:** Create 3 separate email body text variables and use `switch()` to select based on count.

#### Module 5: Email - Send (Gmail/SMTP)
- **From:** `dj@kalerealty.com`
- **From Name:** `DJ Paris`
- **To:** `{{3.Email}}` (agent's email from Monday)
- **Subject:** `{{4.processed_subject}}`
- **Body (HTML):**
```html
<div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6;">
{{4.processed_body}}
</div>
```

#### Module 6: Monday.com - Update Item
- **Board ID:** `18391489234`
- **Item ID:** `{{3.id}}`
- **Column Values:**
  - **Win-Back Count:** `{{3.Win-Back Count + 1}}`
  - **Email Win-Back Date:** `{{addDays(now; 90)}}` (next email in 90 days)

#### Module 7: Monday.com - Create Update
- **Item ID:** `{{3.id}}`
- **Update Text:** `Win-back email #{{3.Win-Back Count + 1}} sent via Make`

### Step 4: Test and Activate

1. **Test manually** with a single record where Email Win-Back Date = today
2. **Check email** arrives from dj@kalerealty.com
3. **Verify Monday.com** updates (count incremented, next date set)
4. **Turn on scheduling** once confirmed working

---

## Alternative: Simpler Make Setup (No Spintax Processing)

If Make's spintax processing is too complex, use this simpler approach:

1. Create 3 separate email templates in Make
2. Use a Router module after the Iterator
3. Route based on `Win-Back Count % 3`:
   - Route 1 (count % 3 = 0): AI Tool Feedback email
   - Route 2 (count % 3 = 1): What's New email
   - Route 3 (count % 3 = 2): Personal Check-In email
4. Each route has its own hardcoded email module

This removes spintax variation but simplifies the Make scenario significantly.

---

## Quick Reference: Make Module Flow

```
[Schedule: Daily 10AM CT]
        ↓
[Monday: Search Items where Email Win-Back Date = today, limit 5]
        ↓
[Iterator: Loop through results]
        ↓
[Set Variable: Process subject/body based on Win-Back Count]
        ↓
[Email: Send from dj@kalerealty.com]
        ↓
[Monday: Update Win-Back Count + 1, Email Win-Back Date + 90 days]
        ↓
[Monday: Create Update note]
```

---

## Notes

- **Max 5 emails/day** to protect sender reputation
- **15-day gap** between SMS and email prevents overwhelming
- **Quarterly rotation** (every 90 days) keeps touchpoints spaced
- **Do Not Contact** flag respected by both SMS and email
- **Spintax** creates natural variation - no two messages identical
