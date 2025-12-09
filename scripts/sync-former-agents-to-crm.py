#!/usr/bin/env python3
"""
Former Kale Agents → CRM Sync Script

Monthly sync script that:
1. Scans "Terminated Agents we want back" group in the Kale Agents roster
2. Checks if they exist in CRM boards (Superlative or Newly Licensed)
3. If NOT in CRM: Creates them in "Former Kale Agents We Want Back" board
4. Also handles "Terminated Agents we do NOT want back" group:
   - Removes any matching leads from all CRM boards

Source Board: 359616654 (Kale Realty Agents)
- Group: new_group99427 (Terminated Agents we want back)
- Group: new_group57275 (Terminated Agents we do NOT want back)

Target Boards:
- 18391489234 (Former Kale Agents We Want Back) - NEW board for this workflow
- 18390370563 (Superlative Leads) - check for matches
- 18391158354 (Newly Licensed Leads) - check for matches

Column Mapping (from roster to new board):
- text95 (First Name) → text_mkyfws0a (First Name)
- text_19 (Last Name) → text_mkyfsd7g (Last Name)
- phone_number8 (Phone) → phone_mkyfkn1f (Phone)
- home_email (Home Email) → email_mkyfnfx4 (Email)
- status18 (Reason) → Note in pulse history
- date4 (Date Terminated) → Note in pulse history
- Item ID → text_mkyfv61s (Former Agent ID)

Usage:
    python sync-former-agents-to-crm.py [--dry-run]
"""

import requests
import json
import time
import re
import argparse
import os
from datetime import datetime

# =============================================================================
# Configuration
# =============================================================================

# API key from environment variable (for GitHub Actions) or fallback to hardcoded (local dev)
MONDAY_API_KEY = os.environ.get("MONDAY_API_KEY", "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzMDE5NDQxNywiYWFpIjoxMSwidWlkIjoxMDk5MzEwNywiaWFkIjoiMjAyNC0wMy0wN1QyMTo1MDoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NDk2MDA1OSwicmduIjoidXNlMSJ9.m3bCdQF0HwlTYrLQy4-fbTtv04A8RPxzTsWeTsGHFfI")
MONDAY_API_URL = "https://api.monday.com/v2"

# Board IDs
ROSTER_BOARD_ID = "359616654"           # Kale Realty Agents
FORMER_AGENTS_BOARD_ID = "18391489234"  # Former Kale Agents We Want Back (NEW)
SUPERLATIVE_BOARD_ID = "18390370563"    # Superlative Leads
NEWLY_LICENSED_BOARD_ID = "18391158354" # Newly Licensed Leads

# Roster Groups
WANT_BACK_GROUP = "new_group99427"       # Terminated Agents we want back
DONT_WANT_BACK_GROUP = "new_group57275"  # Terminated Agents we do NOT want back

# Roster Source Columns
ROSTER_FIRST_NAME = "text95"
ROSTER_LAST_NAME = "text_19"
ROSTER_PHONE = "phone_number8"
ROSTER_EMAIL = "home_email"
ROSTER_REASON = "status18"
ROSTER_DATE_TERMINATED = "date4"

# Former Agents Target Columns
FA_FIRST_NAME = "text_mkyfws0a"
FA_LAST_NAME = "text_mkyfsd7g"
FA_EMAIL = "email_mkyfnfx4"
FA_PHONE = "phone_mkyfkn1f"
FA_STATUS = "color_mkyfnpqe"
FA_FORMER_AGENT_ID = "text_mkyfv61s"

# CRM Email/Phone columns for matching
SUP_EMAIL_COL = "email_mky6p7cy"
SUP_PHONE_COL = "phone_mky6fr9j"
NL_EMAIL_COL = "email_mkybfqax"
NL_PHONE_COL = "phone_mkyb4cr0"

# Rate limiting
RATE_LIMIT_DELAY = 0.5

# =============================================================================
# API Setup
# =============================================================================

session = requests.Session()
session.headers.update({
    "Authorization": MONDAY_API_KEY,
    "Content-Type": "application/json",
    "API-Version": "2024-10"
})


def monday_query(query, variables=None, max_retries=3):
    """Execute a GraphQL query against Monday API."""
    time.sleep(RATE_LIMIT_DELAY)

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(max_retries):
        try:
            response = session.post(MONDAY_API_URL, json=payload)
            response.raise_for_status()
            data = response.json()

            if "errors" in data:
                print(f"  GraphQL Error: {data['errors']}")
                return None

            return data.get("data")
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt + 1}/{max_retries}: {e}")
                time.sleep(2 ** attempt)
            else:
                print(f"  Failed after {max_retries} attempts: {e}")
                return None

    return None


