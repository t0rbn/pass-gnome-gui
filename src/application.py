"""Main application class."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw, Gio

from window import PassGnomeWindow


class PassGnomeApp(Adw.Application):
    """Main application class."""

    def __init__(self):
        super().__init__(
            application_id='org.gnome.PassGui',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )

    def do_activate(self):
        """Called when the application is activated."""
        win = self.props.active_window
        if not win:
            win = PassGnomeWindow(application=self)
        win.present()
