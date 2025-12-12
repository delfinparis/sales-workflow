#!/usr/bin/env python3
"""
Push Leads to Monday.com - BATCH MODE

Reads leads from close_leads_export.json and pushes to Monday.com boards.
This is Step 2 of a 2-step migration process.

Features:
- Processes leads in batches of 200
- Saves progress after each batch (crash-resistant)
- Resume capability - tracks pushed lead IDs
- Detailed logging
- Routes leads based on owner and status

Routing Rules:
- DJ's leads → Superlative board (assigned to DJ)
- Tim's leads → Superlative board (assigned to DJ)
- Aileen's leads → Superlative board (assigned to Ana), Kale Agent → Closed Leads
- Ana's leads → Superlative board (assigned to Ana), Kale Agent → Closed Leads
- Rea's cold leads → Newly Licensed board with 1-year hibernation
- Rea's active leads → Superlative board (assigned to DJ)
- Rea's Kale Agent leads → Closed Leads board
- Unassigned leads → Superlative board (assigned to DJ), Kale Agent → Closed Leads

Usage:
  python3 scripts/push-to-monday.py              # Run migration
  DRY_RUN=true python3 scripts/push-to-monday.py # Preview only
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path

# API Configuration
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzMDE5NDQxNywiYWFpIjoxMSwidWlkIjoxMDk5MzEwNywiaWFkIjoiMjAyNC0wMy0wN1QyMTo1MDoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NDk2MDA1OSwicmduIjoidXNlMSJ9.m3bCdQF0HwlTYrLQy4-fbTtv04A8RPxzTsWeTsGHFfI"
MONDAY_API_URL = "https://api.monday.com/v2"

# Monday Board IDs
SUPERLATIVE_BOARD = "18390370563"
NEWLY_LICENSED_BOARD = "18391158354"
CLOSED_LEADS_BOARD = "18391860337"

# Monday User IDs
DJ_MONDAY_ID = 10993107
REA_MONDAY_ID = 10995945
ANA_MONDAY_ID = 97053956

# Monday Group IDs
SUPERLATIVE_NEW_LEAD_GROUP = "topics"
NEWLY_LICENSED_NEVER_RESPONDED_GROUP = "group_mkyb6hgy"
CLOSED_LEADS_GROUP = "topics"

# Close status to Monday status mapping for Superlative board
SUPERLATIVE_STATUS_MAP = {
    "Top Of Funnel": 5,       # New Lead
    "Never Responded": 5,      # New Lead
    "Cold Reach Out": 5,       # New Lead
    "Qualify": 10,             # Ask Made
    "Present": 13,             # DJ Meeting Complete
    "Propose": 14,             # Offer Extended
    "Paperwork Sent": 14,      # Offer Extended
    "HC Application": 14,      # Offer Extended
    "Bad Fit": 19,             # Lost - Not Qualified
    "Lost": 17,                # Lost - Not Interested
    "Not Right Now": 102,      # Hibernation 90-Day
}

# Statuses that should go to Newly Licensed board for Rea's cold leads
NEWLY_LICENSED_STATUSES = ["Top Of Funnel", "Never Responded", "Lost", "Not Right Now"]

# Status that indicates already joined Kale
CLOSED_STATUS = "Kale Agent"

# Batch size
BATCH_SIZE = 200

# Rate limiting
MONDAY_RATE_LIMIT = 0.25  # seconds between Monday API calls

# Mode
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

# Files
SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = SCRIPT_DIR / "close_leads_export.json"
PROGRESS_FILE = SCRIPT_DIR / "push_progress.json"
LOG_FILE = SCRIPT_DIR / "push_log.txt"

# Stats
stats = {
    "superlative": {"created": 0, "errors": 0, "no_email": 0},
    "newly_licensed": {"created": 0, "errors": 0, "no_email": 0},
    "closed_leads": {"created": 0, "errors": 0, "no_email": 0},
}


def log(message):
    """Log message to file and console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")


