#!/usr/bin/env python3
#main.py

import gi
import sys

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw

from ui import MainUI

class PicaxeApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(application_id="com.example.crunchy", **kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):

        win = Adw.ApplicationWindow(application=app)
        win.set_title("Picaxe")
        win.set_default_size(500, 600) 

        main_view = Adw.ToolbarView()
        
        header = Adw.HeaderBar()
        main_view.add_css_class("flat")

        main_view.add_top_bar(header)

        content = MainUI()
        main_view.set_content(content)
        win.set_content(main_view)

        win.present()

if __name__ == "__main__":
    app = PicaxeApp()
    app.run(sys.argv)