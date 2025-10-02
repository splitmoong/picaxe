#ui.py

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from components.buttons.button import RoundedButton




class MainUI(Gtk.Box):
    def __init__(self):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Create a button
        # Create an instance of our custom button
        browseFilesButton = RoundedButton(
            label="Browse Files",
            width=150,
            height=55
        )

        # Add the button to the box
        self.append(browseFilesButton)

    