# Close CRM - New Amp Passer Leads Workflow

## Workflow Info

- **Workflow Name:** New Amp Passer Leads
- **Sequence ID:** `seq_7TUbe0qzdkzDqHMTy63BMb`
- **Status:** Active
- **Timezone:** America/Chicago
- **Schedule:** Mon-Sun, 8:00 AM - 6:00 PM

---

## Close API Reference

- **API Key:** `api_3U6OkyHlWF2pIcVusIZf2V.1uT08KKRosiYWBy8fH6B4L`
- **Base URL:** `https://api.close.com/api/v1/`

---

## Workflow Steps (12 Total)

### Step 1: SMS #1 (Day 0)
- **Template ID:** `smstmpl_5TOrwpwPehTIKNir5wylSC`
- **Name:** Amp Passer #1
- **Delay:** 0 (immediate)
- **Content:**
```
{{ contact.first_name }}, congrats on passing broker class! This is {{ user.first_name }} @ Kale Realty. QQ - what are you looking for in a brokerage?
```

---

### Step 2: SMS #1.5 (Day 1)
- **Template ID:** `smstmpl_1jvaZg5P7DJi9kOfV0T7RZ`
- **Name:** Amp Passer #1.5
- **Delay:** 86400 seconds (1 day)
- **Content:**
```
We'd love to learn more about you! Schedule a quick chat - https://joinkale.com/schedule
```

---

