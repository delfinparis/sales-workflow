# AI Meeting Notes Setup Guide

This guide covers two options for getting AI meeting notes into Monday.com:

1. **Option A: Google Meet + Gemini Notes** (native, no extra tool)
2. **Option B: MeetGeek** (third-party, more features)

---

## Option A: Google Meet + Gemini Notes → Monday

Use Google's native "Take notes with Gemini" feature, then auto-import to Monday via Make.com.

### Prerequisites

- **Google Workspace** Business Standard ($12/user/mo) or higher, OR Gemini add-on
- **Make.com** with Google + Monday connections
- **Meetings on Google Calendar** (Calendly does this automatically)

### How It Works

```
Google Meet (with "Take notes" enabled)
    ↓
Meeting ends → Gemini generates notes in Google Doc
    ↓
Make.com (scheduled every 30 min) checks calendar
    ↓
Finds notes doc, extracts content
    ↓
Matches lead in Monday by attendee email
    ↓
Pastes into "AI Meeting Notes" column
```

### Step 1: Enable Gemini Notes

**Per-meeting (manual):**
1. Start or join a Google Meet
2. Click "Take notes with Gemini" (top right, pencil icon)
3. Confirm to start note-taking

**Auto-enable for all meetings (recommended):**
1. When creating a Calendar event, click "More options"
2. Under "Meeting records", enable "Take notes"
3. OR: Ask your Google Workspace admin to enable by default

### Step 2: Import Make.com Scenario