def normalize_phone(phone_str):
    """Normalize phone number to digits only for comparison."""
    if not phone_str:
        return ""
    digits = re.sub(r'\D', '', str(phone_str))
    return digits[-10:] if len(digits) >= 10 else digits


def normalize_email(email_str):
    """Normalize email for comparison."""
    if not email_str:
        return ""
    return email_str.lower().strip()


# =============================================================================
# Data Fetching Functions
# =============================================================================

def get_roster_group_items(group_id, group_name):
    """Get all items from a roster group with relevant columns."""
    print(f"Fetching items from '{group_name}'...")

    items = []
    cursor = None

    columns_to_fetch = [
        ROSTER_FIRST_NAME, ROSTER_LAST_NAME, ROSTER_PHONE,
        ROSTER_EMAIL, ROSTER_REASON, ROSTER_DATE_TERMINATED
    ]

    while True:
        if cursor:
            query = """
            query {
                boards(ids: [%s]) {
                    groups(ids: ["%s"]) {
                        items_page(limit: 100, cursor: "%s") {
                            cursor
                            items {
                                id
                                name
                                column_values(ids: ["%s"]) {
                                    id
                                    text
                                    value
                                }
                            }
                        }
                    }
                }
            }
            """ % (ROSTER_BOARD_ID, group_id, cursor, '", "'.join(columns_to_fetch))
        else:
            query = """
            query {
                boards(ids: [%s]) {
                    groups(ids: ["%s"]) {
                        items_page(limit: 100) {
                            cursor
                            items {
                                id
                                name
                                column_values(ids: ["%s"]) {
                                    id
                                    text
                                    value
                                }
                            }
                        }
                    }
                }
            }
            """ % (ROSTER_BOARD_ID, group_id, '", "'.join(columns_to_fetch))

        result = monday_query(query)
        if not result:
            break

        groups = result.get("boards", [{}])[0].get("groups", [])
        if not groups:
            break

        items_page = groups[0].get("items_page", {})
        page_items = items_page.get("items", [])
        cursor = items_page.get("cursor")

        for item in page_items:
            agent = {
                "id": item["id"],
                "name": item["name"],
                "first_name": "",
                "last_name": "",
                "phone": "",
                "email": "",
                "reason": "",
                "date_terminated": ""
            }

            for col in item.get("column_values", []):
                col_id = col["id"]
                text = col.get("text", "")

                if col_id == ROSTER_FIRST_NAME:
                    agent["first_name"] = text
                elif col_id == ROSTER_LAST_NAME:
                    agent["last_name"] = text
                elif col_id == ROSTER_PHONE:
                    agent["phone"] = normalize_phone(text)
                    agent["phone_raw"] = text
                elif col_id == ROSTER_EMAIL:
                    agent["email"] = normalize_email(text)
                    agent["email_raw"] = text
                elif col_id == ROSTER_REASON:
                    agent["reason"] = text
                elif col_id == ROSTER_DATE_TERMINATED:
                    agent["date_terminated"] = text

            items.append(agent)

        print(f"  Fetched {len(items)} items...")

        if not cursor:
            break

    return items


def build_crm_index(board_id, email_col, phone_col, board_name):
    """Build email/phone index of items in a CRM board."""
    print(f"  Indexing {board_name}...")

    email_index = {}
    phone_index = {}
    cursor = None

    while True:
        if cursor:
            query = """
            query {
                boards(ids: [%s]) {
                    items_page(limit: 100, cursor: "%s") {
                        cursor
                        items {
                            id
                            name
                            column_values(ids: ["%s", "%s"]) {
                                id
                                text
                            }
                        }
                    }
                }
            }
            """ % (board_id, cursor, email_col, phone_col)
        else:
            query = """
            query {
                boards(ids: [%s]) {
                    items_page(limit: 100) {
                        cursor
                        items {
                            id
                            name
                            column_values(ids: ["%s", "%s"]) {
                                id
                                text
                            }
                        }
                    }
                }
            }
            """ % (board_id, email_col, phone_col)

        result = monday_query(query)
        if not result:
            break

        items_page = result.get("boards", [{}])[0].get("items_page", {})
        items = items_page.get("items", [])
        cursor = items_page.get("cursor")

        for item in items:
            item_info = {"id": item["id"], "name": item["name"], "board_id": board_id}

            for col in item.get("column_values", []):
                if col["id"] == email_col:
                    email = normalize_email(col.get("text", ""))
                    if email:
                        email_index[email] = item_info
                elif col["id"] == phone_col:
                    phone = normalize_phone(col.get("text", ""))
                    if phone:
                        phone_index[phone] = item_info

        if not cursor:
            break

    print(f"    {len(email_index)} emails, {len(phone_index)} phones indexed")
    return email_index, phone_index


