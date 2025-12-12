# Close CRM to Monday.com Migration Plan

## Overview

Complete migration of all leads from Close CRM to Monday.com CRM boards, with proper field mapping, owner assignment, and status handling.

---

## Phase 0: Pre-Migration Cleanup

### Step 0.1: Delete All Monday CRM Leads
Clear these boards completely before importing:
- [ ] **Superlative Leads** (`18390370563`) - 7,184 items
- [ ] **Newly Licensed Leads** (`18391158354`) - 3,447 items

**Do NOT delete:**
- Former Kale Agents We Want Back (`18391489234`) - 52 items (separate win-back workflow)

---

## Phase 1: Close CRM Lead Distribution

### Current State (10,917 total leads)

| Owner | Count | Destination |
|-------|-------|-------------|
| DJ | 5,085 | Superlative Board (assigned to DJ) |
| Rea | 3,480 | See routing rules below |
| Aileen | 2,182 | Transfer to Ana in Superlative |
| Tim | 48 | Superlative Board (assigned to DJ) |
| Unassigned | 122 | See routing rules below |

### Rea's Leads Routing (3,480)

| Close Status | Count | Destination | Monday Status | Notes |
|--------------|-------|-------------|---------------|-------|
| Top Of Funnel | 1,996 | Newly Licensed | Lead - No Response | Hibernate 1 year |
| Never Responded | 636 | Newly Licensed | Lead - No Response | Hibernate 1 year |
| Lost | 385 | Newly Licensed | Lead - No Response | Hibernate 1 year |
| Not Right Now | 64 | Newly Licensed | Lead - No Response | Hibernate 1 year |
| Kale Agent | 42 | **Closed Leads** (new board) | Won/Closed | Already joined Kale |
| Qualify | 124 | Superlative | (map status) | Active lead |
| Bad Fit | 116 | Superlative | (map status) | |
| Present | 86 | Superlative | (map status) | Active lead |
| Other | ~31 | Superlative | (map status) | |

### Aileen's Leads Routing (2,182)

| Close Status | Count | Destination | Monday Owner | Notes |
|--------------|-------|-------------|--------------|-------|
| Top Of Funnel | 1,091 | Superlative | Ana | |
| Never Responded | 558 | Superlative | Ana | |
| Lost | 399 | Superlative | Ana | |
| Not Right Now | 80 | Superlative | Ana | |
| Kale Agent | 22 | **Closed Leads** | - | Already joined |
| Qualify | 10 | Superlative | Ana | |
| Bad Fit | 17 | Superlative | Ana | |
| Paperwork Sent | 3 | Superlative | Ana | |
| Propose | 1 | Superlative | Ana | |
| Present | 1 | Superlative | Ana | |

### Unassigned Leads Routing (122)

| Close Status | Count | Destination | Monday Owner | Notes |
|--------------|-------|-------------|--------------|-------|
| Top Of Funnel | 61 | Superlative | DJ | |
| Kale Agent | 32 | **Closed Leads** | - | Already joined |
| Qualify | 8 | Superlative | DJ | |
| Lost | 8 | Superlative | DJ | |
| Never Responded | 7 | Superlative | DJ | |
| Paperwork Sent | 4 | Superlative | DJ | |
| Present | 2 | Superlative | DJ | |

---

## Phase 2: Create New Monday Board

### New Board: Closed Leads
For leads who already joined Kale (status = "Kale Agent")

**Estimated items:** 96 (42 Rea + 22 Aileen + 32 unassigned)

**Columns needed:**
- Name
- First Name
- Last Name
- Email
- Phone
- Close Date (when they became Kale Agent)
- Original Lead Owner
- Lead Source (Close)
- Close CRM ID

---

## Phase 3: Field Mapping

### Close CRM Standard Fields Available
| Field | Description | Example |
|-------|-------------|---------|
| `id` | Lead ID | `lead_upcFee1wf8VxuqUVymZ0oRR3Xc6Zgv1GVfbq4TmqTvE` |
| `display_name` | Full name | `Angela Beckham` |
| `status_label` | Lead status | `Kale Agent` |
| `status_id` | Status ID | `stat_gpGLuaytcoLBIH8THhZAcbLDFfyZGwdTa9JlZjDK7of` |
| `date_created` | Created date | `2025-08-15T15:38:15.034000+00:00` |
| `date_updated` | Updated date | `2025-12-11T21:00:03.852000+00:00` |
| `html_url` | Close URL | `https://app.close.com/lead/...` |
| `created_by_name` | Created by | `Rea Endaya` |

