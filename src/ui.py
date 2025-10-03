import gi
from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Adw

from components.buttons.button import RoundedButton

# This creates robust paths to your assets
APP_DIR = Path(__file__).resolve().parent.parent
# UPDATED: Correct path for the new light mode image
LIGHT_ICON_PATH = APP_DIR / "assets" / "pictures" / "drag_and_drop_visual_dark.png"
DARK_ICON_PATH = APP_DIR / "assets" / "pictures" / "drag_and_drop_visual_dark.png"


class MainUI(Gtk.Box):
    # UPDATED: Added on_browse_button_click to accept the action from main.py
    def __init__(self, on_browse_button_click=None):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5
        )

        # 1. Configure the Image widget for expansion
        self.drop_image = Gtk.Image()
        self.drop_image.add_css_class("picaxe-drop-zone")
        self.drop_image.set_vexpand(True)
        self.drop_image.set_margin_top(20)
        self.drop_image.set_margin_start(20)
        self.drop_image.set_margin_end(20)

        # 2. Set up the Drag and Drop target
        drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        drop_target.connect("drop", self.on_drop)
        self.drop_image.add_controller(drop_target)

        # 3. Create the new text label
        drop_label = Gtk.Label(label="Drag and Drop Images")
        drop_label.add_css_class("body")

        # 4. Create the button and connect the click action
        browseFilesButton = RoundedButton(
            label="Browse Files",
            width=200,
            height=55,
            on_click=on_browse_button_click # UPDATED: Pass the click action to the button
        )
        browseFilesButton.set_margin_top(15)
        browseFilesButton.set_margin_bottom(20)

        # 5. Add the widgets in the correct order
        self.append(self.drop_image)
        self.append(drop_label)
        self.append(browseFilesButton)

        # The theme-switching logic remains the same
        style_manager = Adw.StyleManager.get_default()
        style_manager.connect("notify::dark", self.on_theme_change)
        self.on_theme_change(style_manager)

        # Load custom CSS to remove drag-and-drop border
        self._load_styling_css()

    def on_theme_change(self, style_manager, pspec=None):
        """Callback function for when the system theme changes."""
        if style_manager.get_dark():
            self.drop_image.set_from_file(str(DARK_ICON_PATH))
        else:
            self.drop_image.set_from_file(str(LIGHT_ICON_PATH))

    def on_drop(self, drop_target, value, x, y):
        """Callback function for when a file is dropped."""
        files = value.get_files()
        for file in files:
            print(f"File dropped: {file.get_path()}")
        return True

    def _load_styling_css(self):
        # REMOVED: Unnecessary print statement
        css = """
        .picaxe-drop-zone:drop(active) {
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )