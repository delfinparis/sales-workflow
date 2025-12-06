# Jennica Superlative Leads — Complete Setup Script

**Board ID:** 18390370563
**Board URL:** https://kalerealty.monday.com/boards/18390370563

---

## Step 1: Open Monday API Playground

Go to: https://monday.com/developers/v2/try-it-yourself

Make sure you're logged into your Monday account.

---

## Step 2: Run Column Mutations

Copy and paste each mutation below into the API Playground and click "Run".
Run them one at a time. Each should return a success response with the column ID.

---

### CORE FIELDS

**1. Lead Source**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Lead Source"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"Jennica SMS (Superlative)\"},{\"id\":2,\"name\":\"Instantly Email (Cold)\"},{\"id\":3,\"name\":\"Both\"}]}"
  ) {
    id
    title
  }
}
```

**2. Priority**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Priority"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"High (8-12 deals)\"},{\"id\":2,\"name\":\"Medium (5-7 deals)\"},{\"id\":3,\"name\":\"Low (2-4 deals)\"}]}"
  ) {
    id
    title
  }
}
```

**3. Phone**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Phone"
    column_type: phone
  ) {
    id
    title
  }
}
```

**4. Email**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Email"
    column_type: email
  ) {
    id
    title
  }
}
```

**5. Assigned To**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Assigned To"
    column_type: people
  ) {
    id
    title
  }
}
```

---

### TRACKING DATES

**6. First Contact Date**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "First Contact Date"
    column_type: date
  ) {
    id
    title
  }
}
```

**7. Last Contact Date**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Last Contact Date"
    column_type: date
  ) {
    id
    title
  }
}
```

**8. Last Superlative Date**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Last Superlative Date"
    column_type: date
  ) {
    id
    title
  }
}
```

**9. Next Action Date**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Next Action Date"
    column_type: date
  ) {
    id
    title
  }
}
```

**10. Next Action**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Next Action"
    column_type: text
  ) {
    id
    title
  }
}
```

---

### LEAD CONTEXT

**11. Superlative Type**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Superlative Type"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"New Listing\"},{\"id\":2,\"name\":\"Pending/Under Contract\"},{\"id\":3,\"name\":\"Closed Sale\"},{\"id\":4,\"name\":\"Closed Rental\"},{\"id\":5,\"name\":\"YoY Growth\"},{\"id\":6,\"name\":\"Other\"}]}"
  ) {
    id
    title
  }
}
```

**12. Courted Profile**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Courted Profile"
    column_type: link
  ) {
    id
    title
  }
}
```

**13. Deal Count**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Deal Count"
    column_type: numbers
  ) {
    id
    title
  }
}
```

**14. Notes**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Notes"
    column_type: long_text
  ) {
    id
    title
  }
}
```

**15. Current Tasks**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Current Tasks"
    column_type: long_text
  ) {
    id
    title
  }
}
```

---

### TIMEOUT & HIBERNATION

**16. Timeout Until**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Timeout Until"
    column_type: date
  ) {
    id
    title
  }
}
```

**17. Timeout Count**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Timeout Count"
    column_type: numbers
  ) {
    id
    title
  }
}
```

**18. Hibernation Until**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Hibernation Until"
    column_type: date
  ) {
    id
    title
  }
}
```

**19. Do Not Contact**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Do Not Contact"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

---

### DEAD LEAD REVIEW

**20. Dead Until**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Dead Until"
    column_type: date
  ) {
    id
    title
  }
}
```

**21. Review Eligible**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Review Eligible"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**22. Lost Reason**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Lost Reason"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"Not interested\"},{\"id\":2,\"name\":\"Signed with competitor\"},{\"id\":3,\"name\":\"Not qualified (deal count)\"},{\"id\":4,\"name\":\"Bad timing\"},{\"id\":5,\"name\":\"No response after multiple attempts\"},{\"id\":6,\"name\":\"Negative/hostile reply\"},{\"id\":7,\"name\":\"Other\"}]}"
  ) {
    id
    title
  }
}
```

---

### CALENDLY INTEGRATION

**23. Meeting Date**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Meeting Date"
    column_type: date
  ) {
    id
    title
  }
}
```

**24. Meeting URL**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Meeting URL"
    column_type: link
  ) {
    id
    title
  }
}
```

**25. Calendly Cancel Link**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Calendly Cancel Link"
    column_type: link
  ) {
    id
    title
  }
}
```

**26. Calendly Reschedule Link**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Calendly Reschedule Link"
    column_type: link
  ) {
    id
    title
  }
}
```

---

### INSTANTLY EMAIL INTEGRATION

**27. Emailed By**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Emailed By"
    column_type: text
  ) {
    id
    title
  }
}
```

**28. Tool Type**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Tool Type"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"ChatGPT Prompts\"},{\"id\":2,\"name\":\"Listing Description Generator\"},{\"id\":3,\"name\":\"Market Analysis Tool\"},{\"id\":4,\"name\":\"Other\"}]}"
  ) {
    id
    title
  }
}
```

**29. Voice Memo Sent**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Voice Memo Sent"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

---

### DJ MEETING FIELDS

**30. No Show Count**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "No Show Count"
    column_type: numbers
  ) {
    id
    title
  }
}
```

**31. Meeting Outcome**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Meeting Outcome"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"Hot - Ready to Sign\"},{\"id\":2,\"name\":\"Warm - Needs Follow-up\"},{\"id\":3,\"name\":\"Cool - Not Now\"},{\"id\":4,\"name\":\"Cold - Not a Fit\"},{\"id\":5,\"name\":\"No Show\"}]}"
  ) {
    id
    title
  }
}
```

**32. Current Brokerage**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Current Brokerage"
    column_type: text
  ) {
    id
    title
  }
}
```

**33. Why Considering Change**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Why Considering Change"
    column_type: long_text
  ) {
    id
    title
  }
}
```

**34. Business Goals**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Business Goals"
    column_type: long_text
  ) {
    id
    title
  }
}
```

**35. Timeline**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Timeline"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"Immediately\"},{\"id\":2,\"name\":\"1-3 Months\"},{\"id\":3,\"name\":\"3-6 Months\"},{\"id\":4,\"name\":\"6-12 Months\"},{\"id\":5,\"name\":\"Not Sure\"}]}"
  ) {
    id
    title
  }
}
```

**36. Objections**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Objections"
    column_type: long_text
  ) {
    id
    title
  }
}
```

**37. AI Meeting Notes**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "AI Meeting Notes"
    column_type: long_text
  ) {
    id
    title
  }
}
```

---

### DJ MEETING PREP & FOLLOW-UP

**38. Meeting Prep Done**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Meeting Prep Done"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**39. Second Meeting Purpose**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Second Meeting Purpose"
    column_type: dropdown
    defaults: "{\"labels\":[{\"id\":1,\"name\":\"Address commission/split concerns\"},{\"id\":2,\"name\":\"Meet the team\"},{\"id\":3,\"name\":\"Tour office\"},{\"id\":4,\"name\":\"Review paperwork/next steps\"},{\"id\":5,\"name\":\"Follow up on pending deal timing\"},{\"id\":6,\"name\":\"Bring spouse/partner into conversation\"},{\"id\":7,\"name\":\"Other (see notes)\"}]}"
  ) {
    id
    title
  }
}
```

**40. Second Meeting Notes**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Second Meeting Notes"
    column_type: text
  ) {
    id
    title
  }
}
```

---

### OFFER EXTENDED FOLLOW-UP

**41. Offer Date**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Offer Date"
    column_type: date
  ) {
    id
    title
  }
}
```

**42. Day 3 Follow-up Done**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Day 3 Follow-up Done"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**43. Day 7 Follow-up Done**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Day 7 Follow-up Done"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**44. Day 14 Follow-up Done**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Day 14 Follow-up Done"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**45. Day 21 Follow-up Done**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Day 21 Follow-up Done"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**46. Last Offer Follow-up**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Last Offer Follow-up"
    column_type: date
  ) {
    id
    title
  }
}
```

---

### ANA EVENT INVITE

**47. Queue for Event Invite**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Queue for Event Invite"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**48. Last Event Invite**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Last Event Invite"
    column_type: date
  ) {
    id
    title
  }
}
```

---

### SOCIAL SELLING (Phase 2)

**49. Facebook Connected**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Facebook Connected"
    column_type: checkbox
  ) {
    id
    title
  }
}
```

**50. Last Social Check**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Last Social Check"
    column_type: date
  ) {
    id
    title
  }
}
```

**51. Social Intel**
```graphql
mutation {
  create_column(
    board_id: 18390370563
    title: "Social Intel"
    column_type: long_text
  ) {
    id
    title
  }
}
```

---

## Step 3: Configure Status Labels

The Status column already exists on your board. You need to edit the labels.

**Option A: Manual (Recommended)**
1. Click on any Status cell in your board
2. Click "Edit Labels" at the bottom of the dropdown
3. Delete the default labels
4. Add these labels with colors:

| Label | Color |
|-------|-------|
| New Lead | Gray |
| SMS Sent | Light Blue |
| 30-Day Timeout | Orange |
| Replied - Awaiting Ana | Purple |
| Tool Offered | Teal/Green |
| Training Invited | Lime |
| Relationship Building | Gold/Yellow |
| Ask Made | Orange |
| Meeting Scheduled | Red |
| No Show | Pink |
| DJ Meeting Complete | Maroon/Dark Red |
| Offer Extended | Bright Pink |
| Nurture (Post-Meeting) | Soft Blue |
| Won | Dark Green |
| Lost - Not Interested | Dark Gray |
| Lost - Competitor | Dark Red |
| Lost - Not Qualified | Brown |
| Dead - Negative Reply | Black |
| Hibernation 90-Day | Light Gray |

**Option B: API (if you want to try)**
```graphql
mutation {
  change_column_metadata(
    board_id: 18390370563
    column_id: "status"
    column_property: labels
    value: "{\"labels\":{\"0\":{\"color\":\"#c4c4c4\",\"name\":\"New Lead\"},\"1\":{\"color\":\"#579bfc\",\"name\":\"SMS Sent\"},\"2\":{\"color\":\"#fdab3d\",\"name\":\"30-Day Timeout\"},\"3\":{\"color\":\"#a25ddc\",\"name\":\"Replied - Awaiting Ana\"},\"4\":{\"color\":\"#00c875\",\"name\":\"Tool Offered\"},\"5\":{\"color\":\"#9cd326\",\"name\":\"Training Invited\"},\"6\":{\"color\":\"#cab641\",\"name\":\"Relationship Building\"},\"7\":{\"color\":\"#ff642e\",\"name\":\"Ask Made\"},\"8\":{\"color\":\"#e2445c\",\"name\":\"Meeting Scheduled\"},\"9\":{\"color\":\"#ff9ed4\",\"name\":\"No Show\"},\"10\":{\"color\":\"#bb3354\",\"name\":\"DJ Meeting Complete\"},\"11\":{\"color\":\"#ff158a\",\"name\":\"Offer Extended\"},\"12\":{\"color\":\"#66ccff\",\"name\":\"Nurture (Post-Meeting)\"},\"13\":{\"color\":\"#00642e\",\"name\":\"Won\"},\"14\":{\"color\":\"#757575\",\"name\":\"Lost - Not Interested\"},\"15\":{\"color\":\"#d83a52\",\"name\":\"Lost - Competitor\"},\"16\":{\"color\":\"#7f5347\",\"name\":\"Lost - Not Qualified\"},\"17\":{\"color\":\"#333333\",\"name\":\"Dead - Negative Reply\"},\"18\":{\"color\":\"#e8e8e8\",\"name\":\"Hibernation 90-Day\"}}}"
  ) {
    id
  }
}
```

---

## Step 4: Verify Setup

Run this query to see all your columns:

```graphql
query {
  boards(ids: [18390370563]) {
    columns {
      id
      title
      type
    }
  }
}
```

You should see 51 columns (plus the default Name column).

**Save the output!** You'll need the column IDs for Make.com scenarios.

---

## Step 5: Next Steps

After columns and statuses are set up:

1. **Create Views** — Follow `03-create-views.graphql` in the package
2. **Set up Make.com scenarios** — Import the JSON files
3. **Install Calendly app** — Monday marketplace
4. **Connect JustCall** — Configure webhooks
5. **Test the flow** — Create a test lead and walk through

---

## Troubleshooting

**"Column already exists" error:**
- That's fine, skip to the next one

**"Board not found" error:**
- Make sure you're logged into the right Monday account
- Check the board ID is correct

**Status API mutation fails:**
- Use Option A (manual) instead — it's more reliable

---

## Time Estimate

- Running all 51 mutations: ~15-20 minutes
- Setting up statuses: ~5 minutes
- Creating views: ~30 minutes
- Total: ~1 hour for board setup

Let's go! 🚀
