import gi
from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Adw

from components.buttons.button import RoundedButton
from components.cards.imagecard import ImageCard

# This creates robust paths to your assets
APP_DIR = Path(__file__).resolve().parent.parent
# UPDATED: Correct path for the new light mode image
LIGHT_ICON_PATH = APP_DIR / "assets" / "pictures" / "drag_and_drop_visual_dark.png"
DARK_ICON_PATH = APP_DIR / "assets" / "pictures" / "drag_and_drop_visual_dark.png"


class MainUI(Gtk.Box):
    def __init__(self, on_browse_button_click=None, on_drop_files=None):
        super().__init__(
            orientation=Gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.on_drop_files = on_drop_files
        self.on_browse_button_click = on_browse_button_click
        self.image_items = []  # Store image items for display
        
        # Create a stack to switch between drop zone and image list
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.stack.set_transition_duration(300)
        
        # Create the drop zone page
        self._create_drop_zone_page()
        
        # Create the image list page  
        self._create_image_list_page()
        
        # Add stack to main container
        self.append(self.stack)
        
        # Start with drop zone visible
        self.stack.set_visible_child_name("drop_zone")
        
        # Load custom CSS
        self._load_styling_css()
    
    def _create_drop_zone_page(self):
        """Create the initial drop zone interface."""
        drop_zone_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        
        # Configure the Image widget for expansion
        self.drop_image = Gtk.Image()
        self.drop_image.add_css_class("picaxe-drop-zone")
        self.drop_image.set_vexpand(True)
        self.drop_image.set_margin_top(20)
        self.drop_image.set_margin_start(20)
        self.drop_image.set_margin_end(20)

        # Set up the Drag and Drop target
        drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        drop_target.connect("drop", self.on_drop)
        self.drop_image.add_controller(drop_target)

        # Create the text label
        drop_label = Gtk.Label(label="Drag and Drop Images")
        drop_label.add_css_class("body")

        # Create the button
        browse_button = RoundedButton(
            label="Browse Files",
            width=160,
            height=55,
            on_click=self.on_browse_button_click
        )
        browse_button.set_margin_top(15)
        browse_button.set_margin_bottom(20)

        # Add widgets to drop zone
        drop_zone_box.append(self.drop_image)
        drop_zone_box.append(drop_label)
        drop_zone_box.append(browse_button)
        
        # Add to stack
        self.stack.add_named(drop_zone_box, "drop_zone")
        
        # Set up theme switching for drop zone
        style_manager = Adw.StyleManager.get_default()
        style_manager.connect("notify::dark", self.on_theme_change)
        self.on_theme_change(style_manager)
    
    def _create_image_list_page(self):
        """Create the image list interface with scrollable cards."""
        # Create main container for image list
        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        # Create header with title and add button
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_margin_top(16)
        header_box.set_margin_start(16)
        header_box.set_margin_end(16)
        header_box.set_margin_bottom(8)
        
        title_label = Gtk.Label(label="Images")
        title_label.add_css_class("title-2")
        title_label.set_halign(Gtk.Align.START)
        title_label.set_hexpand(True)
        
        add_more_button = RoundedButton(
            label="Add More",
            width=100,
            height=32,
            on_click=self.on_browse_button_click
        )
        
        header_box.append(title_label)
        header_box.append(add_more_button)
        
        # Create scrolled window for image cards
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_vexpand(True)
        
        # Create box to hold image cards
        self.cards_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.cards_box.set_margin_start(8)
        self.cards_box.set_margin_end(8)
        
        self.scrolled_window.set_child(self.cards_box)
        
        # Add components to list page
        list_box.append(header_box)
        list_box.append(self.scrolled_window)
        
        # Add to stack
        self.stack.add_named(list_box, "image_list")
    
    def add_image_items(self, image_items):
        """Add image items and switch to image list view."""
        self.image_items.extend(image_items)
        
        # Clear existing cards
        child = self.cards_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.cards_box.remove(child)
            child = next_child
        
        # Add new cards
        for item in self.image_items:
            card = ImageCard(item)
            self.cards_box.append(card)
        
        # Switch to image list view
        self.stack.set_visible_child_name("image_list")

    def on_theme_change(self, style_manager, pspec=None):
        """Callback function for when the system theme changes."""
        if style_manager.get_dark():
            self.drop_image.set_from_file(str(DARK_ICON_PATH))
        else:
            self.drop_image.set_from_file(str(LIGHT_ICON_PATH))

    def on_drop(self, drop_target, value, x, y):
        """Callback function for when a file is dropped."""
        files = value.get_files()
        if self.on_drop_files:
            self.on_drop_files(files)
        else:
            # Fallback if no callback is provided
            for file in files:
                print(f"File dropped: {file.get_path()}")
        return True

    def _load_styling_css(self):
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