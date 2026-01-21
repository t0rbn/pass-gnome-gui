"""Main application window."""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw

from password_store import PasswordStore
from password_card import PasswordCard


class PassGnomeWindow(Adw.ApplicationWindow):
    """Main application window."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.store = PasswordStore()
        self.current_folder = ''

        self.set_title('Pass Password Manager')
        self.set_default_size(900, 600)

        # Paned container for two panels (each with its own header bar)
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_shrink_start_child(False)
        paned.set_shrink_end_child(False)
        self.set_content(paned)

        # Left panel - Folder tree with header bar
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        left_box.add_css_class('view')

        # Left header bar
        left_header = Adw.HeaderBar()
        left_header.set_show_end_title_buttons(False)
        left_header.set_title_widget(Gtk.Label(label='Folders'))
        left_box.append(left_header)

        # Folder tree scroll
        left_scroll = Gtk.ScrolledWindow()
        left_scroll.set_min_content_width(200)
        left_scroll.set_vexpand(True)
        left_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.folder_tree = Gtk.TreeView()
        self.folder_tree.set_headers_visible(False)
        self.folder_tree.connect('cursor-changed', self.on_folder_selected)

        # Create tree store: name, full_path
        self.tree_store = Gtk.TreeStore(str, str)
        self.folder_tree.set_model(self.tree_store)

        # Column for folder names
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Folder', renderer, text=0)
        self.folder_tree.append_column(column)

        left_scroll.set_child(self.folder_tree)
        left_box.append(left_scroll)
        paned.set_start_child(left_box)

        # Right panel - Password list with header bar
        right_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        right_box.set_hexpand(True)

        # Right header bar with folder title
        right_header = Adw.HeaderBar()
        right_header.set_show_start_title_buttons(False)
        self.folder_title = Adw.WindowTitle(title='Passwords', subtitle='Select a folder')
        right_header.set_title_widget(self.folder_title)
        right_box.append(right_header)

        right_scroll = Gtk.ScrolledWindow()
        right_scroll.set_vexpand(True)
        right_scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        self.password_list = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.password_list.set_margin_top(6)
        self.password_list.set_margin_bottom(12)

        right_scroll.set_child(self.password_list)
        right_box.append(right_scroll)

        paned.set_end_child(right_box)
        paned.set_position(250)

        # Populate folder tree
        self.populate_folder_tree()

    def populate_folder_tree(self):
        """Populate the folder tree view."""
        self.tree_store.clear()

        # Add root entry
        root_iter = self.tree_store.append(None, ['Password Store', ''])

        # Build tree recursively
        self._add_folders_to_tree(self.store.store_path, root_iter, '')

        # Expand root
        root_path = self.tree_store.get_path(root_iter)
        self.folder_tree.expand_row(root_path, False)

    def _add_folders_to_tree(self, path, parent_iter, rel_path):
        """Recursively add folders to the tree store."""
        if not path.exists():
            return

        folders = []
        for item in path.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                folders.append(item)

        for folder in sorted(folders, key=lambda f: f.name.lower()):
            folder_rel_path = f"{rel_path}/{folder.name}" if rel_path else folder.name
            iter = self.tree_store.append(parent_iter, [folder.name, folder_rel_path])
            self._add_folders_to_tree(folder, iter, folder_rel_path)

    def on_folder_selected(self, tree_view):
        """Handle folder selection."""
        selection = tree_view.get_selection()
        model, tree_iter = selection.get_selected()

        if tree_iter is not None:
            folder_path = model.get_value(tree_iter, 1)
            self.current_folder = folder_path
            self.update_password_list()

    def update_password_list(self):
        """Update the password list for the current folder."""
        # Clear existing entries
        while True:
            child = self.password_list.get_first_child()
            if child is None:
                break
            self.password_list.remove(child)

        # Update header bar title
        if self.current_folder:
            self.folder_title.set_title(self.current_folder.split('/')[-1])
            self.folder_title.set_subtitle(self.current_folder)
        else:
            self.folder_title.set_title('Password Store')
            self.folder_title.set_subtitle('Root folder')

        # Add password entries
        entries = self.store.get_entries_in_folder(self.current_folder)

        if not entries:
            empty_label = Gtk.Label(label='No passwords in this folder')
            empty_label.add_css_class('dim-label')
            empty_label.set_margin_top(24)
            self.password_list.append(empty_label)
        else:
            for entry in entries:
                card = PasswordCard(self.store, self.current_folder, entry)
                self.password_list.append(card)
