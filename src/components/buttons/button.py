import gi
import sys

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk

class RoundedButton(Gtk.Button):
    # REMOVED: user_color parameter is no longer needed.
    def __init__(self, label="Button", width=150, height=50, on_click=None):
        """
        A custom Gtk.Button that uses the system's accent color.
        """
        super().__init__(label=label)

        self.set_size_request(width, height)
        if on_click:
            self.connect("clicked", on_click)

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)
        self.add_css_class("suggested-action")
        
        # Add a style class to target this button specifically if needed.
        self.add_css_class("pill-button")

        # --- Updated CSS using GTK's named colors ---
        css = f"""
        /* Target our custom button class */
        .pill-button {{
            font-size: 1rem;
            font-weight: bold;
            
            /* * CHANGED: Use @accent_color for the background.
             * GTK automatically substitutes this with the user's chosen color.
             */
            background-color: @accent_color;
            
            /*
             * Use @accent_fg_color for the text. This is a color
             * guaranteed by the theme to have good contrast with @accent_color.
             */
            color: @accent_fg_color;
            
            border: none;
            border-radius: {height // 2}px;
            transition: background-color 0.15s ease-in-out;
        }}

        .pill-button:hover {{
            /* We can still use lighten() on the named color */
            background-color: lighten(@accent_color, 1.1);
        }}

        .pill-button:active {{
            background-color: darken(@accent_color, 0.9);
        }}
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())

        self.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)