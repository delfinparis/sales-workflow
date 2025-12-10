#!/usr/bin/env python3
"""
Win-Back SMS Script

Sends personalized spintax SMS to former agents on a quarterly cadence:
- Day 90: AI tool feedback request
- Day 180: Check-in message
- Day 270: What's new at Kale

Runs daily via GitHub Actions at 10 AM CT.
"""

import requests
import json
import time
import os
import re
import random
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
WINBACK_COUNT_COL = "numbers_mkygz1v"  # Track which message in sequence
FIRST_NAME_COL = "text_mkyfws0a"
PHONE_COL = "phone_mkyfkn1f"
DO_NOT_CONTACT_COL = "boolean_mkyg123"  # Skip if checked

# Spintax SMS Messages (rotates based on winback_count % 3)
SMS_MESSAGES = [
    # Message 1 - Day 90: AI Tool Feedback
    """{Hey|Hi} {first_name} - {hope all is well|hope you're doing great|how's it going}! I just launched this listing description AI tool and would love your feedback. It researches your neighborhood and rewrites listings to get more showings.

Try it free: listing.joinkale.com

{Let me know what you think|Would love your thoughts|Curious what you think}? {No strings - just want honest feedback|Just looking for honest feedback} from someone who knows their stuff.

- DJ""",

    # Message 2 - Day 180: Check-In
    """{Hey|Hi} {first_name} - just wanted to {check in|reach out|say hi}. {Miss having you around|Been thinking about the old crew|Hope the new gig is treating you well}. {If things ever change|If you ever want to chat|If you're ever curious about what's new}, {my door's always open|you know where to find me|just reach out}.

- DJ""",

    # Message 3 - Day 270: What's New
    """{Hey|Hi} {first_name} - {it's been a while|long time no talk|hope you're killing it out there}. {We've been making some changes here at Kale|Lot of new stuff happening at Kale|Things are evolving here} and {I thought of you|wanted to let you know|figured you might be curious}. {Let me know if you ever want to catch up|Would love to chat sometime|Reach out if you want to hear about it}.

- DJ"""
]


def process_spintax(text):
    """Process spintax text, randomly selecting from {option1|option2|option3} patterns."""
    pattern = r'\{([^{}]+)\}'

    def replace_match(match):
        options = match.group(1).split('|')
        return random.choice(options)

    # Keep processing until no more spintax patterns
    while re.search(pattern, text):
        text = re.sub(pattern, replace_match, text)

    return text

def monday_query(query):
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json",
        "API-Version": "2024-10"
    }
    response = requests.post(MONDAY_API_URL, headers=headers, json={"query": query})
    return response.json().get("data")

def get_todays_winbacks():
    """Get former agents where Win-Back Date = today and Do Not Contact = false."""
    today = date.today().isoformat()

    query = """
    query {
        boards(ids: [%s]) {
            items_page(limit: 500) {
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
        do_not_contact = cols.get(DO_NOT_CONTACT_COL, {}).get("text", "")

        # Skip if Do Not Contact is checked
        if do_not_contact == "true":
            continue

        if winback_date == today:
            first_name = cols.get(FIRST_NAME_COL, {}).get("text", "")
            phone_data = cols.get(PHONE_COL, {}).get("value", "{}")
            phone = json.loads(phone_data).get("phone", "") if phone_data else ""

            # Get winback count for message rotation (default to 0)
            winback_count_text = cols.get(WINBACK_COUNT_COL, {}).get("text", "0")
            try:
                winback_count = int(winback_count_text) if winback_count_text else 0
            except ValueError:
                winback_count = 0

            if phone and first_name:
                ready_items.append({
                    "id": item["id"],
                    "name": item["name"],
                    "first_name": first_name,
                    "phone": phone,
                    "winback_count": winback_count
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

def update_winback_status(item_id, new_count):
    """Update winback count and set next winback date (90 days from now)."""
    from datetime import timedelta

    next_date = (date.today() + timedelta(days=90)).isoformat()

    # Update winback count and next winback date
    query = """
    mutation {
        change_multiple_column_values(
            board_id: %s,
            item_id: %s,
            column_values: "{\\"numbers_mkygz1v\\": %d, \\"date_mkygkfv\\": {\\"date\\": \\"%s\\"}}"
        ) {
            id
        }
    }
    """ % (FORMER_AGENTS_BOARD_ID, item_id, new_count, next_date)

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
    print("Win-Back SMS Script (Spintax Quarterly Drip)")
    print(f"Date: {date.today().isoformat()}")
    print("=" * 60)

    items = get_todays_winbacks()
    print(f"Found {len(items)} agents ready for win-back SMS")

    stats = {"sent": 0, "failed": 0}

    for item in items:
        # Select message based on winback count (rotates through 3 messages)
        message_index = item["winback_count"] % 3
        message_template = SMS_MESSAGES[message_index]

        # Replace {first_name} placeholder then process spintax
        message_with_name = message_template.replace("{first_name}", item["first_name"])
        final_message = process_spintax(message_with_name)

        print(f"  Sending to {item['name']} (msg #{item['winback_count'] + 1})...", end=" ")

        if send_sms(item["phone"], final_message):
            new_count = item["winback_count"] + 1
            update_winback_status(item["id"], new_count)
            create_update(item["id"],
                f"Win-back SMS #{new_count} sent via JustCall.\\n\\n"
                f"Message: {final_message[:100]}...")
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
