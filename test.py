import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import Gtk, AyatanaAppIndicator3

indicator = AyatanaAppIndicator3.Indicator.new(
    "test-icon",
    "/usr/share/icons/hicolor/16x16/status/dialog-information.png",
    AyatanaAppIndicator3.IndicatorCategory.APPLICATION_STATUS
)

indicator.set_status(AyatanaAppIndicator3.IndicatorStatus.ACTIVE)

menu = Gtk.Menu()
item_quit = Gtk.MenuItem(label="Quitter")
item_quit.connect("activate", Gtk.main_quit)
menu.append(item_quit)
menu.show_all()

indicator.set_menu(menu)

Gtk.main()