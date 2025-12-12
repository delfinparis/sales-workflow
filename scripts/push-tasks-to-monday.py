#!/usr/bin/env python3
"""
Push Tasks to Monday.com

Reads tasks from close_tasks_export.json, matches them to Monday items
by Close ID, and updates the Next Action Date and Next Action fields.

Usage:
  python3 scripts/push-tasks-to-monday.py              # Run push
  DRY_RUN=true python3 scripts/push-tasks-to-monday.py # Preview only
"""

import requests
import json
import time
import os
from datetime import datetime
from pathlib import Path

# API Configuration
MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMzMDE5NDQxNywiYWFpIjoxMSwidWlkIjoxMDk5MzEwNywiaWFkIjoiMjAyNC0wMy0wN1QyMTo1MDoxMi4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NDk2MDA1OSwicmduIjoidXNlMSJ9.m3bCdQF0HwlTYrLQy4-fbTtv04A8RPxzTsWeTsGHFfI"
MONDAY_API_URL = "https://api.monday.com/v2"

# Monday Board IDs
SUPERLATIVE_BOARD = "18390370563"
NEWLY_LICENSED_BOARD = "18391158354"
CLOSED_LEADS_BOARD = "18391860337"

# Column IDs for each board
BOARD_CONFIG = {
    SUPERLATIVE_BOARD: {
        "name": "Superlative",
        "close_id_col": "text_mkyhaqf0",
        "next_action_date_col": "date_mky6h6ny",
        "next_action_col": "text_mky64dyz",
        "notes_col": "long_text_mky6bj1v",
    },
    NEWLY_LICENSED_BOARD: {
        "name": "Newly Licensed",
        "close_id_col": "text_mkyb1a5v",
        "next_action_date_col": "date_mkyb0w7t",  # May need to verify
        "next_action_col": "text_mkyb1kcf",  # May need to verify
        "notes_col": "long_text_mkybev5j",
    },
    CLOSED_LEADS_BOARD: {
        "name": "Closed Leads",
        "close_id_col": "text_mkyhbyr2",
        "next_action_date_col": "date_mkyhcgd3",  # May need to verify
        "next_action_col": "text_mkyhd7x9",  # May need to verify
        "notes_col": "long_text_mkyhm5hy",
    },
}

# Mode
DRY_RUN = os.environ.get("DRY_RUN", "false").lower() == "true"

# Files
SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = SCRIPT_DIR / "close_tasks_export.json"
PROGRESS_FILE = SCRIPT_DIR / "task_push_progress.json"
LOG_FILE = SCRIPT_DIR / "task_push_log.txt"

# Stats
stats = {
    "matched": 0,
    "updated": 0,
    "not_found": 0,
    "errors": 0,
    "skipped_no_lead": 0,
}

# Cache for Monday items by Close ID
monday_items_cache = {}

def log(message):
    """Log message to file and console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

def monday_query(query, variables=None):
    """Execute a Monday.com GraphQL query."""
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    response = requests.post(MONDAY_API_URL, headers=headers, json=payload)
    time.sleep(0.3)  # Rate limiting

    if response.status_code != 200:
        raise Exception(f"Monday API error: {response.status_code} - {response.text}")

    data = response.json()
    if "errors" in data:
        raise Exception(f"Monday GraphQL error: {data['errors']}")

    return data

def build_monday_cache():
    """Build a cache of Monday items by Close ID across all boards."""
    global monday_items_cache

    log("Building Monday items cache...")

    for board_id, config in BOARD_CONFIG.items():
        board_name = config["name"]
        close_id_col = config["close_id_col"]

        log(f"  Fetching items from {board_name} board...")

        cursor = None
        items_fetched = 0

        while True:
            if cursor:
                query = f'''
                query {{
                    next_items_page(cursor: "{cursor}", limit: 500) {{
                        cursor
                        items {{
                            id
                            name
                            column_values(ids: ["{close_id_col}"]) {{
                                id
                                text
                            }}
                        }}
                    }}
                }}
                '''
            else:
                query = f'''
                query {{
                    boards(ids: [{board_id}]) {{
                        items_page(limit: 500) {{
                            cursor
                            items {{
                                id
                                name
                                column_values(ids: ["{close_id_col}"]) {{
                                    id
                                    text
                                }}
                            }}
                        }}
                    }}
                }}
                '''

            try:
                result = monday_query(query)

                if cursor:
                    page_data = result.get("data", {}).get("next_items_page", {})
                else:
                    boards = result.get("data", {}).get("boards", [])
                    page_data = boards[0].get("items_page", {}) if boards else {}

                items = page_data.get("items", [])
                cursor = page_data.get("cursor")

                for item in items:
                    close_id = None
                    for col in item.get("column_values", []):
                        if col.get("id") == close_id_col:
                            close_id = col.get("text")
                            break

                    if close_id:
                        monday_items_cache[close_id] = {
                            "item_id": item["id"],
                            "name": item["name"],
                            "board_id": board_id,
                            "board_name": board_name,
                        }

                items_fetched += len(items)

                if not cursor or not items:
                    break

            except Exception as e:
                log(f"    Error fetching from {board_name}: {e}")
                break

        log(f"    Fetched {items_fetched} items from {board_name}")

    log(f"Total cached items with Close ID: {len(monday_items_cache)}")

def update_monday_item(item_id, board_id, task):
    """Update a Monday item with task data."""
    config = BOARD_CONFIG[board_id]

    # Build column values
    column_values = {}

    # Next Action Date
    if task.get("date"):
        # Format: YYYY-MM-DD
        date_str = task["date"][:10] if len(task.get("date", "")) >= 10 else task.get("date")
        column_values[config["next_action_date_col"]] = {"date": date_str}

    # Next Action (task text)
    if task.get("text"):
        column_values[config["next_action_col"]] = task["text"][:255]  # Truncate if too long

    if not column_values:
        return False

    # Build mutation
    column_values_json = json.dumps(column_values).replace('"', '\\"')

    mutation = f'''
    mutation {{
        change_multiple_column_values(
            board_id: {board_id}
            item_id: {item_id}
            column_values: "{column_values_json}"
        ) {{
            id
        }}
    }}
    '''

    if DRY_RUN:
        log(f"    [DRY RUN] Would update item {item_id} with: {column_values}")
        return True

    try:
        monday_query(mutation)
        return True
    except Exception as e:
        log(f"    Error updating item {item_id}: {e}")
        return False

def load_progress():
    """Load progress from file."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {"processed_task_ids": []}