1. Import `make/13-google-meet-notes-to-monday.json`
2. Connect: Google Calendar, Google Drive, Google Docs, Monday.com
3. Configure which calendar to watch (DJ's primary)
4. Replace `YOUR_BOARD_ID` with your Monday board ID
5. Set schedule: Every 30 minutes
6. Activate

### Step 3: Test

1. Schedule a short test Google Meet
2. Enable "Take notes with Gemini"
3. Have a brief meeting
4. Wait 30-45 minutes
5. Check Monday lead record for AI Meeting Notes

### Pros & Cons

| Pros | Cons |
|------|------|
| No extra tool/cost (if you have Workspace) | Requires Business Standard or Gemini add-on |
| Native Google integration | Notes take 5-10 min to generate |
| Notes stay in Google Docs | Make.com polling (not instant) |
| Simple setup | Must enable per-meeting or configure admin default |

---

## Option B: MeetGeek → Monday

MeetGeek is a third-party AI notetaker with native Monday.com integration.

### Why MeetGeek?

- ✅ Native Monday.com integration (no Make.com needed)
- ✅ Works with Google Meet, Zoom, Teams
- ✅ Auto-joins scheduled meetings
- ✅ Generates AI summaries instantly
- ✅ Free tier available
- ✅ Matches meetings to CRM records by email
- ✅ No Google Workspace upgrade required

### Step 1: Create MeetGeek Account

1. Go to [meetgeek.ai](https://meetgeek.ai)
2. Sign up with your Google account (same one you use for Meet)
3. Grant calendar and Meet permissions
4. Complete onboarding

---

## Step 2: Connect Google Calendar

MeetGeek needs access to your calendar to auto-join meetings.

1. Go to MeetGeek Settings > Integrations
2. Connect Google Calendar
3. Choose which calendars to monitor (your main work calendar)
4. Configure auto-join preferences:
   - ✅ Auto-join external meetings
   - ✅ Auto-join internal meetings (optional)
   - Set how early the bot joins (1-2 minutes recommended)

---

## Step 3: Connect Monday.com

1. Go to MeetGeek Settings > Integrations > Monday.com
2. Click "Connect"
3. Authorize MeetGeek to access your Monday workspace
4. Select your board: "Jennica Superlative Leads"

---

## Step 4: Configure Field Mapping

Map MeetGeek data to your Monday columns:

| MeetGeek Field | Monday Column |
|----------------|---------------|
| Meeting Summary | AI Meeting Notes |
| Action Items | (Optional: Next Action) |
| Key Topics | (Optional: Notes) |
| Attendee Email | Email (for matching) |

**Matching logic:** MeetGeek will search for items where the `Email` column matches the meeting attendee's email.

---

## Step 5: Configure Meeting Templates (Optional)

MeetGeek can use templates to structure its summaries. Create a template for recruiting meetings:

**Template: DJ Recruiting Meeting**

```
## Meeting Summary
[AI-generated summary]

## Key Discussion Points
- [Topics discussed]

## Lead's Situation
- Current brokerage: [mentioned]
- Pain points: [mentioned]
- Goals: [mentioned]

## Objections Raised
- [Any concerns or objections]

## Next Steps
- [Action items]

## Timeline
- [When they might be ready to move]
```

---

## Step 6: Test the Integration

1. Schedule a test Google Meet with someone on your team
2. Ensure their email matches a test lead in Monday
3. Have a brief meeting
4. After the meeting ends, check:
   - MeetGeek dashboard for the recording
   - Monday lead record for AI Meeting Notes

---

## How It Works in Practice

### Before the Meeting:
1. Lead books via Calendly
2. Calendly creates Google Meet link
3. MeetGeek sees the calendar event
4. Monday status = "Meeting Scheduled"

### During the Meeting:
1. MeetGeek bot joins automatically
2. Records and transcribes in real-time
3. DJ focuses on the conversation (no note-taking needed)

### After the Meeting:
1. MeetGeek generates AI summary (usually within 5 minutes)
2. Summary is pushed to Monday "AI Meeting Notes" column
3. DJ reviews and fills in structured fields:
   - Meeting Outcome
   - Current Brokerage
   - Why Considering Change
   - Business Goals
   - Timeline
   - Objections
4. DJ changes status based on outcome

---

## DJ's Post-Meeting Workflow

After each meeting, DJ should:

1. **Review AI Notes** — Scan the auto-generated summary for accuracy
2. **Fill in structured fields:**
   - **Meeting Outcome:** Hot / Warm / Cool / Cold
   - **Current Brokerage:** Where they hang their license
   - **Why Considering Change:** Their pain points
   - **Business Goals:** What they want to achieve
   - **Timeline:** When they might move
   - **Objections:** Any concerns raised
3. **Update Status:**
   - Hot → "Offer Extended" (if you made an offer)
   - Warm → "DJ Meeting Complete" + schedule follow-up
   - Cool → "Hibernation 90-Day"
   - Cold → "Lost - Not a Fit"
4. **Set Next Action** if follow-up needed

---

## DJ Meeting Questions Cheat Sheet

Keep these questions handy during meetings:

### Opening
- "Thanks for taking the time! What made you interested in chatting?"
- "How's business been going lately?"

### Current Situation
- "Where are you hanging your license right now?"
- "How long have you been there?"
- "What do you like about your current setup?"

### Pain Points (The Gold)
- "What's the biggest challenge you're facing right now?"
- "If you could change one thing about your brokerage, what would it be?"
- "What support do you wish you had?"

### Goals
- "Where do you want to be in 2-3 years?"
- "What would help you get to the next level?"
- "What's your target for deals this year?"

### The Ask (If Warm)
- "Have you ever thought about making a change?"
- "What would your ideal brokerage look like?"
- "Would you be open to learning more about what we're doing at Kale?"

### Timeline
- "If you were to make a move, when would that be?"
- "What would need to happen for you to consider a change?"

### Close
- "What questions do you have for me?"
- "What would be most helpful as a next step?"

---

## Troubleshooting

### MeetGeek bot didn't join the meeting
- Check calendar permissions
- Ensure meeting is on a monitored calendar
- Verify auto-join is enabled for external meetings
- Check if meeting was created last-minute (bot needs ~5 min notice)

### Notes didn't appear in Monday
- Check MeetGeek dashboard for the recording
- Verify email match between attendee and Monday lead
- Check Monday integration is still connected
- Look for errors in MeetGeek > Integrations > Monday

### Notes are low quality
- Meeting may have been too short
- Audio quality may have been poor
- Try speaking more clearly or using headphones
- Check if the right template is being used

---

## Privacy & Compliance

**MeetGeek:**
- MeetGeek announces itself when joining ("MeetGeek is recording this meeting")
- Attendees are notified recording is in progress
- You can configure whether to auto-transcribe or require consent
- Recordings can be auto-deleted after a set period

**Google Gemini Notes:**
- Google Meet shows a pencil icon to all participants when notes are being taken
- Notes are shared with calendar invitees by default
- Follows your Google Workspace data retention policies

---

## Which Option to Choose?

| Factor | Google Gemini | MeetGeek |
|--------|---------------|----------|
| **Cost** | Included in Workspace Std+ | Free tier available |
| **Setup complexity** | Medium (Make.com needed) | Low (native integration) |
| **Speed to Monday** | 30-45 min delay | Near-instant |
| **Reliability** | Depends on Make.com schedule | Auto-joins every meeting |
| **Note quality** | Good | Good |
| **Works with Zoom/Teams** | ❌ No | ✅ Yes |
| **Recording included** | ❌ Separate feature | ✅ Yes |

**Recommendation:**
- If you already have Google Workspace Business Standard → Try **Google Gemini** first (no extra cost)
- If you need instant sync or use multiple platforms → Use **MeetGeek**
- If you want recordings + transcripts + notes → Use **MeetGeek**

---

## Alternative Tools

| Tool | Monday Integration | Notes |
|------|-------------------|-------|
| Fireflies.ai | Via Zapier/Make | More customizable, good API |
| tl;dv | Via Zapier | Sales-focused features |
| Tactiq | Manual export | Chrome extension, lightweight |
| Otter.ai | Via Zapier | Good transcription quality |

For any tool with webhook/API support, you can build a Make.com scenario similar to our Google Gemini integration.

This requires more setup but offers more flexibility.
