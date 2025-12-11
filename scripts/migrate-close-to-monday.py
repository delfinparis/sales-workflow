#!/usr/bin/env python3
"""
Close CRM to Monday.com Migration Script - COMPLETE VERSION

Migrates ALL leads from Close CRM to Monday.com:
- DJ's leads → Superlative board (assigned to DJ)
- Tim's leads → Superlative board (assigned to DJ)
- Aileen's leads → Superlative board (assigned to Ana), Kale Agent → Closed Leads
- Rea's cold leads → Newly Licensed board with 1-year hibernation
- Rea's active leads → Superlative board (assigned to DJ)
- Rea's Kale Agent leads → Closed Leads board
- Unassigned leads → Superlative board (assigned to DJ), Kale Agent → Closed Leads

Usage:
  DRY_RUN=true python3 scripts/migrate-close-to-monday.py   # Preview only
  python3 scripts/migrate-close-to-monday.py                 # Execute migration
"""

import requests
import json
import time
import os
from datetime import datetime, timedelta

# API Configuration
CLOSE_API_KEY = "api_3U6OkyHlWF2pIcVusIZf2V.1uT08KKRosiYWBy8fH6B4L"
CLOSE_BASE_URL = "https://api.close.com/api/v1/"
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzMDE5NDQxNywiYWFpIjoxMSwidWlkIjoxMDk5MzEwNywiaWFkIjoiMjAyNC0wMy0wN1QyMTo1MDoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NDk2MDA1OSwicmduIjoidXNlMSJ9.m3bCdQF0HwlTYrLQy4-fbTtv04A8RPxzTsWeTsGHFfI"
MONDAY_API_URL = "https://api.monday.com/v2"

# Close CRM IDs
LEAD_OWNER_FIELD = "cf_8XeOgI61X7ks89bycJoNnXYdxbILwjaWx0m7Qq6IAAl"
LEAD_SOURCE_FIELD = "cf_U9j9E5v9LuS4SMLZfI854gU88tmhi0GLVlxtzbZp1yD"

# Close User IDs
DJ_CLOSE_ID = "user_AP0Edi94oMcrN6LGAm9Gcy0ebFjy3F0bRonhocDFeO1"
REA_CLOSE_ID = "user_dDXNoNN8voWPjdLp6jxW27aSA96ezyIRHWvYE2yBaQq"
ANA_CLOSE_ID = "user_DBMZmo4TP2tILMtbDsIVQnSU9JJ0WM0YoXS9Ly7izlh"
AILEEN_CLOSE_ID = "user_cUe328ab6kjnxlUZPrKNrU5GrBb0BYHbpicB46rbj1z"
TIM_CLOSE_ID = "user_kHYbqNSf6bBO9cuhN0OkaMRgnsAZoXirNt565R0OiEJ"

# Monday Board IDs
SUPERLATIVE_BOARD = "18390370563"
NEWLY_LICENSED_BOARD = "18391158354"
CLOSED_LEADS_BOARD = "18391860337"

# Monday User IDs
DJ_MONDAY_ID = 10993107
REA_MONDAY_ID = 10995945
ANA_MONDAY_ID = 97053956

# Monday Group IDs (default groups)
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

# Dry run mode
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

# Rate limiting
CLOSE_RATE_LIMIT = 0.2  # seconds between Close API calls
MONDAY_RATE_LIMIT = 0.3  # seconds between Monday API calls

# Global stats
global_stats = {
    "superlative": {"created": 0, "errors": 0, "no_email": 0},
    "newly_licensed": {"created": 0, "errors": 0, "no_email": 0},
    "closed_leads": {"created": 0, "errors": 0, "no_email": 0},
}


def close_request(endpoint, method="GET", params=None, data=None):
    """Make a request to Close CRM API."""
    url = f"{CLOSE_BASE_URL}{endpoint}"
    response = requests.request(
        method,
        url,
        auth=(CLOSE_API_KEY, ""),
        params=params,
        json=data
    )
    time.sleep(CLOSE_RATE_LIMIT)
    return response.json()


def monday_request(query, variables=None):
    """Make a request to Monday.com API."""
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(MONDAY_API_URL, headers=headers, json=payload)
    time.sleep(MONDAY_RATE_LIMIT)
    return response.json()