### Close CRM Custom Fields Available
| Field ID | Name | Type |
|----------|------|------|
| `cf_8XeOgI61X7ks89bycJoNnXYdxbILwjaWx0m7Qq6IAAl` | Lead Owner | user |
| `cf_U9j9E5v9LuS4SMLZfI854gU88tmhi0GLVlxtzbZp1yD` | Kale Lead Source | text |
| `cf_OOmZXaW7wr2fPZBkyp3lETVgFEkwYmUbsAGn3901x4K` | Left Kale Date | text |
| `cf_RZFq96WnPU5gJpj4eLcg62pXrFPuNhDdULrGKr85T3A` | Added To Courted | text |
| `cf_c09clx40GuQEME4aFK13bHwS57NdQOUTMWI5KAq9EfY` | Lead Type | text |
| `cf_XPSkF9vmCkjQJU4tkjFUV0EethSIAt8qqHiHZsjK3Sm` | Office Name | text |

### Close CRM Contact Fields
| Field | Description |
|-------|-------------|
| `contacts[0].name` | Contact name (split into first/last) |
| `contacts[0].emails[0].email` | Primary email |
| `contacts[0].phones[0].phone` | Primary phone |

---

### Close → Monday Superlative Board Mapping

| Close Field | Monday Column | Monday ID | Transform |
|-------------|---------------|-----------|-----------|
| `display_name` | Name | `name` | Direct |
| `contact.name` (first word) | First Name | `text_mky6wn9s` | Split on space |
| `contact.name` (rest) | Last Name | `text_mky6whek` | Split on space |
| `contacts[0].emails[0].email` | Email | `email_mky6p7cy` | `{"email": X, "text": X}` |
| `contacts[0].phones[0].phone` | Phone | `phone_mky6fr9j` | `{"phone": X, "countryShortName": "US"}` |
| `status_label` | Status | `status` | See status mapping table |
| `custom['Lead Owner']` | Assigned To | `multiple_person_mky6jgt4` | Map to Monday user ID |
| `date_created` | First Contact Date | `date_mky6ky4j` | `{"date": "YYYY-MM-DD"}` |
| `custom['Kale Lead Source']` | Lead Source (Close) | `text_mkyffxfn` | Direct |
| `id` | Close Lead ID | `text_mkyhaqf0` | Direct |
| `custom['Left Kale Date']` | Win-Back Date | `date_mkyct9n3` | Parse date if present |

### Close → Monday Newly Licensed Board Mapping

| Close Field | Monday Column | Monday ID | Transform |
|-------------|---------------|-----------|-----------|
| `display_name` | Name | `name` | Direct |
| `contact.name` (first word) | First Name | `text_mkybe1vc` | Split on space |
| `contact.name` (rest) | Last Name | `text_mkyb85z9` | Split on space |
| `contacts[0].emails[0].email` | Email | `email_mkybfqax` | `{"email": X, "text": X}` |
| `contacts[0].phones[0].phone` | Phone | `phone_mkyb4cr0` | `{"phone": X, "countryShortName": "US"}` |
| (fixed) | Lead Status | `color_mkybxbyk` | `{"index": 9}` = "Lead - No Response" |
| `date_created` | Import Date | `date_mkybk1hp` | `{"date": "YYYY-MM-DD"}` |
| `id` | Close CRM Lead ID | `text_mkyb1a5v` | Direct |
| (calculated) | Hibernation Until | `date_mkyb1317` | `today + 365 days` |
| `custom['Kale Lead Source']` | Lead Source (Close) | `text_mkyfrjqv` | Direct |

### Status Mapping: Close → Monday Superlative

