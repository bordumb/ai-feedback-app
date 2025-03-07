#!/usr/bin/env python3

import os
import sys

IGNORED_DIRS = {
    ".git", ".next", "node_modules", "dist", "build", "coverage", "__pycache__"
}

IGNORED_EXTENSIONS = {
    ".map", ".d.ts", ".d.ts.map", ".pyc", ".DS_Store"
}

def should_ignore(name: str, path: str) -> bool:
    """
    Returns True if name/path should be ignored based on
    the predefined ignored directories and file extensions.
    """
    # Ignore hidden directories/files (e.g., .git, .env) unless specifically excluded
    if name.startswith(".") and name not in {".env"}:
        return True

    # Check if it's in the ignored dirs set
    if name in IGNORED_DIRS:
        return True

    # Check file extension
    _, ext = os.path.splitext(name)
    if ext.lower() in IGNORED_EXTENSIONS:
        return True

    return False

def print_directory_tree(start_path: str, prefix: str = "") -> None:
    """
    Recursively prints the folder/file structure under start_path,
    ignoring certain directories/files.
    """
    # Gather contents
    with os.scandir(start_path) as it:
        entries = sorted(it, key=lambda e: (not e.is_dir(), e.name.lower()))
    
    # Print directories first, then files
    for entry in entries:
        if should_ignore(entry.name, entry.path):
            continue

        # Mark directories
        if entry.is_dir():
            print(f"{prefix}{entry.name}/")
            print_directory_tree(entry.path, prefix + "  ")
        else:
            print(f"{prefix}{entry.name}")

if __name__ == "__main__":
    # Use current directory by default unless a path argument is supplied
    start_path = sys.argv[1] if len(sys.argv) > 1 else "."
    print_directory_tree(start_path)