def get_all_close_leads_by_owner(owner_id, owner_name):
    """Fetch all leads from Close CRM for a specific owner."""
    print(f"  Fetching {owner_name}'s leads from Close CRM...")

    leads = []
    has_more = True
    skip = 0
    limit = 100

    if owner_id is None:
        # Query for leads with no owner
        query = f'NOT has:custom.{LEAD_OWNER_FIELD}'
    else:
        query = f'custom.{LEAD_OWNER_FIELD}:"{owner_id}"'

    while has_more:
        params = {
            "query": query,
            "_skip": skip,
            "_limit": limit,
            "_fields": "id,display_name,status_label,contacts,date_created,custom"
        }

        result = close_request("lead/", params=params)
        batch = result.get("data", [])
        leads.extend(batch)

        has_more = result.get("has_more", False)
        skip += limit

        if len(leads) % 500 == 0:
            print(f"    Fetched {len(leads)} leads...")

    print(f"    Total {owner_name} leads: {len(leads)}")
    return leads


def extract_contact_info(lead):
    """Extract first contact's name, email, phone from Close lead."""
    contacts = lead.get("contacts", [])
    if not contacts:
        return None, None, None, None

    contact = contacts[0]
    name = contact.get("name") or ""
    name_parts = name.split(" ", 1) if name else []
    first_name = name_parts[0] if name_parts else ""
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    emails = contact.get("emails", [])
    email = emails[0].get("email", "") if emails else ""

    phones = contact.get("phones", [])
    phone = phones[0].get("phone", "") if phones else ""

    return first_name, last_name, email, phone


def get_lead_source(lead):
    """Get lead source from Close custom field."""
    custom = lead.get("custom", {})
    return custom.get(LEAD_SOURCE_FIELD, "")


def create_superlative_item(lead, first_name, last_name, email, phone, assigned_to_id):
    """Create item in Superlative board."""
    if DRY_RUN:
        return "DRY_RUN"

    name = f"{first_name} {last_name}".strip() or lead.get("display_name", "Unknown")
    close_id = lead.get("id", "")
    date_created = lead.get("date_created", "")[:10]  # YYYY-MM-DD
    status_label = lead.get("status_label", "Top Of Funnel")
    status_index = SUPERLATIVE_STATUS_MAP.get(status_label, 5)  # Default to New Lead
    lead_source = get_lead_source(lead)

    # Column values for Superlative board
    column_values = {
        "text_mky6wn9s": first_name,  # First Name
        "text_mky6whek": last_name,   # Last Name
        "email_mky6p7cy": {"email": email, "text": email} if email else None,
        "phone_mky6fr9j": {"phone": phone, "countryShortName": "US"} if phone else None,
        "multiple_person_mky6jgt4": {"personsAndTeams": [{"id": assigned_to_id, "kind": "person"}]},
        "date_mky6ky4j": {"date": date_created} if date_created else None,  # First Contact Date
        "text_mkyhaqf0": close_id,  # Close Lead ID
        "status": {"index": status_index},  # Status
        "text_mkyffxfn": lead_source or status_label,  # Lead Source (Close)
    }

    # Remove None values
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
        print(f"    Error creating superlative item: {result}")
        return None


def create_newly_licensed_item(lead, first_name, last_name, email, phone):
    """Create item in Newly Licensed board with 1-year hibernation."""
    if DRY_RUN:
        return "DRY_RUN"

    name = f"{first_name} {last_name}".strip() or lead.get("display_name", "Unknown")
    close_id = lead.get("id", "")
    today = datetime.now().strftime("%Y-%m-%d")
    hibernate_until = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    lead_source = get_lead_source(lead)
    status_label = lead.get("status_label", "")

    # Column values for Newly Licensed board
    column_values = {
        "text_mkybe1vc": first_name,  # First Name
        "text_mkyb85z9": last_name,   # Last Name
        "email_mkybfqax": {"email": email, "text": email} if email else None,
        "phone_mkyb4cr0": {"phone": phone, "countryShortName": "US"} if phone else None,
        "multiple_person_mkyb4wzn": {"personsAndTeams": [{"id": REA_MONDAY_ID, "kind": "person"}]},
        "date_mkybk1hp": {"date": today},  # Import Date
        "color_mkybxbyk": {"index": 1},  # Lead Status: "Never Responded"
        "text_mkyb1a5v": close_id,  # Close CRM Lead ID
        "date_mkyb1317": {"date": hibernate_until},  # Hibernation Until
        "text_mkyfrjqv": lead_source or status_label,  # Lead Source (Close)
    }

    # Remove None values
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
        print(f"    Error creating newly licensed item: {result}")
        return None