def monday_request(query, variables=None, retries=3):
    """Make a request to Monday.com API with retry logic."""
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    for attempt in range(retries):
        try:
            response = requests.post(MONDAY_API_URL, headers=headers, json=payload, timeout=30)
            time.sleep(MONDAY_RATE_LIMIT)

            result = response.json()

            # Check for rate limiting
            if "errors" in result:
                error_msg = str(result["errors"])
                if "rate" in error_msg.lower() or "limit" in error_msg.lower():
                    wait_time = 10
                    log(f"  Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

            return result
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                log(f"  Request failed: {e}. Retrying in {2 ** attempt}s...")
                time.sleep(2 ** attempt)
            else:
                raise

    return {}


def load_progress():
    """Load push progress."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r") as f:
            data = json.load(f)
            return set(data.get("pushed_ids", []))
    return set()


def save_progress(pushed_ids):
    """Save push progress."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump({
            "pushed_ids": list(pushed_ids),
            "stats": stats,
            "last_updated": datetime.now().isoformat()
        }, f, indent=2)


def format_activity_summary(activities):
    """Format activities into a notes string."""
    if not activities:
        return ""
    summary = "--- Close CRM Activity History ---\n"
    summary += "\n".join(activities)
    return summary


def create_superlative_item(lead, assigned_to_id):
    """Create item in Superlative board."""
    if DRY_RUN:
        return "DRY_RUN"

    name = f"{lead['first_name']} {lead['last_name']}".strip() or lead.get("display_name", "Unknown")
    close_id = lead.get("close_id", "")
    date_created = lead.get("date_created", "")
    status_label = lead.get("status_label", "Top Of Funnel")
    status_index = SUPERLATIVE_STATUS_MAP.get(status_label, 5)
    lead_source = lead.get("lead_source", "")
    email = lead.get("email", "")
    phone = lead.get("phone", "")
    office_name = lead.get("office_name", "")
    activities = lead.get("activities", [])
    activity_summary = format_activity_summary(activities)

    column_values = {
        "text_mky6wn9s": lead["first_name"],
        "text_mky6whek": lead["last_name"],
        "email_mky6p7cy": {"email": email, "text": email} if email else None,
        "phone_mky6fr9j": {"phone": phone, "countryShortName": "US"} if phone else None,
        "multiple_person_mky6jgt4": {"personsAndTeams": [{"id": assigned_to_id, "kind": "person"}]},
        "date_mky6ky4j": {"date": date_created} if date_created else None,
        "text_mkyhaqf0": close_id,
        "status": {"index": status_index},
        "text_mkyffxfn": lead_source or status_label,
        "text_mky6grjs": office_name,  # Current Brokerage
        "long_text_mky6bj1v": {"text": activity_summary} if activity_summary else None,
    }

    column_values = {k: v for k, v in column_values.items() if v is not None}

    query = """
    mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {
        create_item(
            board_id: $boardId,
            group_id: $groupId,
            item_name: $itemName,
            column_values: $columnValues
        ) {
            id
        }
    }
    """

    variables = {
        "boardId": SUPERLATIVE_BOARD,
        "groupId": SUPERLATIVE_NEW_LEAD_GROUP,
        "itemName": name,
        "columnValues": json.dumps(column_values)
    }

    result = monday_request(query, variables)

    if "data" in result and result["data"].get("create_item"):
        return result["data"]["create_item"]["id"]
    else:
        log(f"    Error: {result}")
        return None


