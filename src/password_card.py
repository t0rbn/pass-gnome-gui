"""Card widget for displaying a password entry."""

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk


class PasswordCard(Gtk.Box):
    """A card displaying a password entry."""

    def __init__(self, store, folder_path, entry_name):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.store = store
        self.folder_path = folder_path
        self.entry_name = entry_name
        self.entry_path = f"{folder_path}/{entry_name}" if folder_path else entry_name
        self.password = None
        self.unmasked = False

        self.add_css_class('card')
        self.set_margin_start(12)
        self.set_margin_end(12)
        self.set_margin_top(6)
        self.set_margin_bottom(6)

        # Inner padding
        inner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        inner_box.set_margin_start(16)
        inner_box.set_margin_end(16)
        inner_box.set_margin_top(16)
        inner_box.set_margin_bottom(16)
        self.append(inner_box)

        # Username label (title)
        username_label = Gtk.Label(label=entry_name)
        username_label.set_xalign(0)
        username_label.add_css_class('title-3')
        inner_box.append(username_label)

        # Password row
        password_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        inner_box.append(password_row)

        # Password field (masked)
        self.password_entry = Gtk.Entry()
        self.password_entry.set_text('••••••••')
        self.password_entry.set_editable(False)
        self.password_entry.set_can_focus(False)
        self.password_entry.set_hexpand(True)
        password_row.append(self.password_entry)

        # Unmask button
        self.unmask_button = Gtk.Button()
        self.unmask_button.set_icon_name('view-reveal-symbolic')
        self.unmask_button.set_tooltip_text('Show/Hide password')
        self.unmask_button.connect('clicked', self.on_unmask_clicked)
        password_row.append(self.unmask_button)

        # Copy button
        copy_button = Gtk.Button()
        copy_button.set_icon_name('edit-copy-symbolic')
        copy_button.set_tooltip_text('Copy password to clipboard')
        copy_button.connect('clicked', self.on_copy_clicked)
        password_row.append(copy_button)

    def on_unmask_clicked(self, button):
        """Toggle password visibility."""
        if not self.unmasked:
            # Fetch password if not already fetched
            if self.password is None:
                self.unmask_button.set_sensitive(False)
                self.password_entry.set_text('Loading...')
                self.store.get_password(self.entry_path, self._on_password_received)
            else:
                self._show_password()
        else:
            self._hide_password()

    def _on_password_received(self, password):
        """Callback when password is retrieved."""
        self.unmask_button.set_sensitive(True)
        self.password = password
        if password:
            self._show_password()
        else:
            self.password_entry.set_text('Error')

    def _show_password(self):
        """Show the unmasked password."""
        self.password_entry.set_text(self.password)
        self.unmask_button.set_icon_name('view-conceal-symbolic')
        self.unmasked = True

    def _hide_password(self):
        """Hide the password with mask."""
        self.password_entry.set_text('••••••••')
        self.unmask_button.set_icon_name('view-reveal-symbolic')
        self.unmasked = False

    def on_copy_clicked(self, button):
        """Copy password to clipboard."""
        self.store.copy_to_clipboard(self.entry_path)