### Step 3: Email #1 (Day 1, same day as SMS #1.5)
- **Template ID:** `tmpl_T6hwODIXakSrTyInqiMCQjGxxwTLbL3L4QKtyLKKCxR`
- **Name:** New Amp Passer Email #1
- **Delay:** 0 (immediately after SMS #1.5)
- **Subject:** `about your broker license...`
- **Attachment:** Top 26 Questions To Ask When Choosing a New Brokerage.pdf
- **Content:**
```html
Hi {{ contact.first_name }},

Congrats on passing the broker class! Quick question - what are you most looking for in a brokerage? Training, tools, support - or something else?

P.S. I attached 26 questions to ask when interviewing brokerages! :)
```

---

### Step 4: Email #2 (Day 3)
- **Template ID:** `tmpl_pSpV6t1S9tn4GEFQ4jrDOXtCtHEXxl7XdOPEIKSYcZ5`
- **Name:** New Amp Passer Email #2
- **Delay:** 172800 seconds (2 days after previous)
- **Subject:** `congrats`
- **Content:**
```html
Hi {{ contact.first_name }},

Amazing job on your broker class! Just curious - are you going into real estate full-time or will you be a dual career agent? There are NO wrong answers! :)
```

---

### Step 5: SMS #2 (Day 3, same day as Email #2)
- **Template ID:** `smstmpl_21SNzin1VZX3kXd3DDYSCY`
- **Name:** Amp Passer #2
- **Delay:** 0 (immediately after Email #2)
- **Content:**
```
Here's the 26 most important questions to ask BEFORE joining a brokerage! https://joinkale.com/real-estate-interview-questions
```

---

### Step 6: Email #3 (Day 5)
- **Template ID:** `tmpl_aJ9hgL23n41WzZMcWDDTWEKTdigGwCdBvRjSOMKPg0H`
- **Name:** New Amp Passer Email #3
- **Delay:** 259200 seconds (3 days after previous)
- **Subject:** `{{ contact.first_name }}, quick question...`
- **Content:**
```html
Hi {{ contact.first_name }},

We'd like to learn more about your real estate vision! Are you looking to work more with buyers, sellers, or not sure yet?
```

---

### Step 7: Email #4 (Day 6)
- **Template ID:** `tmpl_RouSXpw38SlcW9RE3A2fr4WUcN9CNPd7RtPEUJYoJxD`
- **Name:** New Amp Passer Email #4
- **Delay:** 345600 seconds (4 days after previous step 5)
- **Subject:** `Congrats...`
- **Content:**
```html
Hey {{ contact.first_name }},

You're a superstar for passing the broker class! What are you looking for in a brokerage?
```

---

### Step 8: Email #5 (Day 7)
- **Template ID:** `tmpl_cUxiupwLZRQC6vAfIipYwgzfRH6HJyUG0fZ1hCsucJB`
- **Name:** New Amp Passer Email #5
- **Delay:** 432000 seconds (5 days after previous step 5)
- **Subject:** `real estate license...`
- **Content:**
```html
Hi {{ contact.first_name }},

We want to learn about you! What is your #1 real estate goal right now! There are NO wrong answers! :)
```

---

### Step 9: Email #6 (Day 8)
- **Template ID:** `tmpl_Fc00pXSApo7oX1bTa348viuCoEx1UD2deUwoOODlpsd`
- **Name:** New Amp Passer Email #6
- **Delay:** 518400 seconds (6 days after previous step 5)
- **Subject:** `you are awesome...`
- **Content:**
```html
Hi {{ contact.first_name }},

Passing the broker class is NOT easy. And you did it! Now you need to join a firm! What are you looking for in a brokerage?
```

---

### Step 10: Email #7 (Day 9)
- **Template ID:** `tmpl_OyiPEAwfOSlNO4YCFaWww2Mdi8dvByRxiYXi4SP6MxU`
- **Name:** New Amp Passer Email #7
- **Delay:** 604800 seconds (7 days after previous step 5)
- **Subject:** `Real Estate License`
- **Content:**
```html
Hi {{ contact.first_name }},

We know that some agents do NOT want to talk to a brokerage before reading about it. We get it! Here's our website. Learn away! :)

Link: https://joinkale.com
```

---

### Step 11: SMS #7 (Day 30)
- **Template ID:** `smstmpl_0YYsoX2x5VwcoNjIbgB8qc`
- **Name:** Amp Passer #7
- **Delay:** 2592000 seconds (30 days)
- **Content:**
```
Hi {{ contact.first_name }} - {{ user.first_name }} from Kale. Are you still looking for a brokerage to join?
```

---

### Step 12: Lead Update (Day 33)
- **Type:** update-lead
- **Delay:** 259200 seconds (3 days after SMS #7)
- **Action:** Marks workflow as complete

---

## Timeline Summary

| Day | Type | Template | Content Summary |
|-----|------|----------|-----------------|
| 0 | SMS | #1 | Congrats + what are you looking for? |
| 1 | SMS | #1.5 | Schedule a chat link |
| 1 | Email | #1 | Congrats + 26 questions PDF |
| 3 | Email | #2 | Full-time or dual career? |
| 3 | SMS | #2 | 26 questions link |
| 5 | Email | #3 | Buyers, sellers, or not sure? |
| 6 | Email | #4 | You're a superstar + what looking for? |
| 7 | Email | #5 | #1 real estate goal? |
| 8 | Email | #6 | Need to join a firm + what looking for? |
| 9 | Email | #7 | Website link for self-research |
| 30 | SMS | #7 | Still looking for a brokerage? |
| 33 | Update | - | Mark workflow complete |

---

## Auto-Stop Behavior

When a lead replies to ANY SMS or email in this sequence, the workflow automatically stops in Close CRM.

---

## Key Links

- **Schedule Link:** https://joinkale.com/schedule
- **26 Questions Article:** https://joinkale.com/real-estate-interview-questions
- **Website:** https://joinkale.com

---

## Integration Notes

### Triggering the Workflow

To enroll a lead in this workflow via API:

```bash
curl -X POST "https://api.close.com/api/v1/sequence_subscription/" \
  -u "api_3U6OkyHlWF2pIcVusIZf2V.1uT08KKRosiYWBy8fH6B4L:" \
  -H "Content-Type: application/json" \
  -d '{
    "sequence_id": "seq_7TUbe0qzdkzDqHMTy63BMb",
    "contact_id": "CONTACT_ID_HERE",
    "sender_account_id": "SENDER_ACCOUNT_ID",
    "sender_email_account_id": "EMAIL_ACCOUNT_ID",
    "sender_name": "Rea"
  }'
```

### Stopping the Workflow

To manually stop a lead's workflow:

```bash
curl -X DELETE "https://api.close.com/api/v1/sequence_subscription/SUBSCRIPTION_ID/" \
  -u "api_3U6OkyHlWF2pIcVusIZf2V.1uT08KKRosiYWBy8fH6B4L:"
```
