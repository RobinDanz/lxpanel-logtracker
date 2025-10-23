import threading
import time
from itertools import cycle
from pathlib import Path

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GLib

from watchdog.observers import Observer
from logtracker.watcher import LsyncdLogWatcher
from logtracker import const


class RaspbianAppIndicator:
    def __init__(self, log_file):
        self.log_file = log_file
        self.indicator = AppIndicator3.Indicator.new(
            "LogMon",
            const.ICON_IDLE,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS
        )
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # Menu
        menu = Gtk.Menu()
        quit_item = Gtk.MenuItem(label="Quitter")
        quit_item.connect("activate", self.quit_app)
        menu.append(quit_item)
        menu.show_all()
        self.indicator.set_menu(menu)

        # Animation
        self._animating = False
        self._anim_cycle = cycle([const.ICON_IDLE, const.ICON_ACTIVE])

        # Watchdog
        parent_folder = Path(log_file).parent
        event_handler = LsyncdLogWatcher(log_file=self.log_file, handler=self)
        self.observer = Observer()
        self.observer.schedule(event_handler=event_handler, path=parent_folder, recursive=False)
        self.observer.start()

        # Thread d’animation
        self._stop_event = threading.Event()
        self._anim_thread = threading.Thread(target=self._blink_icon, daemon=True)
        self._anim_thread.start()

    def notify(self, line):
        print(f"Line: {line}")
        if "copy_start" in line:
            self.start_animation()
        elif "copy_end" in line:
            self.stop_animation()

    def start_animation(self):
        self._animating = True

    def stop_animation(self):
        self._animating = False
        GLib.idle_add(self.indicator.set_icon, const.ICON_IDLE)

    def _blink_icon(self):
        """Thread d’animation (utilise GLib.idle_add pour maj depuis le thread Gtk)"""
        while not self._stop_event.is_set():
            if self._animating:
                next_icon = next(self._anim_cycle)
                GLib.idle_add(self.indicator.set_icon, next_icon)
                time.sleep(0.3)
            else:
                time.sleep(0.2)

    def quit_app(self, _):
        print("Quit")
        self._stop_event.set()
        self.observer.stop()
        self.observer.join()
        Gtk.main_quit()

    def run(self):
        Gtk.main()


if __name__ == "__main__":
    app = RaspbianAppIndicator("/path/to/your/logfile.log")
    app.run()