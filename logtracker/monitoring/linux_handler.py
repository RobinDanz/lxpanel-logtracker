
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib
from logtracker import const

class LinuxLogMonitorApp:
    def __init__(self):
        print('Init linux handler')
        
    indicator = AppIndicator3.Indicator.new(
        "logmonitor",
        const.ICON_IDLE,
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    # menu = Gtk.Menu()
    # quit_item = Gtk.MenuItem(label="Quitter")
    # quit_item.connect("activate", Gtk.main_quit)
    # menu.append(quit_item)
    # menu.show_all()
    # indicator.set_menu(menu)

    # def on_activity(active):
    #     GLib.idle_add(
    #         indicator.set_icon_full,
    #         ICON_ACTIVE if active else ICON_IDLE,
    #         "Active" if active else "Idle"
    #     )

    # threading.Thread(target=get_log_activity, args=(on_activity,), daemon=True).start()
    # Gtk.main()