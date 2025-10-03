#!/usr/bin/env python3
#main.py

import gi
import sys
from pathlib import Path
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ui import MainUI
from objects.ImageItem import ImageItem

class PicaxeApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="com.example.crunchy", **kwargs)
        self.connect('activate', self.on_activate)
        self.win = None
        self.image_items = []  # Store ImageItem objects
        self.history_dir = Path.home() / ".picaxe-history"
        self._setup_history_directory()

    def on_activate(self, app):
        self.win = Adw.ApplicationWindow(application=app)
        self.win.set_title("Picaxe")
        self.win.set_default_size(650, 500)

        main_view = Adw.ToolbarView()
        header = Adw.HeaderBar()
        main_view.add_css_class("flat")
        main_view.add_top_bar(header)

        self.content = MainUI(
            on_browse_button_click=self._on_browse_files,
            on_drop_files=self._on_drop_files
        )
        # Store reference to sync deletions
        self.content.parent_app = self
        main_view.set_content(self.content)
        
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
                print("Selected files:")
                new_items = []
                for file in files:
                    path = Path(file.get_path())
                    try:
                        image_item = ImageItem(path)
                        self.image_items.append(image_item)
                        new_items.append(image_item)
                        print(f"Created ImageItem: {image_item}")
                    except Exception as img_error:
                        print(f"Error creating ImageItem for {path}: {img_error}")
                
                # Update UI with new items
                if new_items:
                    self.content.add_image_items(new_items)
        except Exception as e:
            print(f"File selection cancelled or failed: {e}")

    def _on_drop_files(self, files):
        """Called when files are dropped onto the UI."""
        print("Files dropped:")
        new_items = []
        for file in files:
            path = Path(file.get_path())
            try:
                # Only process image files
                if path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                    image_item = ImageItem(path)
                    self.image_items.append(image_item)
                    new_items.append(image_item)
                    print(f"Created ImageItem: {image_item}")
                else:
                    print(f"Skipped non-image file: {path}")
            except Exception as img_error:
                print(f"Error creating ImageItem for {path}: {img_error}")
        
        # Update UI with new items
        if new_items:
            self.content.add_image_items(new_items)


    def _setup_history_directory(self):
        """Create the .picaxe-history directory if it doesn't exist."""
        try:
            self.history_dir.mkdir(exist_ok=True)
            print(f"History directory ready at: {self.history_dir}")
        except Exception as e:
            print(f"Warning: Could not create history directory: {e}")
    
    def _save_history(self):
        """Save current session to history (placeholder for future implementation)."""
        # TODO: Implement serialization of image_items to JSON
        pass


if __name__ == "__main__":
    app = PicaxeApp()
    app.run(sys.argv)