def save_progress(progress):
    """Save progress to file."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def main():
    log("=" * 60)
    log("PUSH TASKS TO MONDAY")
    log("=" * 60)

    if DRY_RUN:
        log("*** DRY RUN MODE - No changes will be made ***")

    # Load tasks
    if not INPUT_FILE.exists():
        log(f"Error: {INPUT_FILE} not found. Run extract-close-tasks.py first.")
        return

    with open(INPUT_FILE, "r") as f:
        tasks = json.load(f)

    log(f"Loaded {len(tasks)} tasks from {INPUT_FILE}")

    # Load progress
    progress = load_progress()
    processed_ids = set(progress.get("processed_task_ids", []))
    log(f"Already processed: {len(processed_ids)} tasks")

    # Build Monday cache
    build_monday_cache()

    # Process tasks
    log("\nProcessing tasks...")

    tasks_to_process = [t for t in tasks if t.get("task_id") not in processed_ids]
    log(f"Tasks to process: {len(tasks_to_process)}")

    for i, task in enumerate(tasks_to_process):
        task_id = task.get("task_id")
        lead_id = task.get("lead_id")
        task_text = task.get("text", "")[:50]
        assigned_to = task.get("assigned_to_name", "Unknown")

        if not lead_id:
            stats["skipped_no_lead"] += 1
            processed_ids.add(task_id)
            continue

        # Find Monday item by Close lead ID
        monday_item = monday_items_cache.get(lead_id)

        if not monday_item:
            stats["not_found"] += 1
            log(f"  [{i+1}/{len(tasks_to_process)}] No Monday match for lead {lead_id} - {task_text}...")
            processed_ids.add(task_id)
            continue

        stats["matched"] += 1
        item_id = monday_item["item_id"]
        board_id = monday_item["board_id"]
        board_name = monday_item["board_name"]

        log(f"  [{i+1}/{len(tasks_to_process)}] {assigned_to}: {task_text}... -> {board_name}")

        # Update Monday item
        if update_monday_item(item_id, board_id, task):
            stats["updated"] += 1
        else:
            stats["errors"] += 1

        processed_ids.add(task_id)

        # Save progress every 50 tasks
        if (i + 1) % 50 == 0:
            progress["processed_task_ids"] = list(processed_ids)
            save_progress(progress)
            log(f"  Progress saved ({len(processed_ids)} processed)")

    # Final save
    progress["processed_task_ids"] = list(processed_ids)
    save_progress(progress)

    # Summary
    log("\n" + "=" * 60)
    log("SUMMARY")
    log("=" * 60)
    log(f"Tasks processed: {len(tasks_to_process)}")
    log(f"  Matched to Monday: {stats['matched']}")
    log(f"  Updated successfully: {stats['updated']}")
    log(f"  Not found in Monday: {stats['not_found']}")
    log(f"  Errors: {stats['errors']}")
    log(f"  Skipped (no lead ID): {stats['skipped_no_lead']}")
    log("=" * 60)

if __name__ == "__main__":
    main()
