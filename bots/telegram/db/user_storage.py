import os
import json
from core.config import BASE_DIR
from datetime import datetime, timezone

# Create the database directory in the root directory if it doesn't exist
base_dir = BASE_DIR
DATABASE_DIR = base_dir / "database" / "telegram" / "users.json"

# If the data file doesn't exist, create it
if not os.path.exists(DATABASE_DIR):
    os.makedirs(os.path.dirname(DATABASE_DIR), exist_ok=True)
    with open(DATABASE_DIR, "w", encoding="utf-8") as f:
        json.dump({}, f)


def load_users() -> dict:
    """
    Loads all user data from the users.json file.

    Returns:
        dict: A dictionary where keys are user IDs (as strings) and values are user info.
    """
    with open(DATABASE_DIR, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    """
    Saves the given user dictionary into the users.json file.

    Args:
        users (dict): A dictionary of users to be saved.
    """
    with open(DATABASE_DIR, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def upsert_user(user_id, username, first_name, last_name):
    """
    Adds or updates a user in the users.json file.

    Args:
        user_id (int): Telegram user ID.
        username (str): Telegram username.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
    """
    users = load_users()
    user_id_str = str(user_id)
    # Get the current time in UTC and ISO format
    now = datetime.now(timezone.utc).isoformat()

    if user_id_str not in users:
        users[user_id_str] = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "created_at": now,
            "updated_at": now,
        }
    else:
        users[user_id_str].update(
            {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
                "updated_at": now,
            }
        )

    save_users(users)


def get_total_users() -> int:
    """
    Returns the total number of unique users stored.

    Returns:
        int: The number of users in the system.
    """
    users = load_users()
    return len(users)
