import gi
from pathlib import Path

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gdk, Adw

from components.buttons.button import RoundedButton
from components.cards.imagecard import ImageCard
from constants import MARGIN_STANDARD, MARGIN_SMALL, CARD_SPACING

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
        
        # We'll create a persistent footer (drag hint + Browse button) after the stack

        # Create the drop zone page
        self._create_drop_zone_page()
        
        # Create the image list page  
        self._create_image_list_page()

        # Add stack to main container
        self.append(self.stack)

        # Start with drop zone visible
        self.stack.set_visible_child_name("drop_zone")
        # Footer with persistent drag hint and Browse button at the bottom
        footer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        footer_box.set_margin_top(MARGIN_SMALL)
        footer_box.set_margin_bottom(MARGIN_STANDARD)
        footer_box.set_margin_start(MARGIN_STANDARD)
        footer_box.set_margin_end(MARGIN_STANDARD)
        footer_box.set_hexpand(True)

    # Footer contains only the persistent Browse button

        self.browse_button = RoundedButton(
            label="Browse Files",
            width=160,
            height=55,
            on_click=self.on_browse_button_click
        )
        self.browse_button.set_halign(Gtk.Align.CENTER)

        footer_box.append(self.browse_button)

        # Append footer to the main container so it stays at the bottom
        self.append(footer_box)

        # Load custom CSS
        self._load_styling_css()
    
    def _create_drop_zone_page(self):
        """Create the initial drop zone interface."""
        drop_zone_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        # Configure the Image widget for expansion (purely presentational)
        self.drop_image = Gtk.Image()
        self.drop_image.add_css_class("picaxe-drop-zone")
        self.drop_image.set_vexpand(True)
        self.drop_image.set_margin_top(20)
        self.drop_image.set_margin_bottom(0)
        self.drop_image.set_margin_start(MARGIN_STANDARD)
        self.drop_image.set_margin_end(MARGIN_STANDARD)


        # Note: attach a DropTarget to the entire MainUI (self) so drops work
        # even after the splash. Attach here once.
        drop_target = Gtk.DropTarget.new(Gdk.FileList, Gdk.DragAction.COPY)
        drop_target.connect("drop", self.on_drop)
        # attach to the top-level widget (self)
        self.add_controller(drop_target)

        # Add the presentational image to the drop zone
        drop_zone_box.append(self.drop_image)
    # no splash label — splash image only

        # Add to stack
        self.stack.add_named(drop_zone_box, "drop_zone")

        # Set up theme switching for drop image
        style_manager = Adw.StyleManager.get_default()
        style_manager.connect("notify::dark", self.on_theme_change)
        self.on_theme_change(style_manager)
    
    def _create_image_list_page(self):
        """Create the image list interface with scrollable cards."""
        # Create main container for image list
        list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        
        # Create header with title and add button
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_margin_top(MARGIN_STANDARD)
        header_box.set_margin_start(MARGIN_STANDARD)
        header_box.set_margin_end(MARGIN_STANDARD)
        header_box.set_margin_bottom(MARGIN_SMALL)
        
        # title_label is persistent in the header; keep header_box empty here
        # so the stack page aligns under the global header
        
        # No Add More button — Browse Files is persistent in the header
        
        header_box.append(Gtk.Label())  # spacer to keep layout consistent
        
        # Create scrolled window for image cards
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.scrolled_window.set_vexpand(True)
        
        # Create box to hold image cards
        self.cards_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=CARD_SPACING)
        self.cards_box.set_margin_start(0)  # No margins - cards handle their own positioning
        self.cards_box.set_margin_end(0)    # No margins - cards handle their own positioning
        
        self.scrolled_window.set_child(self.cards_box)
        
        # Add components to list page
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
            card = ImageCard(item, on_delete=self._on_delete_image)
            self.cards_box.append(card)
        
        # Switch to image list view
        self.stack.set_visible_child_name("image_list")
    # Footer keeps the Browse button; no splash label used anymore
    
    def _on_delete_image(self, image_item):
        """Handle deletion of an image item."""
        try:
            # Remove from internal list
            self.image_items.remove(image_item)
            
            # Also remove from parent app's list if available
            if hasattr(self, 'parent_app') and self.parent_app:
                try:
                    self.parent_app.image_items.remove(image_item)
                except ValueError:
                    pass  # Item might not be in parent list
            
            # Refresh the card display
            self._refresh_cards()
            
            # If no images left, go back to drop zone
            if not self.image_items:
                self.stack.set_visible_child_name("drop_zone")
                # no splash label to show; splash image will be visible
                
            print(f"Deleted: {image_item.path.name}")
        except ValueError:
            print(f"Error: Image item not found in list")
    
    def _refresh_cards(self):
        """Refresh the card display after deletion."""
        # Clear existing cards
        child = self.cards_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.cards_box.remove(child)
            child = next_child
        
        # Add remaining cards
        for item in self.image_items:
            card = ImageCard(item, on_delete=self._on_delete_image)
            self.cards_box.append(card)

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