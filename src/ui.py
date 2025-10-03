import gi
from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Adw

from components.buttons.button import RoundedButton

# This creates robust paths to your assets
APP_DIR = Path(__file__).resolve().parent.parent
LIGHT_ICON_PATH = APP_DIR / "assets" / "pictures" /"drag_and_drop_visual_dark.png"
DARK_ICON_PATH = APP_DIR / "assets" / "pictures" /"drag_and_drop_visual_dark.png"


class MainUI(Gtk.Box):
    def __init__(self):
        # The main box will be vertical. Spacing is between elements.
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=5  # Changed: Reduced spacing between image and label
        )

        # 1. Configure the Image widget for expansion
        self.drop_image = Gtk.Image()
        self.drop_image.add_css_class("picaxe-drop-zone")
        self.drop_image.set_vexpand(True)
        self.drop_image.set_margin_top(20)
        self.drop_image.set_margin_start(20)
        self.drop_image.set_margin_end(20)

        # 2. Set up the Drag and Drop target on the (now large) image
        drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        drop_target.connect("drop", self.on_drop)
        self.drop_image.add_controller(drop_target)


        # 3. Create the new text label
        drop_label = Gtk.Label(label="Drag and Drop Images")
        drop_label.add_css_class("body")

        # 4. Create the button
        browseFilesButton = RoundedButton(
            label="Browse Files",
            width=150,
            height=50
        )
        browseFilesButton.set_margin_top(40)
        browseFilesButton.set_margin_bottom(20)

        # 5. Add the widgets in the correct order
        self.append(self.drop_image)
        self.append(drop_label)
        self.append(browseFilesButton)

        # The theme-switching logic remains the same
        style_manager = Adw.StyleManager.get_default()
        style_manager.connect("notify::dark", self.on_theme_change)
        self.on_theme_change(style_manager)

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
        print("kkkkkkkk")
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