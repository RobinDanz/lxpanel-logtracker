import threading
import time
from itertools import cycle
from pathlib import Path

from watchdog.observers import Observer
from logtracker.watcher import LsyncdLogWatcher
from logtracker import const

import pystray
from PIL import Image

class PystrayMonitorApp:
    def __init__(self, log_file):
        self.log_file = log_file

        # Chargement des icônes avec PIL.Image
        self.icon_idle = Image.open(const.ICON_IDLE)
        self.icon_active = Image.open(const.ICON_ACTIVE)

        # Animation
        self._anim_cycle = cycle([self.icon_idle, self.icon_active])
        self._animating = threading.Event()
        self._stop_event = threading.Event()

        # Pystray icon
        self.icon = pystray.Icon(
            "LogMon",
            self.icon_idle,
            "Log Monitor",
            menu=pystray.Menu(
                pystray.MenuItem("Quitter", self.quit_app)
            )
        )

        # Watchdog
        parent_folder = Path(log_file).parent
        event_handler = LsyncdLogWatcher(log_file=self.log_file, handler=self)
        self.observer = Observer()
        self.observer.schedule(event_handler=event_handler, path=parent_folder, recursive=False)
        self.observer.start()

        # Thread d’animation
        self.anim_thread = threading.Thread(target=self._blink_icon, daemon=True)
        self.anim_thread.start()

    def run(self):
        """Démarre l’icône système (bloquant tant qu’elle est active)."""
        self.icon.run()

    def quit_app(self, _=None):
        """Quitte proprement."""
        self._stop_event.set()
        self._animating.clear()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        self.icon.stop()

    def notify(self, line):
        """Appelée par le watcher pour chaque nouvelle ligne de log."""
        print(f"Line: {line}")
        if 'copy_start' in line:
            self.start_animation()
        elif 'copy_end' in line:
            self.stop_animation()

    def start_animation(self):
        self._animating.set()

    def stop_animation(self):
        self._animating.clear()
        self.icon.icon = self.icon_idle

    def _blink_icon(self):
        """Fait clignoter l’icône pendant que _animating est actif."""
        while not self._stop_event.is_set():
            if self._animating.is_set():
                next_icon = next(self._anim_cycle)
                self.icon.icon = next_icon
                self.icon.update_menu()  # Rafraîchit le tray
                time.sleep(0.3)
            else:
                time.sleep(0.2)