import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Crunchy")
        self.set_default_size(600, 400)

class ImageToolApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.imagetool")

    def do_activate(self, *args):
        win = MainWindow(self)
        win.present()

if __name__ == "__main__":
    app = ImageToolApp()
    app.run()
