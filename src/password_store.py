"""Interface to the pass password store."""

import os
import subprocess
import threading
from pathlib import Path

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import GLib


class PasswordStore:
    """Interface to the pass password store."""

    def __init__(self):
        self.store_path = Path(os.environ.get('PASSWORD_STORE_DIR',
                                               Path.home() / '.password-store'))

    def get_folder_tree(self):
        """Returns a nested dict representing the folder structure."""
        tree = {}
        if not self.store_path.exists():
            return tree

        for root, dirs, files in os.walk(self.store_path):
            # Skip .git directory
            dirs[:] = [d for d in dirs if not d.startswith('.')]

            rel_path = Path(root).relative_to(self.store_path)

            # Get the current node in our tree
            current = tree
            if str(rel_path) != '.':
                for part in rel_path.parts:
                    if part not in current:
                        current[part] = {}
                    current = current[part]

        return tree

    def get_entries_in_folder(self, folder_path):
        """Returns list of password entries (without .gpg extension) in a folder."""
        if folder_path == '':
            full_path = self.store_path
        else:
            full_path = self.store_path / folder_path

        entries = []
        if full_path.exists():
            for item in full_path.iterdir():
                if item.is_file() and item.suffix == '.gpg':
                    entries.append(item.stem)

        return sorted(entries)

    def get_password(self, entry_path, callback=None):
        """Retrieve password for an entry using pass command (runs in background thread)."""
        def _get():
            try:
                result = subprocess.run(
                    ['pass', 'show', entry_path],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    password = result.stdout.split('\n')[0]
                    if callback:
                        GLib.idle_add(callback, password)
                    return password
                if callback:
                    GLib.idle_add(callback, None)
                return None
            except (subprocess.TimeoutExpired, FileNotFoundError):
                if callback:
                    GLib.idle_add(callback, None)
                return None

        thread = threading.Thread(target=_get, daemon=True)
        thread.start()

    def copy_to_clipboard(self, entry_path, callback=None):
        """Copy password to clipboard using pass -c (runs in background thread)."""
        def _copy():
            try:
                subprocess.run(
                    ['pass', '-c', entry_path],
                    capture_output=True,
                    timeout=30
                )
                if callback:
                    GLib.idle_add(callback, True)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                if callback:
                    GLib.idle_add(callback, False)

        thread = threading.Thread(target=_copy, daemon=True)
        thread.start()