def get_former_agents_index():
    """Get index of agents already in Former Agents board by their roster ID."""
    print("  Indexing Former Agents board...")

    index = set()
    cursor = None

    while True:
        if cursor:
            query = """
            query {
                boards(ids: [%s]) {
                    items_page(limit: 100, cursor: "%s") {
                        cursor
                        items {
                            column_values(ids: ["%s"]) {
                                text
                            }
                        }
                    }
                }
            }
            """ % (FORMER_AGENTS_BOARD_ID, cursor, FA_FORMER_AGENT_ID)
        else:
            query = """
            query {
                boards(ids: [%s]) {
                    items_page(limit: 100) {
                        cursor
                        items {
                            column_values(ids: ["%s"]) {
                                text
                            }
                        }
                    }
                }
            }
            """ % (FORMER_AGENTS_BOARD_ID, FA_FORMER_AGENT_ID)

        result = monday_query(query)
        if not result:
            break

        items_page = result.get("boards", [{}])[0].get("items_page", {})
        items = items_page.get("items", [])
        cursor = items_page.get("cursor")

        for item in items:
            for col in item.get("column_values", []):
                if col.get("text"):
                    index.add(col["text"])

        if not cursor:
            break

    print(f"    {len(index)} former agents already in board")
    return index


# =============================================================================
# Action Functions
# =============================================================================

def create_former_agent(agent, dry_run=False):
    """Create a new item in Former Kale Agents board."""
    item_name = agent["name"]

    if dry_run:
        print(f"  [DRY RUN] Would create: {item_name}")
        return True

    # Build column values
    column_values = {
        FA_FIRST_NAME: agent.get("first_name", ""),
        FA_LAST_NAME: agent.get("last_name", ""),
        FA_FORMER_AGENT_ID: agent["id"],
    }

    # Email needs special format
    if agent.get("email_raw"):
        column_values[FA_EMAIL] = {"email": agent["email_raw"], "text": agent["email_raw"]}

    # Phone needs special format
    if agent.get("phone_raw"):
        column_values[FA_PHONE] = {"phone": agent["phone_raw"], "countryShortName": "US"}

    query = """
    mutation ($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
        create_item(
            board_id: $boardId,
            item_name: $itemName,
            column_values: $columnValues
        ) {
            id
        }
    }
    """
    variables = {
        "boardId": FORMER_AGENTS_BOARD_ID,
        "itemName": item_name,
        "columnValues": json.dumps(column_values)
    }

    result = monday_query(query, variables)
    if not result or not result.get("create_item"):
        return False

    new_item_id = result["create_item"]["id"]

    # Add update with reason and termination date
    notes_parts = []
    if agent.get("reason"):
        notes_parts.append(f"**Reason for Leaving:** {agent['reason']}")
    if agent.get("date_terminated"):
        notes_parts.append(f"**Date Terminated:** {agent['date_terminated']}")

    if notes_parts:
        update_body = "**Former Kale Agent Info:**\n\n" + "\n".join(notes_parts)
        update_body += "\n\n*Synced from Kale Realty Agents roster.*"

        update_query = """
        mutation ($itemId: ID!, $body: String!) {
            create_update(item_id: $itemId, body: $body) {
                id
            }
        }
        """
        monday_query(update_query, {"itemId": new_item_id, "body": update_body})

    return True


def delete_crm_item(board_id, item_id, item_name, dry_run=False):
    """Delete an item from CRM."""
    if dry_run:
        print(f"  [DRY RUN] Would delete: {item_name} from board {board_id}")
        return True

    query = """
    mutation {
        delete_item(item_id: %s) {
            id
        }
    }
    """ % item_id

    result = monday_query(query)
    return result is not None


