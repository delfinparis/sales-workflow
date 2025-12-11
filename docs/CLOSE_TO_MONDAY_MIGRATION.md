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

### Close CRM Fields → Monday Superlative Board

| Close Field | Close Type | Monday Column | Monday ID | Notes |
|-------------|------------|---------------|-----------|-------|
| display_name | text | Name | `name` | |
| contact.name (split) | text | First Name | `text_mky6wn9s` | |
| contact.name (split) | text | Last Name | `text_mky6whek` | |
| contact.emails[0] | email | Email | `email_mky6p7cy` | |
| contact.phones[0] | phone | Phone | `phone_mky6fr9j` | |
| status_label | status | Status | `status` | Needs mapping |
| Lead Owner | user | Assigned To | `multiple_person_mky6jgt4` | Map user IDs |
| date_created | date | First Contact Date | `date_mky6ky4j` | |
| Kale Lead Source | text | Lead Source (Close) | `text_mkyffxfn` | Custom field |
| id | text | (new column?) | TBD | Store Close ID |

### Close CRM Fields → Monday Newly Licensed Board

| Close Field | Close Type | Monday Column | Monday ID | Notes |
|-------------|------------|---------------|-----------|-------|
| display_name | text | Name | `name` | |
| contact.name (split) | text | First Name | `text_mkybe1vc` | |
| contact.name (split) | text | Last Name | `text_mkyb85z9` | |
| contact.emails[0] | email | Email | `email_mkybfqax` | |
| contact.phones[0] | phone | Phone | `phone_mkyb4cr0` | |
| status_label | status | Lead Status | `color_mkybxbyk` | All = "Lead - No Response" |
| date_created | date | Import Date | `date_mkybk1hp` | |
| id | text | Close CRM Lead ID | `text_mkyb1a5v` | |

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
| Closed Leads | TBD (create first) |

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
- [ ] Delete Superlative Leads items
- [ ] Delete Newly Licensed Leads items

### Phase 1: Analysis (COMPLETE)
- [x] Query Close lead counts by owner
- [x] Query Close lead counts by status
- [x] Document routing rules

### Phase 2: Create New Board
- [ ] Create Closed Leads board
- [ ] Add required columns
- [ ] Get board ID

### Phase 3: Field Mapping
- [x] Get Monday Superlative column IDs (DONE)
- [x] Get Monday Newly Licensed column IDs (DONE)
- [x] Get Ana's Monday user ID → `97053956` (Anaya Dada)
- [x] Verify status label mappings (DONE - see mapping table above)
- [ ] Create Close ID column if needed

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

## Rollback Plan

If migration fails:
1. Close CRM data remains unchanged (read-only migration)
2. Monday boards can be cleared and re-run
3. Each script is idempotent (can re-run safely)

---

## Notes

- All "Kale Agent" status leads go to Closed Leads board regardless of owner
- Aileen's leads transfer ownership to Ana
- Tim's leads transfer ownership to DJ
- Unassigned leads get assigned to DJ
- Rea's newly licensed leads get 1-year hibernation date set
- Duplicate checking by email before creating Monday items
