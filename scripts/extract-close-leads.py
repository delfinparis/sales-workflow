#!/usr/bin/env python3
"""
Close CRM Lead Extraction Script - BATCH MODE

Extracts ALL leads from Close CRM and saves to a local JSON file.
This is Step 1 of a 2-step migration process.

Features:
- Downloads leads in batches of 200
- Saves after each batch (crash-resistant)
- Resume capability - tracks processed IDs
- Detailed logging

Usage:
  python3 scripts/extract-close-leads.py
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

# API Configuration
CLOSE_API_KEY = "api_3U6OkyHlWF2pIcVusIZf2V.1uT08KKRosiYWBy8fH6B4L"
CLOSE_BASE_URL = "https://api.close.com/api/v1/"

# Close CRM IDs
LEAD_OWNER_FIELD = "cf_8XeOgI61X7ks89bycJoNnXYdxbILwjaWx0m7Qq6IAAl"
LEAD_SOURCE_FIELD = "cf_U9j9E5v9LuS4SMLZfI854gU88tmhi0GLVlxtzbZp1yD"
OFFICE_NAME_FIELD = "cf_XPSkF9vmCkjQJU4tkjFUV0EethSIAt8qqHiHZsjK3Sm"

# Close User IDs - map to owner names
CLOSE_USER_MAP = {
    "user_AP0Edi94oMcrN6LGAm9Gcy0ebFjy3F0bRonhocDFeO1": "DJ",
    "user_dDXNoNN8voWPjdLp6jxW27aSA96ezyIRHWvYE2yBaQq": "Rea",
    "user_DBMZmo4TP2tILMtbDsIVQnSU9JJ0WM0YoXS9Ly7izlh": "Ana",
    "user_cUe328ab6kjnxlUZPrKNrU5GrBb0BYHbpicB46rbj1z": "Aileen",
    "user_kHYbqNSf6bBO9cuhN0OkaMRgnsAZoXirNt565R0OiEJ": "Tim",
}

# Batch size
BATCH_SIZE = 200

# Rate limiting
CLOSE_RATE_LIMIT = 0.15  # seconds between Close API calls

# Output files
SCRIPT_DIR = Path(__file__).parent
OUTPUT_FILE = SCRIPT_DIR / "close_leads_export.json"
LOG_FILE = SCRIPT_DIR / "extract_log.txt"


def log(message):
    """Log message to file and console."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")


