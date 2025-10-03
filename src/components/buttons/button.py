import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class RoundedButton(Gtk.Button):
    def __init__(self, label="Button", width=150, height=50, on_click=None):
        """A custom, pill-shaped Gtk.Button that uses the system's accent color."""
        super().__init__(label=label)

        self.set_size_request(width, height)
        if on_click:
            self.connect("clicked", on_click)

        self.set_halign(Gtk.Align.CENTER)
        self.set_valign(Gtk.Align.CENTER)

        #things you have to do get get accented by system
        self.add_css_class("suggested-action")
        #add css class
        self.add_css_class("pill-button")

        css = f"""
        .pill-button {{
            border-radius: {height // 2}px;
        }}
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css.encode())
        self.get_style_context().add_provider(provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)