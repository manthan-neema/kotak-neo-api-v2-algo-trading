import json
from pathlib import Path
from typing import Optional, Dict, Any

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "session.json"


def save_session(session: Dict[str, Any]) -> None:
    """
    Save session data atomically to disk.
    """
    tmp_file = SESSION_FILE.with_suffix(".tmp")

    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(session, f, indent=2)

    tmp_file.replace(SESSION_FILE)


def load_session() -> Optional[Dict[str, Any]]:
    """
    Load session from disk if it exists and is valid JSON.
    """
    if not SESSION_FILE.exists():
        return None

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # Corrupted session file
        return None
    except OSError:
        # Permission / IO issue
        return None


def is_session_valid(client) -> bool:
    """
    Validate session by making a lightweight authenticated API call.
    """
    try:
        response = client.positions()

        # Adjust this check based on actual API response
        if not isinstance(response, dict):
            return False

        return response.get("status") == 200

    except Exception:
        return False