def close_request(endpoint, method="GET", params=None, data=None, retries=3):
    """Make a request to Close CRM API with retry logic."""
    url = f"{CLOSE_BASE_URL}{endpoint}"

    for attempt in range(retries):
        try:
            response = requests.request(
                method,
                url,
                auth=(CLOSE_API_KEY, ""),
                params=params,
                json=data,
                timeout=30
            )
            time.sleep(CLOSE_RATE_LIMIT)

            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After', 10))
                log(f"  Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            if response.status_code >= 400:
                log(f"  API error {response.status_code}: {response.text[:200]}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue

            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
                log(f"  Request failed: {e}. Retrying in {2 ** attempt}s...")
                time.sleep(2 ** attempt)
            else:
                raise

    return {}


def get_lead_activities(lead_id, limit=5):
    """Fetch recent activities for a lead."""
    activities = []
    params = {
        "lead_id": lead_id,
        "_limit": limit,
        "_order_by": "-date_created"
    }

    try:
        result = close_request("activity/", params=params)
        raw_activities = result.get("data", [])

        for act in raw_activities:
            act_type = act.get("_type", "")
            date = act.get("date_created", "")[:10]

            if act_type == "Email":
                direction = "Sent" if act.get("direction") == "outgoing" else "Received"
                subject = act.get("subject", "(no subject)")[:50]
                activities.append(f"[{date}] Email {direction}: {subject}")
            elif act_type == "SMS":
                direction = "Sent" if act.get("direction") == "outgoing" else "Received"
                text = act.get("text", "")[:50]
                activities.append(f"[{date}] SMS {direction}: {text}")
            elif act_type == "Call":
                direction = act.get("direction", "")
                duration = act.get("duration", 0)
                activities.append(f"[{date}] Call ({direction}, {duration}s)")
            elif act_type == "Note":
                note = act.get("note", "")[:50]
                activities.append(f"[{date}] Note: {note}")
            elif act_type == "Meeting":
                title = act.get("title", "Meeting")[:50]
                activities.append(f"[{date}] Meeting: {title}")
    except Exception as e:
        pass  # Skip activities if they fail

    return activities


def extract_contact_info(lead):
    """Extract contact info from Close lead."""
    contacts = lead.get("contacts", [])
    if not contacts:
        return {"first_name": "", "last_name": "", "email": "", "phone": ""}

    contact = contacts[0]
    name = contact.get("name") or ""
    name_parts = name.split(" ", 1) if name else []

    emails = contact.get("emails", [])
    phones = contact.get("phones", [])

    return {
        "first_name": name_parts[0] if name_parts else "",
        "last_name": name_parts[1] if len(name_parts) > 1 else "",
        "email": emails[0].get("email", "") if emails else "",
        "phone": phones[0].get("phone", "") if phones else ""
    }


def get_owner_name(lead):
    """Get owner name from lead custom field."""
    custom = lead.get("custom", {})
    owner_id = custom.get(LEAD_OWNER_FIELD, "")
    return CLOSE_USER_MAP.get(owner_id, "Unassigned")


def get_lead_source(lead):
    """Get lead source from Close custom field."""
    custom = lead.get("custom", {})
    return custom.get(LEAD_SOURCE_FIELD, "")


def get_office_name(lead):
    """Get office name from Close custom field."""
    custom = lead.get("custom", {})
    return custom.get(OFFICE_NAME_FIELD, "")


def load_existing_export():
    """Load existing export file if it exists."""
    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r") as f:
                data = json.load(f)
                leads = {lead["close_id"]: lead for lead in data.get("leads", [])}
                log(f"Loaded {len(leads)} existing leads from export file")
                return leads
        except Exception as e:
            log(f"Could not load existing export: {e}")
    return {}


def save_export(leads_dict):
    """Save leads to JSON file."""
    leads = list(leads_dict.values())

    # Generate summaries
    by_owner = {}
    by_status = {}
    for lead in leads:
        owner = lead.get("owner", "Unassigned")
        status = lead.get("status_label", "Unknown")
        by_owner[owner] = by_owner.get(owner, 0) + 1
        by_status[status] = by_status.get(status, 0) + 1

    export_data = {
        "export_date": datetime.now().isoformat(),
        "total_leads": len(leads),
        "summary_by_owner": by_owner,
        "summary_by_status": by_status,
        "leads": leads
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(export_data, f, indent=2)

    return by_owner, by_status


def main():
    log("=" * 60)
    log("CLOSE CRM LEAD EXTRACTION - BATCH MODE")
    log("=" * 60)
    log(f"Batch size: {BATCH_SIZE}")

    # Load existing data for resume
    leads_dict = load_existing_export()
    existing_ids = set(leads_dict.keys())

    # First, get total count
    log("\nCounting total leads in Close CRM...")
    count_result = close_request("lead/", params={"_limit": 1})
    # Close doesn't give total count easily, so we'll discover as we go

    # Fetch all leads in batches
    log("\nFetching leads from Close API...")
    has_more = True
    skip = 0
    batch_num = 0
    new_leads_count = 0

    while has_more:
        batch_num += 1
        log(f"\n--- Batch {batch_num} (skip={skip}) ---")

        params = {
            "_skip": skip,
            "_limit": BATCH_SIZE,
            "_fields": "id,display_name,status_label,contacts,date_created,custom"
        }

        result = close_request("lead/", params=params)
        batch = result.get("data", [])

        if not batch:
            break

        batch_new = 0
        batch_skip = 0

        for lead in batch:
            lead_id = lead.get("id")

            # Skip if already extracted
            if lead_id in existing_ids:
                batch_skip += 1
                continue

            # Extract and enrich lead data
            contact_info = extract_contact_info(lead)
            owner_name = get_owner_name(lead)
            lead_source = get_lead_source(lead)
            office_name = get_office_name(lead)
            activities = get_lead_activities(lead_id, limit=5)

            enriched_lead = {
                "close_id": lead_id,
                "display_name": lead.get("display_name", ""),
                "status_label": lead.get("status_label", ""),
                "date_created": lead.get("date_created", "")[:10] if lead.get("date_created") else "",
                "owner": owner_name,
                "lead_source": lead_source,
                "office_name": office_name,
                "first_name": contact_info["first_name"],
                "last_name": contact_info["last_name"],
                "email": contact_info["email"],
                "phone": contact_info["phone"],
                "activities": activities,
                "extracted_at": datetime.now().isoformat()
            }

            leads_dict[lead_id] = enriched_lead
            existing_ids.add(lead_id)
            batch_new += 1
            new_leads_count += 1

        log(f"  Batch {batch_num}: {batch_new} new, {batch_skip} skipped")
        log(f"  Total extracted: {len(leads_dict)}")

        # Save after each batch (crash resistant!)
        by_owner, _ = save_export(leads_dict)
        log(f"  Saved to {OUTPUT_FILE.name}")

        has_more = result.get("has_more", False)
        skip += BATCH_SIZE

    # Final summary
    log("\n" + "=" * 60)
    log("EXTRACTION COMPLETE")
    log("=" * 60)
    log(f"Total leads in export: {len(leads_dict)}")
    log(f"New leads this run: {new_leads_count}")
    log(f"Output file: {OUTPUT_FILE}")

    # Display summary
    with open(OUTPUT_FILE, "r") as f:
        data = json.load(f)

    log("\nBy Owner:")
    for owner, count in sorted(data["summary_by_owner"].items()):
        log(f"  {owner}: {count}")

    log("\nBy Status:")
    for status, count in sorted(data["summary_by_status"].items()):
        log(f"  {status}: {count}")

    log("\n" + "=" * 60)
    log("Next step: python3 scripts/push-to-monday.py")
    log("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log("\nInterrupted! Progress has been saved. Run again to resume.")
    except Exception as e:
        log(f"\nError: {e}")
        log("Progress has been saved. Run again to resume.")
        raise
