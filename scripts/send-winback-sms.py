#!/usr/bin/env python3
"""
Win-Back SMS Script

Sends personalized SMS to former agents 90 days after termination,
offering free access to the Kale Listing AI tool.

Runs daily via GitHub Actions.
"""

import requests
import json
import time
import os
from datetime import datetime, date

# Configuration
MONDAY_API_KEY = os.environ.get("MONDAY_API_KEY")
JUSTCALL_API_KEY = os.environ.get("JUSTCALL_API_KEY")
JUSTCALL_API_SECRET = os.environ.get("JUSTCALL_API_SECRET")

MONDAY_API_URL = "https://api.monday.com/v2"
JUSTCALL_SMS_URL = "https://api.justcall.io/v1/texts/new"

FORMER_AGENTS_BOARD_ID = "18391489234"
WINBACK_DATE_COL = "date_mkygkfv"
WINBACK_SENT_COL = "boolean_mkygr6v"
FIRST_NAME_COL = "text_mkyfws0a"
PHONE_COL = "phone_mkyfkn1f"

SMS_MESSAGE = """Hey {first_name} - hope all is well! I just launched this listing description AI tool and would love your feedback. It researches your neighborhood and rewrites listings to get more showings.

Try it free: listing.joinkale.com

Let me know what you think? No strings - just want honest feedback from someone who knows their stuff.

- DJ"""

def monday_query(query):
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json",
        "API-Version": "2024-10"
    }
    response = requests.post(MONDAY_API_URL, headers=headers, json={"query": query})
    return response.json().get("data")

def get_todays_winbacks():
    """Get former agents where Win-Back Date = today and Win-Back Sent = false."""
    today = date.today().isoformat()

    query = """
    query {
        boards(ids: [%s]) {
            items_page(limit: 100) {
                items {
                    id
                    name
                    column_values {
                        id
                        text
                        value
                    }
                }
            }
        }
    }
    """ % FORMER_AGENTS_BOARD_ID

    result = monday_query(query)
    items = result.get("boards", [{}])[0].get("items_page", {}).get("items", [])

    ready_items = []
    for item in items:
        cols = {c["id"]: c for c in item.get("column_values", [])}

        winback_date = cols.get(WINBACK_DATE_COL, {}).get("text", "")
        winback_sent = cols.get(WINBACK_SENT_COL, {}).get("text", "")

        if winback_date == today and winback_sent != "true":
            first_name = cols.get(FIRST_NAME_COL, {}).get("text", "")
            phone_data = cols.get(PHONE_COL, {}).get("value", "{}")
            phone = json.loads(phone_data).get("phone", "") if phone_data else ""

            if phone and first_name:
                ready_items.append({
                    "id": item["id"],
                    "name": item["name"],
                    "first_name": first_name,
                    "phone": phone
                })

    return ready_items

def send_sms(phone, message):
    """Send SMS via JustCall API."""
    headers = {
        "Authorization": f"{JUSTCALL_API_KEY}:{JUSTCALL_API_SECRET}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": phone,
        "body": message
    }
    response = requests.post(JUSTCALL_SMS_URL, headers=headers, json=payload)
    return response.status_code == 200

def mark_sent(item_id):
    """Mark Win-Back Sent = true on Monday item."""
    query = """
    mutation {
        change_column_value(
            board_id: %s,
            item_id: %s,
            column_id: "%s",
            value: "{\\"checked\\": true}"
        ) {
            id
        }
    }
    """ % (FORMER_AGENTS_BOARD_ID, item_id, WINBACK_SENT_COL)

    return monday_query(query)

def create_update(item_id, message):
    """Create update note on Monday item."""
    query = """
    mutation {
        create_update(
            item_id: %s,
            body: "%s"
        ) {
            id
        }
    }
    """ % (item_id, message.replace('"', '\\"').replace('\n', '\\n'))

    return monday_query(query)

def main():
    print("=" * 60)
    print("Win-Back SMS Script")
    print(f"Date: {date.today().isoformat()}")
    print("=" * 60)

    items = get_todays_winbacks()
    print(f"Found {len(items)} agents ready for win-back SMS")

    stats = {"sent": 0, "failed": 0}

    for item in items:
        message = SMS_MESSAGE.format(first_name=item["first_name"])

        print(f"  Sending to {item['name']} ({item['phone']})...", end=" ")

        if send_sms(item["phone"], message):
            mark_sent(item["id"])
            create_update(item["id"],
                f"Win-back SMS sent via JustCall.\\n\\n"
                f"Message: {message[:100]}...")
            print("SENT")
            stats["sent"] += 1
        else:
            print("FAILED")
            stats["failed"] += 1

        time.sleep(1)  # Rate limiting

    print()
    print("=" * 60)
    print("Complete!")
    print(f"  Sent: {stats['sent']}")
    print(f"  Failed: {stats['failed']}")

if __name__ == "__main__":
    main()
