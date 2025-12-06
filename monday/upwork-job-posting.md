# Upwork Job Posting: Make.com + Monday.com CRM Integration

## Job Title
Make.com Expert Needed: 13 Monday.com Automation Scenarios (CRM + Workflow)

---

## Job Description

We need an experienced Make.com (formerly Integromat) specialist to build 13 automation scenarios that connect our custom Monday.com boards to Monday CRM and external services (Close CRM, Calendly, Google Sheets).

### Background
We have two real estate recruiting workflows on Monday.com:
1. **Superlative Leads** board - Team tracks potential agent recruits (Jennica/Ana workflow)
2. **Newly Licensed Leads** board - Rea manages newly licensed broker outreach (AMP passers)

We want to integrate these with Monday's built-in CRM boards (Contacts, Accounts, Deals) plus external services.

---

## PART A: CRM Integration Scenarios (5 scenarios)

**Scenario 1: Auto-Create Contact on New Lead**
- Trigger: New item created on Superlative Leads board (ID: 18390370563)
- Action: Create matching Contact in CRM Contacts board (ID: 7569016308)
- Action: Link the Contact back to the original item via board relation column
- Map fields: Name, Email, Phone, Current Brokerage

**Scenario 2: Create Deal on Won Status**
- Trigger: Status changes to "Won" on Superlative Leads board
- Action: Create Deal in CRM Deals board (ID: 7569016316)
- Action: Link Deal to the Contact
- Calculate Deal Value from Deal Count column (Deal Count × $10,000)
- Set Close Probability to 100%, Close Date to today

**Scenario 3: Duplicate Detection**
- Trigger: New item created on Superlative Leads board
- Action: Search for existing items with same email (excluding trigger item)
- If duplicate found: Add warning to Notes column, send Slack notification
- Slack channel: #leads

**Scenario 4: Sync Contact Updates**
- Trigger: Email or Phone changes on Superlative Leads board
- Action: Update the linked Contact record in CRM Contacts with new values

**Scenario 5: Link Brokerage to Account**
- Trigger: Current Brokerage field is set/changed on Superlative Leads board
- Action: Search CRM Accounts board (ID: 7569016292) for matching company
- If not found: Create new Account
- Action: Link Account to the Superlative Leads item via board relation column

---

## PART B: Newly Licensed Leads Scenarios (8 scenarios)

**Scenario 6: Google Sheets Import to Monday**
- Trigger: Webhook from Google Sheets (Apps Script button click)
- Action: Create items in "Newly Licensed Leads" board
- Action: Place all new items in "Never Responded" group
- Action: Set status to "New Lead", Lead Source to "AMP Passer List"
- Action: Set Import Date to today

**Scenario 7: Create Lead in Close CRM + Start Workflow**
- Trigger: New item created on Newly Licensed Leads board
- Action: Create lead in Close CRM with name, email, phone
- Action: Start "New Amp Passer Leads" sequence (workflow ID will be provided)
- Action: Store Close CRM Lead ID back in Monday item

**Scenario 8: SMS Reply Detection (Close CRM)**
- Trigger: Close CRM webhook - SMS reply received
- Action: Find matching item in Monday by Close CRM Lead ID
- Action: Change status to "Replied"
- Action: Move item to "Responded" group
- Action: Set "Workflow Status" to "Stopped"
- Action: Set "Last Response Date" to today

**Scenario 9: Calendly Appointment Booked**
- Trigger: Calendly webhook - appointment scheduled
- Action: Find matching item in Monday by email
- Action: Change status to "Appointment Scheduled"
- Action: Move item to "Scheduled Appointments" group
- Action: Set "Appointment Date" and "Appointment URL"

**Scenario 10: Calendly Appointment Completed**
- Trigger: Calendly webhook - appointment marked complete (or invitee no-show = false)
- Action: Find matching item in Monday by email
- Action: Change status to "Completed Appointment"

**Scenario 11: Calendly No-Show Detection**
- Trigger: Calendly webhook - invitee no-show
- Action: Find matching item in Monday by email
- Action: Change status to "No Show"
- Action: Increment "No Show Count" by 1

**Scenario 12: 30-Day Auto-Expire (Never Responded)**
- Trigger: Scheduled - run daily at 8:00 AM
- Action: Find items where Import Date > 30 days ago AND status is still "New Lead" or "In Workflow"
- Action: Change status to "Lost - No Response"
- Action: Check "Add to Event List" checkbox

**Scenario 13: Hibernation Expiry**
- Trigger: Scheduled - run daily at 8:00 AM
- Action: Find items where "Hibernation Until" date has passed AND status is "Chose Another Firm"
- Action: Change status to "New Lead" (ready for re-engagement)
- Action: Uncheck "Do Not Contact"

---

## Technical Details Provided
- All Board IDs for both boards
- All Column IDs
- Board relation column IDs for linking
- Architecture documentation
- Workflow diagrams
- Close CRM API key and workflow ID
- Calendly webhook documentation
- Google Apps Script code for Sheets button

### Deliverables
1. 13 working Make.com scenarios
2. Brief documentation explaining each scenario (trigger, actions, any special logic)
3. Test each scenario with sample data
4. 7 days of bug fixes after delivery if any issues arise

### Requirements
- Proven experience with Make.com (share examples or portfolio)
- Experience with Monday.com API and board relations
- Experience with Close CRM API (or similar CRM integrations)
- Experience with Calendly webhooks
- Understanding of CRM and lead management workflows
- Clear communication in English

### Timeline
- Preferred completion: Within 7-10 business days
- Open to discussing timeline based on your availability

### Budget
Fixed price: $400-500 USD

(Open to negotiation for the right candidate with strong Monday.com + Make.com + CRM experience)

---

## How to Apply

Please include in your proposal:
1. Your experience with Make.com and Monday.com specifically
2. A brief description of a similar integration you've built
3. Any questions you have about the requirements
4. Your estimated timeline

---

## Tags/Skills to Add on Upwork
- Make.com
- Integromat
- Monday.com
- API Integration
- Workflow Automation
- CRM Integration
- No-Code Automation
- Close CRM
- Calendly
- Google Apps Script

---

## Category
- Web, Mobile & Software Dev > Automation & Integration

---

## Screening Questions (Optional)

1. How many Make.com scenarios have you built involving Monday.com?
2. Have you worked with Monday.com's board relation columns before?
3. Have you integrated Close CRM or Calendly with Make.com before?
4. What's your typical turnaround time for 13 scenarios of this complexity?
