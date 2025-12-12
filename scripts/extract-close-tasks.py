#!/usr/bin/env python3
"""
Extract Future Tasks from Close CRM

Pulls all incomplete tasks from Close CRM for Ana, DJ, and Rea.
Saves to close_tasks_export.json for the push script.

Usage:
  python3 scripts/extract-close-tasks.py
"""

import requests
import json
import time
from datetime import datetime
from pathlib import Path

# API Configuration
CLOSE_API_KEY = "api_3U6OkyHlWF2pIcVusIZf2V.1uT08KKRosiYWBy8fH6B4L"
CLOSE_API_URL = "https://api.close.com/api/v1"

# Close User IDs
CLOSE_USERS = {
    "user_AP0Edi94oMcrN6LGAm9Gcy0ebFjy3F0bRonhocDFeO1": "DJ",
    "user_DBMZmo4TP2tILMtbDsIVQnSU9JJ0WM0YoXS9Ly7izlh": "Ana",  # Anaya
    "user_dDXNoNN8voWPjdLp6jxW27aSA96ezyIRHWvYE2yBaQq": "Rea",
}

# Files
SCRIPT_DIR = Path(__file__).parent
OUTPUT_FILE = SCRIPT_DIR / "close_tasks_export.json"
LOG_FILE = SCRIPT_DIR / "task_extract_log.txt"

def log(message):
    """Log message to file and console."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)
    with open(LOG_FILE, "a") as f:
        f.write(log_line + "\n")

def get_close_tasks():
    """Fetch all incomplete tasks from Close."""
    tasks = []
    has_more = True
    skip = 0
    limit = 100

    log("Fetching incomplete tasks from Close...")

    while has_more:
        url = f"{CLOSE_API_URL}/task/"
        params = {
            "is_complete": "false",
            "_skip": skip,
            "_limit": limit,
        }

        response = requests.get(
            url,
            params=params,
            auth=(CLOSE_API_KEY, "")
        )

        if response.status_code != 200:
            log(f"Error fetching tasks: {response.status_code} - {response.text}")
            break

        data = response.json()
        batch = data.get("data", [])
        tasks.extend(batch)

        log(f"  Fetched {len(batch)} tasks (total: {len(tasks)})")

        has_more = data.get("has_more", False)
        skip += limit
        time.sleep(0.5)  # Rate limiting

    return tasks

def filter_tasks_by_user(tasks):
    """Filter tasks to only include Ana, DJ, Rea's tasks."""
    filtered = []

    for task in tasks:
        assigned_to = task.get("assigned_to")
        if assigned_to in CLOSE_USERS:
            task["assigned_to_name"] = CLOSE_USERS[assigned_to]
            filtered.append(task)

    return filtered

def enrich_task_data(tasks):
    """Add useful fields to task data."""
    enriched = []

    for task in tasks:
        enriched_task = {
            "task_id": task.get("id"),
            "lead_id": task.get("lead_id"),
            "text": task.get("text", ""),
            "date": task.get("date"),
            "date_created": task.get("date_created"),
            "assigned_to": task.get("assigned_to"),
            "assigned_to_name": task.get("assigned_to_name"),
            "is_complete": task.get("is_complete", False),
            "_type": task.get("_type"),
            "object_type": task.get("object_type"),
            "object_id": task.get("object_id"),
        }
        enriched.append(enriched_task)

    return enriched

def main():
    log("=" * 60)
    log("CLOSE TASK EXTRACTION")
    log("=" * 60)

    # Fetch all incomplete tasks
    all_tasks = get_close_tasks()
    log(f"Total incomplete tasks in Close: {len(all_tasks)}")

    # Filter to Ana, DJ, Rea
    filtered_tasks = filter_tasks_by_user(all_tasks)
    log(f"Tasks assigned to Ana/DJ/Rea: {len(filtered_tasks)}")

    # Enrich data
    enriched_tasks = enrich_task_data(filtered_tasks)

    # Count by user
    by_user = {}
    for task in enriched_tasks:
        name = task.get("assigned_to_name", "Unknown")
        by_user[name] = by_user.get(name, 0) + 1

    log("Tasks by user:")
    for name, count in sorted(by_user.items()):
        log(f"  {name}: {count}")

    # Count tasks with dates
    with_dates = len([t for t in enriched_tasks if t.get("date")])
    log(f"Tasks with due dates: {with_dates}")

    # Save to file
    with open(OUTPUT_FILE, "w") as f:
        json.dump(enriched_tasks, f, indent=2)

    log(f"Saved {len(enriched_tasks)} tasks to {OUTPUT_FILE}")
    log("=" * 60)
    log("EXTRACTION COMPLETE")
    log("=" * 60)

if __name__ == "__main__":
    main()
