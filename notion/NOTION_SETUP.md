# Notion Setup Guide for Kale Realty Sales Team

This guide helps you set up the team-facing documentation in Notion.

---

## Recommended Page Structure

```
📁 Kale Recruitment Hub (Main Page)
├── 🏠 Home Dashboard
├── 📚 Training Guides
│   ├── 🟣 Jennica's Guide
│   ├── 🔵 Ana's Guide
│   ├── 🟢 Rea's Guide
│   └── 🎯 DJ's Guide
├── 📋 Quick Reference
│   ├── 🗂️ Status Meanings
│   ├── 📊 Column Reference
│   └── 🔄 Workflow Diagram
├── 📄 Cheat Sheets (Printable)
│   ├── Jennica One-Pager
│   ├── Ana One-Pager
│   └── Rea One-Pager
├── ❓ FAQ & Troubleshooting
└── 📞 Contacts & Links
```

---

## Step-by-Step Setup

### Step 1: Create Main Page
1. In Notion, create a new page called **"Kale Recruitment Hub"**
2. Add an icon (suggest: 🏠 or your company logo)
3. Add a cover image (optional)

### Step 2: Create Home Dashboard
Create a page called **"🏠 Home Dashboard"** with:

```markdown
# Welcome to Kale Recruitment

**Quick Links:**
- [Monday.com Board](YOUR_MONDAY_LINK)
- [JustCall](YOUR_JUSTCALL_LINK)
- [Calendly - DJ](YOUR_CALENDLY_LINK)
- [Courted.ai](https://courted.ai)

---

## Today's Priorities

### 🟣 Jennica
- Send 20 personalized SMS to agents with superlatives
- Check "🟣 Jennica's Day" view in Monday

### 🔵 Ana
- Respond to all "Replied - Awaiting Ana" leads (within 4 hours!)
- Check scheduled follow-ups
- Watch for Ghost Risk = High

### 🟢 Rea
- Check "Responded" group for new replies
- Make daily call attempts
- Send Calendly links to interested leads

---

## Key Metrics (Update Weekly)
| Metric | This Week | Goal |
|--------|-----------|------|
| SMS Sent (Jennica) | | 100/week |
| Replies Received | | 15% |
| Meetings Scheduled | | 5/week |
| Offers Extended | | 2/week |
```

### Step 3: Create Training Pages
Copy content from these files into Notion pages:

| Notion Page | Source File |
|-------------|-------------|
| 🟣 Jennica's Guide | `docs/TRAINING_JENNICA.md` |
| 🔵 Ana's Guide | `docs/TRAINING_ANA.md` |
| 🟢 Rea's Guide | `docs/TRAINING_REA.md` |

**Tip:** Notion supports markdown! Just paste the content directly.

### Step 4: Create Cheat Sheets
Copy from `docs/CHEAT_SHEETS.md` - these work great as:
- Toggle blocks (collapsible sections)
- Or separate sub-pages for printing

### Step 5: Create Quick Reference
Create a **"📋 Quick Reference"** page with sub-pages:

#### 🗂️ Status Meanings
```
| Status | Meaning | Who Owns It |
|--------|---------|-------------|
| New Lead | Fresh lead, not contacted | Jennica |
| SMS Sent | First text sent | Jennica |
| Replied - Awaiting Ana | They replied! | Ana |
| Ana Engaged | Ana is talking to them | Ana |
| Tool Offered | Sent tools/resources | Ana |
| Training Invited | Invited to training | Ana |
| Relationship Building | Building trust | Ana |
| Ask Made | Asked about switching | Ana |
| Meeting Scheduled | DJ meeting booked | DJ |
| DJ Meeting Complete | Met with DJ | DJ |
| Offer Extended | Sent offer | DJ |
| Won | Signed! 🎉 | Done |
| Hibernation 90-Day | Not now, check back | System |
| 30-Day Timeout | No response | System |
| Dead - Negative Reply | Said stop | Never contact |
```

#### 📊 Column Reference
```
## Columns Ana Updates

### During Every Contact
- Last Contact Date
- Next Action
- Next Action Date
- Notes (if important)

### When They Complain About Brokerage
- Pain Points (their exact words)
- Current Split (e.g., "70/30")
- Trigger Event (select from dropdown)

### When They Mention a Competitor
- Competitor Name
- Competitor Reason

### Auto-Updated (Just Check These)
- Lead Score (0-100)
- Temperature (Cold/Warm/Hot)
- Ghost Risk (Low/Medium/High/Ghosted)
```