| Close Status | Close Status ID | Monday Status | Monday Index | Notes |
|--------------|-----------------|---------------|--------------|-------|
| Top Of Funnel | `stat_broiYwml7eEj5SFwAvolMOhK0bPsA961YhnhVgyqtDJ` | New Lead | 5 | |
| Never Responded | `stat_GM1XZLRo6iWw7L5MErnRLmLAomMnvtHxNrMWpmwZjKN` | New Lead | 5 | |
| Cold Reach Out | `stat_XMeasIhqKgO00Zq5WHPm8RF6pLbngcZD40U7Aj42HTM` | New Lead | 5 | |
| Qualify | `stat_ZumjZ332FAzeIChMtwQvn72JVMQNlw9cjfbNSdYCLmb` | Ask Made | 10 | Active pipeline |
| Present | `stat_cvENukdW4deeZDg8kgfitNgXGqrg3BSBuUpsMj2Iib7` | DJ Meeting Complete | 13 | |
| Propose | `stat_jFNYSesA1YDSFYiZRrEBZdF082h4xd7nYGHD1NgXf4f` | Offer Extended | 14 | |
| Paperwork Sent | `stat_i7QhRXMzVdKm0NSV8aahYCx3o7yKjMLu0uP2555IAui` | Offer Extended | 14 | |
| Bad Fit | `stat_jyuDEdENpXxnyUnjOrLPCgYPHckgOPPBkDveh4tdHuF` | Lost - Not Qualified | 19 | |
| Lost | `stat_MWPLuOaeQDBbalLYXORYbclyXm9Mt96xaoc2XsrEQ2V` | Lost - Not Interested | 17 | |
| Not Right Now | `stat_gSGH90rg1lUOX2la33FAZLlytei5oH2IHsYGAusyw0g` | Hibernation 90-Day | 102 | |
| HC Application | `stat_JvbIwU7Lc0aXDx6BJHLpxCMKrMYfsMn02JsMWGNvNP1` | Offer Extended | 14 | |
| Kale Agent | `stat_gpGLuaytcoLBIH8THhZAcbLDFfyZGwdTa9JlZjDK7of` | → Closed Leads board | - | Don't put in Superlative |

### User ID Mapping: Close → Monday

| Name | Close User ID | Monday User ID | Notes |
|------|---------------|----------------|-------|
| DJ | `user_AP0Edi94oMcrN6LGAm9Gcy0ebFjy3F0bRonhocDFeO1` | `10993107` | |
| Rea | `user_dDXNoNN8voWPjdLp6jxW27aSA96ezyIRHWvYE2yBaQq` | `10995945` | |
| Ana (Anaya) | `user_DBMZmo4TP2tILMtbDsIVQnSU9JJ0WM0YoXS9Ly7izlh` | `97053956` | anaya@kalerealty.com |
| Aileen | `user_cUe328ab6kjnxlUZPrKNrU5GrBb0BYHbpicB46rbj1z` | → Ana | Leads transfer to Ana |
| Tim | `user_kHYbqNSf6bBO9cuhN0OkaMRgnsAZoXirNt565R0OiEJ` | → DJ (`10993107`) | Leads transfer to DJ |

**Note:** There are two Ana accounts in Monday:
- `97053956`: Anaya Dada (anaya@kalerealty.com) ← **USE THIS ONE**
- `96623356`: ana@kalerealty.com

---

## Phase 4: Migration Scripts

### Script 1: Clear Monday Boards
- Delete all items from Superlative Leads
- Delete all items from Newly Licensed Leads

### Script 2: Create Closed Leads Board
- Create new board with required columns
- Get board ID for migration

### Script 3: Migrate DJ's Leads
- Source: Close leads where Lead Owner = DJ
- Destination: Superlative Board
- Owner: DJ
- Status: Map from Close status

