#!/usr/bin/env python3
#main.py

import gi
import sys

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ui import MainUI

class PicaxeApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="com.example.crunchy", **kwargs)
        self.connect('activate', self.on_activate)
        self.win = None

    def on_activate(self, app):
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_title("Picaxe")
        self.win.set_default_size(500, 600)

        main_view = Adw.ToolbarView()
        header = Adw.HeaderBar()
        main_view.add_css_class("flat")
        main_view.add_top_bar(header)

        content = MainUI(on_browse_button_click=self._on_browse_files)
        main_view.set_content(content)
        
        self.win.set_content(main_view)
        self.win.present()

    def _on_browse_files(self, button):
        """Called when the 'Browse Files' button is clicked."""
        dialog = Gtk.FileDialog(title="Select Images", modal=True)
        
        img_filter = Gtk.FileFilter()
        img_filter.set_name("Image Files")
        img_filter.add_mime_type("image/png")
        img_filter.add_mime_type("image/jpeg")
        img_filter.add_mime_type("image/webp")
        dialog.set_default_filter(img_filter)
        
        # CHANGED: Replaced set_select_multiple and .open with a single call
        # to the method for selecting multiple files.
        dialog.open_multiple(self.win, None, self._on_files_selected)

    def _on_files_selected(self, dialog, result):
        """Callback that runs after the user selects files or cancels."""
        try:
            # CHANGED: Use the corresponding "_finish" method for multiple files.
            files = dialog.open_multiple_finish(result)
            if files:
                file_paths = [f.get_path() for f in files]
                print("Selected files:")
                for path in file_paths:
                    print(f"- {path}")
        except Exception as e:
            print(f"File selection cancelled or failed: {e}")


if __name__ == "__main__":
    app = PicaxeApp()
    app.run(sys.argv)