#!/usr/bin/env python3
"""
Setup script to create Email Win-Back Date column on Monday.com
Run once to create the column, then update send-winback-sms.py with the returned column ID.

Usage: MONDAY_API_KEY=your_key python3 scripts/setup-email-winback-column.py
"""

import requests
import os
import json

MONDAY_API_KEY = os.environ.get("MONDAY_API_KEY")
MONDAY_API_URL = "https://api.monday.com/v2"
FORMER_AGENTS_BOARD_ID = "18391489234"

def monday_query(query):
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json",
        "API-Version": "2024-10"
    }
    response = requests.post(MONDAY_API_URL, headers=headers, json={"query": query})
    return response.json()

def main():
    if not MONDAY_API_KEY:
        print("ERROR: Set MONDAY_API_KEY environment variable")
        return

    print("=" * 60)
    print("Email Win-Back Column Setup")
    print("=" * 60)

    # First, check existing columns
    print("\n1. Checking existing columns...")
    query = """
    query {
        boards(ids: [%s]) {
            columns {
                id
                title
                type
            }
        }
    }
    """ % FORMER_AGENTS_BOARD_ID

    result = monday_query(query)
    columns = result.get("data", {}).get("boards", [{}])[0].get("columns", [])

    # Check if Email Win-Back Date already exists
    email_col = None
    for col in columns:
        if "email" in col["title"].lower() and "win" in col["title"].lower():
            email_col = col
            break

    if email_col:
        print(f"   Found existing column: {email_col['title']}")
        print(f"   Column ID: {email_col['id']}")
        print(f"\n   UPDATE send-winback-sms.py line 31:")
        print(f'   EMAIL_WINBACK_DATE_COL = "{email_col["id"]}"')
        return

    # Create the column
    print("\n2. Creating 'Email Win-Back Date' column...")
    create_query = """
    mutation {
        create_column(
            board_id: %s,
            title: "Email Win-Back Date",
            column_type: date
        ) {
            id
            title
        }
    }
    """ % FORMER_AGENTS_BOARD_ID

    result = monday_query(create_query)

    if "errors" in result:
        print(f"   ERROR: {result['errors']}")
        return

    new_col = result.get("data", {}).get("create_column", {})
    print(f"   Created column: {new_col.get('title')}")
    print(f"   Column ID: {new_col.get('id')}")

    print(f"\n" + "=" * 60)
    print("SUCCESS! Now update send-winback-sms.py line 31:")
    print(f'EMAIL_WINBACK_DATE_COL = "{new_col.get("id")}"')
    print("=" * 60)

if __name__ == "__main__":
    main()