def create_closed_leads_item(lead, first_name, last_name, email, phone, original_owner):
    """Create item in Closed Leads board."""
    if DRY_RUN:
        return "DRY_RUN"

    name = f"{first_name} {last_name}".strip() or lead.get("display_name", "Unknown")
    close_id = lead.get("id", "")
    today = datetime.now().strftime("%Y-%m-%d")

    # Column values for Closed Leads board
    column_values = {
        "text_mkyh58bq": first_name,  # First Name
        "text_mkyhzkee": last_name,   # Last Name
        "email_mkyh4hrg": {"email": email, "text": email} if email else None,
        "phone_mkyhe6mx": {"phone": phone, "countryShortName": "US"} if phone else None,
        "text_mkyhbyr2": close_id,  # Close Lead ID
        "date_mkyhn9j9": {"date": today},  # Close Date
        "text_mkyhvxbd": original_owner,  # Original Lead Owner
    }

    # Remove None values
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
        print(f"    Error creating closed leads item: {result}")
        return None


def process_lead(lead, destination, assigned_to_id, original_owner):
    """Process a single lead and route to appropriate board."""
    first_name, last_name, email, phone = extract_contact_info(lead)

    if not email:
        global_stats[destination]["no_email"] += 1
        return False

    if destination == "superlative":
        item_id = create_superlative_item(lead, first_name, last_name, email, phone, assigned_to_id)
    elif destination == "newly_licensed":
        item_id = create_newly_licensed_item(lead, first_name, last_name, email, phone)
    elif destination == "closed_leads":
        item_id = create_closed_leads_item(lead, first_name, last_name, email, phone, original_owner)
    else:
        return False

    if item_id:
        global_stats[destination]["created"] += 1
        return True
    else:
        global_stats[destination]["errors"] += 1
        return False


def migrate_dj_leads():
    """Migrate DJ's leads to Superlative board."""
    print("\n" + "=" * 60)
    print("MIGRATING DJ'S LEADS")
    print("=" * 60)

    leads = get_all_close_leads_by_owner(DJ_CLOSE_ID, "DJ")

    kale_agent_count = 0
    processed = 0

    for lead in leads:
        status = lead.get("status_label", "")

        if status == CLOSED_STATUS:
            process_lead(lead, "closed_leads", None, "DJ")
            kale_agent_count += 1
        else:
            process_lead(lead, "superlative", DJ_MONDAY_ID, "DJ")

        processed += 1
        if processed % 100 == 0:
            print(f"    Processed {processed}/{len(leads)}...")

    print(f"  → {len(leads) - kale_agent_count} to Superlative, {kale_agent_count} to Closed Leads")


def migrate_tim_leads():
    """Migrate Tim's leads to Superlative board (assigned to DJ)."""
    print("\n" + "=" * 60)
    print("MIGRATING TIM'S LEADS (→ DJ)")
    print("=" * 60)

    leads = get_all_close_leads_by_owner(TIM_CLOSE_ID, "Tim")

    kale_agent_count = 0
    processed = 0

    for lead in leads:
        status = lead.get("status_label", "")

        if status == CLOSED_STATUS:
            process_lead(lead, "closed_leads", None, "Tim")
            kale_agent_count += 1
        else:
            process_lead(lead, "superlative", DJ_MONDAY_ID, "Tim")  # Assign to DJ

        processed += 1

    print(f"  → {len(leads) - kale_agent_count} to Superlative (DJ), {kale_agent_count} to Closed Leads")


def migrate_aileen_leads():
    """Migrate Aileen's leads to Superlative board (assigned to Ana)."""
    print("\n" + "=" * 60)
    print("MIGRATING AILEEN'S LEADS (→ Ana)")
    print("=" * 60)

    leads = get_all_close_leads_by_owner(AILEEN_CLOSE_ID, "Aileen")

    kale_agent_count = 0
    processed = 0

    for lead in leads:
        status = lead.get("status_label", "")

        if status == CLOSED_STATUS:
            process_lead(lead, "closed_leads", None, "Aileen")
            kale_agent_count += 1
        else:
            process_lead(lead, "superlative", ANA_MONDAY_ID, "Aileen")  # Assign to Ana

        processed += 1
        if processed % 100 == 0:
            print(f"    Processed {processed}/{len(leads)}...")

    print(f"  → {len(leads) - kale_agent_count} to Superlative (Ana), {kale_agent_count} to Closed Leads")


