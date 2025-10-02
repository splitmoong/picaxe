#main.py

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
from ui import MainUI

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Crunchy")
        self.set_default_size(800, 600)

        # Add the UI
        ui = MainUI()
        self.set_child(ui)

class CrunchyApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.crunchy")

    def do_activate(self):
        win = MainWindow(self)
        win.present()

if __name__ == "__main__":
    app = CrunchyApp()
    app.run()
