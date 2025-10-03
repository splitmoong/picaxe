import gi
from pathlib import Path

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GdkPixbuf

from constants import MARGIN_STANDARD, MARGIN_SMALL, CARD_INNER_SPACING, THUMBNAIL_SIZE

class ImageCard(Gtk.Box):
    def __init__(self, image_item):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=CARD_INNER_SPACING)
        
        self.image_item = image_item
        
        # Card itself has margins from the window edges
        self.set_margin_top(MARGIN_SMALL)
        self.set_margin_bottom(MARGIN_SMALL)
        self.set_margin_start(MARGIN_STANDARD)  # 16px from left window edge
        self.set_margin_end(MARGIN_STANDARD)    # 16px from right window edge
        
        # Create thumbnail - no additional margins since card handles positioning
        self.thumbnail = Gtk.Image()
        self.thumbnail.set_size_request(THUMBNAIL_SIZE, THUMBNAIL_SIZE)
        self._load_thumbnail()
        
        # Create info section
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        info_box.set_hexpand(True)
        info_box.set_valign(Gtk.Align.CENTER)
        
        # Filename label
        filename_label = Gtk.Label(label=image_item.path.name)
        filename_label.set_halign(Gtk.Align.START)
        filename_label.add_css_class("heading")
        
        # Size and format info
        size_text = f"{image_item.size_kb:.1f} KB • {image_item.original_type.upper()}"
        size_label = Gtk.Label(label=size_text)
        size_label.set_halign(Gtk.Align.START)
        size_label.add_css_class("dim-label")
        
        info_box.append(filename_label)
        info_box.append(size_label)
        
        # Add components to the card
        self.append(self.thumbnail)
        self.append(info_box)
        
        # Add card styling
        self.add_css_class("card")
        self._load_card_css()
    
    def _load_thumbnail(self):
        """Load and set the thumbnail image."""
        try:
            # Create a scaled pixbuf from the image file
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                str(self.image_item.path), 
                THUMBNAIL_SIZE, THUMBNAIL_SIZE, 
                True  # preserve aspect ratio
            )
            self.thumbnail.set_from_pixbuf(pixbuf)
        except Exception as e:
            print(f"Could not load thumbnail for {self.image_item.path}: {e}")
            # Set a placeholder or default icon
            self.thumbnail.set_from_icon_name("image-missing")
    
    def _load_card_css(self):
        """Load custom CSS for the card styling."""
        css = f"""
        .card {{
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: {MARGIN_STANDARD}px; /* CHANGED THIS LINE */
        }}
        .card:hover {{
            background-color: rgba(255, 255, 255, 0.1);
        }}
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        self.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)