# =============================================================================
# Main Logic
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Sync Former Kale Agents to CRM')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be done without making changes')
    args = parser.parse_args()

    print("=" * 60)
    print("Former Kale Agents → CRM Sync")
    print("=" * 60)
    print()
    print("Source: Kale Realty Agents (359616654)")
    print("Target: Former Kale Agents We Want Back (18391489234)")
    print()

    if args.dry_run:
        print("*** DRY RUN MODE - No changes will be made ***\n")

    stats = {
        "want_back_total": 0,
        "already_in_former": 0,
        "already_in_crm": 0,
        "created": 0,
        "dont_want_total": 0,
        "removed_from_crm": 0,
        "failed": 0
    }

    # Step 1: Build CRM indexes (for checking if someone is already in CRM)
    print("Building CRM indexes...")
    sup_email_idx, sup_phone_idx = build_crm_index(
        SUPERLATIVE_BOARD_ID, SUP_EMAIL_COL, SUP_PHONE_COL, "Superlative Leads"
    )
    nl_email_idx, nl_phone_idx = build_crm_index(
        NEWLY_LICENSED_BOARD_ID, NL_EMAIL_COL, NL_PHONE_COL, "Newly Licensed Leads"
    )

    # Combine CRM indexes
    crm_emails = {**sup_email_idx, **nl_email_idx}
    crm_phones = {**sup_phone_idx, **nl_phone_idx}

    # Step 2: Get Former Agents board index (to avoid duplicates)
    former_agent_ids = get_former_agents_index()

    # Step 3: Get "Don't Want Back" list (blocklist)
    print()
    dont_want_back = get_roster_group_items(DONT_WANT_BACK_GROUP, "Terminated Agents we do NOT want back")
    stats["dont_want_total"] = len(dont_want_back)

    blocklist_emails = {a["email"] for a in dont_want_back if a["email"]}
    blocklist_phones = {a["phone"] for a in dont_want_back if a["phone"]}
    print(f"  Blocklist: {len(blocklist_emails)} emails, {len(blocklist_phones)} phones")

    # Step 4: Process "Don't Want Back" - Remove from CRM if they exist
    print()
    print("Checking blocklist for CRM removal...")
    print("-" * 40)

    for agent in dont_want_back:
        # Check if in CRM by email
        if agent["email"] and agent["email"] in crm_emails:
            item = crm_emails[agent["email"]]
            if delete_crm_item(item["board_id"], item["id"], item["name"], args.dry_run):
                stats["removed_from_crm"] += 1
                print(f"  ✓ Removed (email): {item['name']}")
            else:
                stats["failed"] += 1

        # Check if in CRM by phone (if not already matched by email)
        elif agent["phone"] and agent["phone"] in crm_phones:
            item = crm_phones[agent["phone"]]
            if delete_crm_item(item["board_id"], item["id"], item["name"], args.dry_run):
                stats["removed_from_crm"] += 1
                print(f"  ✓ Removed (phone): {item['name']}")
            else:
                stats["failed"] += 1

    # Step 5: Get "Want Back" list
    print()
    want_back = get_roster_group_items(WANT_BACK_GROUP, "Terminated Agents we want back")
    stats["want_back_total"] = len(want_back)

    # Step 6: Process "Want Back" - Add to Former Agents board if not in CRM and not blocklisted
    print()
    print("Processing 'Want Back' agents...")
    print("-" * 40)

    for agent in want_back:
        # Skip if in blocklist
        if agent["email"] in blocklist_emails or agent["phone"] in blocklist_phones:
            continue

        # Skip if already in Former Agents board
        if agent["id"] in former_agent_ids:
            stats["already_in_former"] += 1
            continue

        # Skip if already in CRM
        if (agent["email"] and agent["email"] in crm_emails) or \
           (agent["phone"] and agent["phone"] in crm_phones):
            stats["already_in_crm"] += 1
            continue

        # Create in Former Agents board
        if create_former_agent(agent, args.dry_run):
            stats["created"] += 1
            print(f"  ✓ Created: {agent['name']}")
        else:
            stats["failed"] += 1
            print(f"  ✗ Failed: {agent['name']}")

    # Summary
    print()
    print("=" * 60)
    print("Sync Complete!")
    print("=" * 60)
    print(f"\nResults:")
    print(f"  'Want Back' agents: {stats['want_back_total']}")
    print(f"    Already in Former Agents board: {stats['already_in_former']}")
    print(f"    Already in CRM: {stats['already_in_crm']}")
    print(f"    Created in Former Agents: {stats['created']}")
    print(f"  'Don't Want Back' agents: {stats['dont_want_total']}")
    print(f"    Removed from CRM: {stats['removed_from_crm']}")
    print(f"  Failed: {stats['failed']}")


if __name__ == "__main__":
    main()