### Script 4: Migrate Tim's Leads
- Source: Close leads where Lead Owner = Tim
- Destination: Superlative Board
- Owner: DJ (Tim's leads transfer to DJ)

### Script 5: Migrate Aileen's Leads
- Source: Close leads where Lead Owner = Aileen
- Destination:
  - Kale Agent → Closed Leads board
  - All others → Superlative Board (owner: Ana)

### Script 6: Migrate Rea's Leads
- Source: Close leads where Lead Owner = Rea
- Destination:
  - Kale Agent → Closed Leads board
  - Top Of Funnel/Never Responded/Lost/Not Right Now → Newly Licensed (hibernate 1 year)
  - Qualify/Present/etc. → Superlative Board (owner: DJ)

### Script 7: Migrate Unassigned Leads
- Source: Close leads with no Lead Owner
- Destination:
  - Kale Agent → Closed Leads board
  - All others → Superlative Board (owner: DJ)

---

## Phase 5: Post-Migration - Match Existing Kale Agents

### Step 5.1: Get Current Kale Agents from Monday
Query the main Monday workspace (not CRM) for current Kale agents roster.

### Step 5.2: Match Against CRM
For each current Kale agent:
1. Search Superlative board by email
2. If match found → Move to Closed Leads board
3. Mark as "Won" with join date

### Step 5.3: Process "Left Kale" Groups
From Monday main workspace:
- **"Left Kale but we want back"** group → Former Kale Agents We Want Back board
- **"Left Kale but we do NOT want back"** group → Closed Leads with "Do Not Contact" flag

---

## API Credentials

### Close CRM
- **API Key:** `api_3U6OkyHlWF2pIcVusIZf2V.1uT08KKRosiYWBy8fH6B4L`
- **Base URL:** `https://api.close.com/api/v1/`
- **Lead Owner Field ID:** `cf_8XeOgI61X7ks89bycJoNnXYdxbILwjaWx0m7Qq6IAAl`

### Monday.com
- **API Key:** `eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzMDE5NDQxNywiYWFpIjoxMSwidWlkIjoxMDk5MzEwNywiaWFkIjoiMjAyNC0wMy0wN1QyMTo1MDoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NDk2MDA1OSwicmduIjoidXNlMSJ9.m3bCdQF0HwlTYrLQy4-fbTtv04A8RPxzTsWeTsGHFfI`
- **API URL:** `https://api.monday.com/v2`

### Board IDs
| Board | ID |
|-------|-----|
| Superlative Leads | `18390370563` |
| Newly Licensed Leads | `18391158354` |
| Former Kale Agents We Want Back | `18391489234` |
| Closed Leads (Won) | `18391860337` |

### Monday User IDs
| Name | ID | Email |
|------|-----|-------|
| DJ | `10993107` | dj@kalerealty.com |
| Rea | `10995945` | rea@kalerealty.com |
| Ana (Anaya) | `97053956` | anaya@kalerealty.com |
| Tim | `10993186` | tim@kalerealty.com |
| Jennica | `96623424` | jennica.abiera@gmail.com |

---

## Progress Tracking

### Phase 0: Pre-Migration Cleanup
- [x] Delete Superlative Leads items (0 items - already cleared)
- [x] Delete Newly Licensed Leads items (0 items - already cleared)

### Phase 1: Analysis (COMPLETE)
- [x] Query Close lead counts by owner
- [x] Query Close lead counts by status
- [x] Document routing rules

### Phase 2: Create New Board (COMPLETE)
- [x] Create Closed Leads board → `18391860337`
- [x] Add required columns
- [x] Get board ID

### Phase 3: Field Mapping (COMPLETE)
- [x] Get Monday Superlative column IDs (DONE)
- [x] Get Monday Newly Licensed column IDs (DONE)
- [x] Get Ana's Monday user ID → `97053956` (Anaya Dada)
- [x] Verify status label mappings (DONE - see mapping table above)
- [x] Create Close ID column → `text_mkyhaqf0`

### Phase 4: Migration Scripts
- [ ] Write clear boards script
- [ ] Write DJ migration script
- [ ] Write Tim migration script
- [ ] Write Aileen migration script
- [ ] Write Rea migration script
- [ ] Write Unassigned migration script
- [ ] Dry run all scripts
- [ ] Execute all scripts

### Phase 5: Post-Migration
- [ ] Identify current Kale agents board/group
- [ ] Match and move to Closed Leads
- [ ] Process "Left Kale want back" group
- [ ] Process "Left Kale do NOT want back" group

---

## How to Run/Resume Migration (2-Step Process)

### Overview
The migration is split into two steps for reliability:
1. **Step 1: Extract** - Pull all leads from Close API → save to local JSON
2. **Step 2: Push** - Read JSON → push to Monday API

Both steps process in batches of 200 with crash-resistant progress tracking.

---

### Step 1: Extract Leads from Close

**Script:** `scripts/extract-close-leads.py`

Extracts all Close leads with:
- Contact info (name, email, phone)
- Lead owner, status, lead source
- Office name
- Last 5 activities (emails, calls, SMS, notes, meetings)

**Commands:**
```bash
cd "/Users/djparis/Downloads/jennica-workflow 4"

# Run extraction (resumes automatically if interrupted)
python3 scripts/extract-close-leads.py
```

**Output:**
- `scripts/close_leads_export.json` - All extracted leads
- `scripts/extract_log.txt` - Extraction log

**Resume:** Just run again. Uses `close_id` to skip already-extracted leads.

---

### Step 2: Push Leads to Monday

**Script:** `scripts/push-to-monday.py`

Reads from `close_leads_export.json` and pushes to Monday with:
- Smart routing by owner/status (see routing rules above)
- Status mapping to Monday indices
- Activities combined into Notes field
- Close ID stored for matching

**Commands:**
```bash
cd "/Users/djparis/Downloads/jennica-workflow 4"

# Preview only (no changes)
DRY_RUN=true python3 scripts/push-to-monday.py

# Run push (resumes automatically if interrupted)
python3 scripts/push-to-monday.py
```

**Output:**
- `scripts/push_progress.json` - Tracks pushed lead IDs
- `scripts/push_log.txt` - Push log

**Resume:** Just run again. Tracks pushed Close IDs to skip duplicates.

---

### If Migration is Interrupted

1. **Script errors out or times out:**
   - Just run the script again
   - Extract script checks `close_leads_export.json` for existing IDs
   - Push script checks `push_progress.json` for pushed IDs

2. **Check progress:**
   ```bash
   # Extraction progress
   tail -20 scripts/extract_log.txt

   # Push progress
   tail -20 scripts/push_log.txt
   cat scripts/push_progress.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'Pushed: {len(d.get(\"pushed_ids\",[]))}')"
   ```

3. **Start completely fresh:**
   ```bash
   rm scripts/close_leads_export.json scripts/push_progress.json
   python3 scripts/extract-close-leads.py
   python3 scripts/push-to-monday.py
   ```

---

### Legacy Script (Still Available)
**File:** `scripts/migrate-close-to-monday.py`

The original single-script approach that pulls from Close and pushes to Monday in one run.
The 2-step process above is preferred for large migrations as it's more crash-resistant.

---

## Rollback Plan

If migration fails:
1. Close CRM data remains unchanged (read-only migration)
2. Monday boards can be cleared and re-run
3. Script has resume capability - just run again

---

## Phase 6: Migrate Future Tasks from Close

After the lead push completes, migrate scheduled/future tasks from Close to Monday.

### Overview
Close has scheduled tasks (follow-ups, reminders) that need to be migrated so they don't get lost.
Since each Monday lead now has a `Close ID` field, we can match tasks to leads.

### Step 6.1: Extract Future Tasks from Close

**Script:** `scripts/extract-close-tasks.py` (to be created)

Pull all open/incomplete tasks from Close:
- API endpoint: `/task/?is_complete=false`
- Capture: task text, due date, assigned user, linked lead_id

**Output:** `scripts/close_tasks_export.json`

### Step 6.2: Match and Push Tasks to Monday

**Script:** `scripts/push-tasks-to-monday.py` (to be created)

For each Close task:
1. Look up the lead's `close_id` in Close task
2. Search Monday for item with matching Close ID
3. Either:
   - Create a subitem/task on the Monday item, OR
   - Append to the Notes field with due date

### Close Task API Fields
| Field | Description |
|-------|-------------|
| `id` | Task ID |
| `lead_id` | Linked Close lead ID |
| `text` | Task description |
| `date` | Due date |
| `is_complete` | Boolean (we filter for false) |
| `assigned_to` | Close user ID |
| `_type` | Task type |

### Progress Tracking - Phase 6
- [ ] Create `extract-close-tasks.py` script
- [ ] Run task extraction
- [ ] Create `push-tasks-to-monday.py` script
- [ ] Match tasks to Monday items by Close ID
- [ ] Push tasks to Monday (Notes or subitems)

---

## Notes

- All "Kale Agent" status leads go to Closed Leads board regardless of owner
- Aileen's leads transfer ownership to Ana
- Tim's leads transfer ownership to DJ
- Unassigned leads get assigned to DJ
- Rea's newly licensed leads get 1-year hibernation date set
- Duplicate checking by email before creating Monday items
- Future tasks will be migrated in Phase 6 after leads are pushed