def migrate_ana_leads():
    """Migrate Ana's leads to Superlative board."""
    print("\n" + "=" * 60)
    print("MIGRATING ANA'S LEADS")
    print("=" * 60)

    leads = get_all_close_leads_by_owner(ANA_CLOSE_ID, "Ana")

    kale_agent_count = 0
    processed = 0

    for lead in leads:
        status = lead.get("status_label", "")

        if status == CLOSED_STATUS:
            process_lead(lead, "closed_leads", None, "Ana")
            kale_agent_count += 1
        else:
            process_lead(lead, "superlative", ANA_MONDAY_ID, "Ana")

        processed += 1

    print(f"  → {len(leads) - kale_agent_count} to Superlative, {kale_agent_count} to Closed Leads")


def migrate_rea_leads():
    """Migrate Rea's leads - cold to Newly Licensed, active to Superlative."""
    print("\n" + "=" * 60)
    print("MIGRATING REA'S LEADS")
    print("=" * 60)

    leads = get_all_close_leads_by_owner(REA_CLOSE_ID, "Rea")

    newly_licensed_count = 0
    superlative_count = 0
    kale_agent_count = 0
    processed = 0

    for lead in leads:
        status = lead.get("status_label", "")

        if status == CLOSED_STATUS:
            process_lead(lead, "closed_leads", None, "Rea")
            kale_agent_count += 1
        elif status in NEWLY_LICENSED_STATUSES:
            process_lead(lead, "newly_licensed", REA_MONDAY_ID, "Rea")
            newly_licensed_count += 1
        else:
            # Active leads go to Superlative, assigned to DJ
            process_lead(lead, "superlative", DJ_MONDAY_ID, "Rea")
            superlative_count += 1

        processed += 1
        if processed % 100 == 0:
            print(f"    Processed {processed}/{len(leads)}...")

    print(f"  → {newly_licensed_count} to Newly Licensed, {superlative_count} to Superlative (DJ), {kale_agent_count} to Closed Leads")


def migrate_unassigned_leads():
    """Migrate unassigned leads to Superlative board (assigned to DJ)."""
    print("\n" + "=" * 60)
    print("MIGRATING UNASSIGNED LEADS (→ DJ)")
    print("=" * 60)

    leads = get_all_close_leads_by_owner(None, "Unassigned")

    kale_agent_count = 0
    processed = 0

    for lead in leads:
        status = lead.get("status_label", "")

        if status == CLOSED_STATUS:
            process_lead(lead, "closed_leads", None, "Unassigned")
            kale_agent_count += 1
        else:
            process_lead(lead, "superlative", DJ_MONDAY_ID, "Unassigned")

        processed += 1

    print(f"  → {len(leads) - kale_agent_count} to Superlative (DJ), {kale_agent_count} to Closed Leads")


def print_summary():
    """Print final migration summary."""
    print("\n" + "=" * 60)
    print("MIGRATION SUMMARY")
    print("=" * 60)

    total_created = 0
    total_errors = 0
    total_no_email = 0

    for board, stats in global_stats.items():
        print(f"\n{board.upper().replace('_', ' ')} BOARD:")
        print(f"  Created: {stats['created']}")
        print(f"  Errors: {stats['errors']}")
        print(f"  No email (skipped): {stats['no_email']}")
        total_created += stats['created']
        total_errors += stats['errors']
        total_no_email += stats['no_email']

    print(f"\nTOTAL:")
    print(f"  Created: {total_created}")
    print(f"  Errors: {total_errors}")
    print(f"  No email (skipped): {total_no_email}")
    print(f"  Grand Total Processed: {total_created + total_errors + total_no_email}")


def main():
    print("=" * 60)
    print("CLOSE CRM TO MONDAY.COM MIGRATION")
    print("=" * 60)
    print(f"Mode: {'DRY RUN (no changes will be made)' if DRY_RUN else 'LIVE MIGRATION'}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Run all migrations in order
    migrate_dj_leads()
    migrate_tim_leads()
    migrate_aileen_leads()
    migrate_ana_leads()
    migrate_rea_leads()
    migrate_unassigned_leads()

    # Print summary
    print_summary()

    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
