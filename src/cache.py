from __future__ import annotations

# New cache utility for storing scraped Hacker News posts
# Provides helper functions to read and write a JSON cache so that already
# scraped posts are not scraped again on subsequent runs.

import json
import os
from pathlib import Path
from typing import Dict, List

# Cache file lives in the project root (one directory above `src`).
_CACHE_FILE = Path(__file__).resolve().parent.parent / "posts_cache.json"


def _ensure_cache_file_exists() -> None:
    """Create an empty cache file if it does not yet exist."""
    if not _CACHE_FILE.exists():
        # Ensure parent directory exists (should, but be safe)
        _CACHE_FILE.touch()
        _CACHE_FILE.write_text("[]", encoding="utf-8")


def load_posts() -> List[Dict[str, str]]:
    """Load cached posts from the JSON file.

    Returns an empty list if the file does not exist or cannot be decoded.
    Each post is stored as a dictionary with at least the keys: ``title``,
    ``href``, and ``content``.
    """
    if not _CACHE_FILE.exists():
        return []

    try:
        with _CACHE_FILE.open("r", encoding="utf-8") as fh:
            return json.load(fh)  # type: ignore[return-value]
    except (json.JSONDecodeError, OSError):
        # If the file is corrupted or unreadable, reset it.
        return []


def save_posts(posts: List[Dict[str, str]]) -> None:
    """Overwrite the cache with the provided list of ``posts``.

    Args:
        posts: List of post dictionaries to persist.
    """
    # Make sure the directory/file exists before writing
    _ensure_cache_file_exists()

    with _CACHE_FILE.open("w", encoding="utf-8") as fh:
        json.dump(posts, fh, ensure_ascii=False, indent=2)


def post_exists(href: str) -> bool:
    """Return ``True`` if a post with *href* already exists in the cache."""
    cached_hrefs = {p.get("href") for p in load_posts()}
    return href in cached_hrefs
