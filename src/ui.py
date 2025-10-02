#ui.py

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from components.buttons.button import RoundedButton

class MainUI(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_hexpand(True)
        self.set_vexpand(True)

        # Spacer to take all the vertical space above
        spacer = Gtk.Box()
        spacer.set_vexpand(True)

        # Create the custom button
        browseFilesButton = RoundedButton(
            label="Browse Files",
            width=150,
            height=55
        )
        browseFilesButton.set_halign(Gtk.Align.CENTER)   # center horizontally
        browseFilesButton.set_valign(Gtk.Align.END)      # stick to bottom
        browseFilesButton.set_margin_bottom(40)          # padding at bottom

        # Pack spacer first, then button
        self.append(spacer)
        self.append(browseFilesButton)

    