### Step 6: Create FAQ Page
```markdown
# ❓ Frequently Asked Questions

## General

**Q: What if I can't find someone on Courted.ai?**
A: Skip them and move to the next lead. Don't send generic messages.

**Q: What if someone says "stop"?**
A: Reply "No problem!" and immediately change status to "Dead - Negative Reply"

**Q: What if I'm not sure which status to use?**
A: Ask DJ in Slack before guessing.

---

## For Jennica

**Q: What if they have no recent superlative?**
A: Skip them for now. They might get one later.

**Q: Can I text someone I texted before?**
A: Check "Last Superlative Date" - if it's months old AND they have a NEW achievement, yes.

---

## For Ana

**Q: How quickly should I respond to new replies?**
A: Within 4 hours. Speed matters!

**Q: What if they ask about commission/splits?**
A: Say "Great question! DJ can cover all the specifics - want me to set up a quick call?"

**Q: When should I make "the ask"?**
A: When the relationship feels natural, usually after offering tools and having 2-3 good exchanges.

---

## For Rea

**Q: How many days should I call before giving up?**
A: 7 days of attempts. Then mark "Lost - No Response"

**Q: What if they already joined another brokerage?**
A: Say congrats, change status to "Chose Another Firm", set Hibernation for 90 days.
```

### Step 7: Create Contacts Page
```markdown
# 📞 Contacts & Links

## Team
| Role | Name | Contact |
|------|------|---------|
| Broker | DJ | [Slack/Phone] |
| Admin | [Name] | [Contact] |

## Tools
| Tool | Link | Login |
|------|------|-------|
| Monday.com | [Link] | SSO |
| JustCall | [Link] | [Email] |
| Calendly | [Link] | DJ's calendar |
| Courted.ai | [Link] | [Email] |
| Instantly | [Link] | [Email] |

## Support
- **Something broken?** → Message DJ in Slack
- **Need Monday help?** → Check the training guide first
- **Emergency?** → Call DJ
```

---

## Notion Tips for Your Team

### Make it Easy to Navigate
- Add the main pages to **Favorites** (star icon)
- Use the **Quick Find** (Cmd+P) to jump to any page

### Keep Training Guides Updated
- When workflows change, update Notion (not just GitHub)
- Add a "Last Updated" date at the bottom of each guide

### Use Comments for Questions
- Team members can comment on any section
- DJ gets notified and can answer inline

### Mobile Access
- Download the Notion app
- Pages work great on phones for quick reference

---

## Sharing Settings

1. Go to **Share** in top right
2. Add team members by email
3. Set permissions:
   - **Jennica, Ana, Rea**: Can view + comment
   - **DJ**: Full access (can edit)

Or create a **Guest link** for view-only access.

---

## Automatic GitHub → Notion Sync

Training documentation can be automatically synced from GitHub to Notion whenever changes are pushed.

### Setup (One-Time)

#### Step 1: Create Notion Integration
1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **"+ New integration"**
3. Name it "GitHub Sync" (or similar)
4. Select your workspace
5. Click **Submit**
6. Copy the **Internal Integration Token** (starts with `secret_`)

#### Step 2: Share Pages with Integration
For each training page you want to sync:
1. Open the page in Notion
2. Click **Share** in the top right
3. Click **Invite**
4. Search for your integration name ("GitHub Sync")
5. Click to add it

#### Step 3: Get Page IDs
For each page, copy the page ID from the URL:
```
https://www.notion.so/Your-Page-Name-abc123def456...
                                      ↑↑↑↑↑↑↑↑↑↑↑↑↑
                                      This is the page ID
```

#### Step 4: Configure the Sync
1. Edit `notion_config.json` in the repo root
2. Replace placeholder IDs with your actual page IDs:

```json
{
  "pages": {
    "training_jennica": "abc123def456...",
    "training_ana": "xyz789ghi012...",
    "training_rea": "...",
    "training_dj": "...",
    "daily_reference": "...",
    "cheat_sheets": "..."
  }
}
```

#### Step 5: Add GitHub Secret
1. Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `NOTION_TOKEN`
4. Value: Paste your integration token
5. Click **Add secret**

### How It Works

- **Automatic**: When you push changes to `docs/TRAINING_*.md` files on main branch, GitHub Actions syncs them to Notion
- **Manual**: Go to Actions → "Sync Training Docs to Notion" → "Run workflow"
- **Sync indicator**: Each Notion page shows a callout with last sync time

### Files That Sync

| GitHub File | Notion Page Key |
|-------------|-----------------|
| `docs/TRAINING_JENNICA.md` | `training_jennica` |
| `docs/TRAINING_ANA.md` | `training_ana` |
| `docs/TRAINING_REA.md` | `training_rea` |
| `docs/TRAINING_DJ.md` | `training_dj` |
| `docs/DAILY_QUICK_REFERENCE.md` | `daily_reference` |
| `docs/CHEAT_SHEETS.md` | `cheat_sheets` |

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Sync fails with "unauthorized" | Check NOTION_TOKEN secret is set correctly |
| Page not updating | Make sure the page is shared with your integration |
| Wrong content synced | Verify the page ID in notion_config.json |
| Sync runs but no changes | Check GitHub Actions log for errors |
