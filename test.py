#!/usr/bin/env python3
import gi, signal, time
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

ICON_ON = "/usr/share/icons/Adwaita/16x16/status/dialog-information.png"
ICON_OFF = "/usr/share/icons/Adwaita/16x16/status/dialog-warning.png"

class TrayBlinker:
    def __init__(self):
        self.icon = Gtk.StatusIcon()
        self.visible = True
        self.icon.set_from_file(ICON_ON)
        self.icon.set_tooltip_text("Icône clignotante")

        # clic gauche = quitter
        self.icon.connect("activate", self.quit)

        GLib.timeout_add(500, self.toggle_icon)  # 500 ms blink

    def toggle_icon(self):
        if self.visible:
            self.icon.set_from_file(ICON_OFF)
        else:
            self.icon.set_from_file(ICON_ON)
        self.visible = not self.visible
        return True  # keep repeating

    def quit(self, _):
        Gtk.main_quit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = TrayBlinker()
    Gtk.main()