def create_newly_licensed_item(lead):
    """Create item in Newly Licensed board with 1-year hibernation."""
    if DRY_RUN:
        return "DRY_RUN"

    name = f"{lead['first_name']} {lead['last_name']}".strip() or lead.get("display_name", "Unknown")
    close_id = lead.get("close_id", "")
    today = datetime.now().strftime("%Y-%m-%d")
    hibernate_until = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    lead_source = lead.get("lead_source", "")
    status_label = lead.get("status_label", "")
    email = lead.get("email", "")
    phone = lead.get("phone", "")
    office_name = lead.get("office_name", "")
    activities = lead.get("activities", [])
    activity_summary = format_activity_summary(activities)

    column_values = {
        "text_mkybe1vc": lead["first_name"],
        "text_mkyb85z9": lead["last_name"],
        "email_mkybfqax": {"email": email, "text": email} if email else None,
        "phone_mkyb4cr0": {"phone": phone, "countryShortName": "US"} if phone else None,
        "multiple_person_mkyb4wzn": {"personsAndTeams": [{"id": REA_MONDAY_ID, "kind": "person"}]},
        "date_mkybk1hp": {"date": today},
        "color_mkybxbyk": {"index": 9},  # Lead - No Response
        "text_mkyb1a5v": close_id,
        "date_mkyb1317": {"date": hibernate_until},
        "text_mkyfrjqv": lead_source or status_label,
        "text_mkyh307h": office_name,  # Office Name
        "long_text_mkybev5j": {"text": activity_summary} if activity_summary else None,  # Notes
    }

    column_values = {k: v for k, v in column_values.items() if v is not None}

    query = """
    mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {
        create_item(
            board_id: $boardId,
            group_id: $groupId,
            item_name: $itemName,
            column_values: $columnValues
        ) {
            id
        }
    }
    """

    variables = {
        "boardId": NEWLY_LICENSED_BOARD,
        "groupId": NEWLY_LICENSED_NEVER_RESPONDED_GROUP,
        "itemName": name,
        "columnValues": json.dumps(column_values)
    }

    result = monday_request(query, variables)

    if "data" in result and result["data"].get("create_item"):
        return result["data"]["create_item"]["id"]
    else:
        log(f"    Error: {result}")
        return None


def create_closed_leads_item(lead, original_owner):
    """Create item in Closed Leads board."""
    if DRY_RUN:
        return "DRY_RUN"

    name = f"{lead['first_name']} {lead['last_name']}".strip() or lead.get("display_name", "Unknown")
    close_id = lead.get("close_id", "")
    today = datetime.now().strftime("%Y-%m-%d")
    email = lead.get("email", "")
    phone = lead.get("phone", "")
    lead_source = lead.get("lead_source", "")
    status_label = lead.get("status_label", "")
    office_name = lead.get("office_name", "")
    activities = lead.get("activities", [])
    activity_summary = format_activity_summary(activities)

    column_values = {
        "text_mkyh58bq": lead["first_name"],
        "text_mkyhzkee": lead["last_name"],
        "email_mkyh4hrg": {"email": email, "text": email} if email else None,
        "phone_mkyhe6mx": {"phone": phone, "countryShortName": "US"} if phone else None,
        "text_mkyhbyr2": close_id,
        "date_mkyhn9j9": {"date": today},
        "text_mkyhvxbd": original_owner,
        "text_mkyh5w15": lead_source or status_label,  # Lead Source (Close)
        "text_mkyhc4gt": office_name,  # Office Name
        "long_text_mkyhm5hy": {"text": activity_summary} if activity_summary else None,  # Notes
    }

    column_values = {k: v for k, v in column_values.items() if v is not None}

    query = """
    mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON!) {
        create_item(
            board_id: $boardId,
            group_id: $groupId,
            item_name: $itemName,
            column_values: $columnValues
        ) {
            id
        }
    }
    """

    variables = {
        "boardId": CLOSED_LEADS_BOARD,
        "groupId": CLOSED_LEADS_GROUP,
        "itemName": name,
        "columnValues": json.dumps(column_values)
    }

    result = monday_request(query, variables)

    if "data" in result and result["data"].get("create_item"):
        return result["data"]["create_item"]["id"]
    else:
        log(f"    Error: {result}")
        return None


def route_lead(lead, pushed_ids):
    """Route a lead to the appropriate Monday board based on owner and status."""
    close_id = lead.get("close_id")

    # Skip if already pushed
    if close_id in pushed_ids:
        return True, "skipped"

    owner = lead.get("owner", "Unassigned")
    status = lead.get("status_label", "")
    email = lead.get("email", "")

    # Skip leads without email
    if not email:
        return False, "no_email"

    # Determine destination and assignment
    destination = None
    assigned_to = None
    item_id = None

    if status == CLOSED_STATUS:
        # All Kale Agent leads go to Closed Leads
        destination = "closed_leads"
        item_id = create_closed_leads_item(lead, owner)
    elif owner == "DJ":
        destination = "superlative"
        item_id = create_superlative_item(lead, DJ_MONDAY_ID)
    elif owner == "Tim":
        destination = "superlative"
        item_id = create_superlative_item(lead, DJ_MONDAY_ID)  # Assign to DJ
    elif owner == "Aileen":
        destination = "superlative"
        item_id = create_superlative_item(lead, ANA_MONDAY_ID)  # Assign to Ana
    elif owner == "Ana":
        destination = "superlative"
        item_id = create_superlative_item(lead, ANA_MONDAY_ID)
    elif owner == "Rea":
        if status in NEWLY_LICENSED_STATUSES:
            destination = "newly_licensed"
            item_id = create_newly_licensed_item(lead)
        else:
            destination = "superlative"
            item_id = create_superlative_item(lead, DJ_MONDAY_ID)  # Active leads to DJ
    else:  # Unassigned
        destination = "superlative"
        item_id = create_superlative_item(lead, DJ_MONDAY_ID)  # Assign to DJ

    if item_id:
        stats[destination]["created"] += 1
        return True, destination
    else:
        stats[destination]["errors"] += 1
        return False, "error"


def main():
    log("=" * 60)
    log("PUSH LEADS TO MONDAY.COM - BATCH MODE")
    log("=" * 60)
    log(f"Mode: {'DRY RUN' if DRY_RUN else 'LIVE'}")
    log(f"Batch size: {BATCH_SIZE}")

    # Load input data
    if not INPUT_FILE.exists():
        log(f"ERROR: Input file not found: {INPUT_FILE}")
        log("Run extract-close-leads.py first!")
        return

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    leads = data.get("leads", [])
    log(f"Loaded {len(leads)} leads from {INPUT_FILE.name}")

    # Load progress
    pushed_ids = load_progress()
    if pushed_ids:
        log(f"Found {len(pushed_ids)} previously pushed leads")

    # Process in batches
    total_leads = len(leads)
    batch_num = 0
    processed = 0
    new_pushed = 0

    log("\nPushing leads to Monday.com...")

    for i in range(0, total_leads, BATCH_SIZE):
        batch = leads[i:i + BATCH_SIZE]
        batch_num += 1
        batch_created = 0
        batch_skipped = 0
        batch_no_email = 0
        batch_errors = 0

        log(f"\n--- Batch {batch_num} ({i+1}-{min(i+BATCH_SIZE, total_leads)} of {total_leads}) ---")

        for lead in batch:
            close_id = lead.get("close_id")

            if close_id in pushed_ids:
                batch_skipped += 1
                processed += 1
                continue

            success, result = route_lead(lead, pushed_ids)

            if success and result != "skipped":
                pushed_ids.add(close_id)
                batch_created += 1
                new_pushed += 1
            elif result == "no_email":
                batch_no_email += 1
                # Still mark as processed so we don't retry
                pushed_ids.add(close_id)
            elif result == "error":
                batch_errors += 1

            processed += 1

        log(f"  Created: {batch_created}, Skipped: {batch_skipped}, No email: {batch_no_email}, Errors: {batch_errors}")

        # Save progress after each batch
        save_progress(pushed_ids)
        log(f"  Progress saved ({len(pushed_ids)} total pushed)")

    # Final summary
    log("\n" + "=" * 60)
    log("PUSH COMPLETE")
    log("=" * 60)
    log(f"Total processed: {processed}")
    log(f"New leads pushed this run: {new_pushed}")

    log("\nBy Board:")
    for board, board_stats in stats.items():
        log(f"  {board.upper().replace('_', ' ')}:")
        log(f"    Created: {board_stats['created']}")
        log(f"    Errors: {board_stats['errors']}")
        log(f"    No email: {board_stats['no_email']}")

    log(f"\nProgress file: {PROGRESS_FILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\nInterrupted! Progress has been saved. Run again to resume.")
    except Exception as e:
        log(f"\nError: {e}")
        log("Progress has been saved. Run again to resume.")
        raise
