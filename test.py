import sys
import threading
import time
from itertools import cycle
from pathlib import Path

from watchdog.observers import Observer
from logtracker.watcher import LsyncdLogWatcher
from logtracker import const

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer, QRect
from PyQt5.QtGui import QPixmap


class LogMonitorWidget(QWidget):
    def __init__(self, log_file):
        super().__init__()

        self.log_file = log_file

        # --- Icônes ---
        self.icon_idle = QPixmap(const.ICON_IDLE)
        self.icon_active = QPixmap(const.ICON_ACTIVE)
        self._anim_cycle = cycle([self.icon_idle, self.icon_active])

        # --- État ---
        self._animating = threading.Event()
        self._stop_event = threading.Event()

        # --- Interface graphique ---
        self.setWindowFlags(
            Qt.FramelessWindowHint |     # pas de bordure
            Qt.WindowStaysOnTopHint |    # reste au-dessus
            Qt.Tool                      # pas dans la barre des tâches
        )
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                border: 1px solid #5E81AC;
                border-radius: 10px;
                color: white;
                font-family: Sans;
                font-size: 11pt;
            }
            QPushButton {
                background-color: #4C566A;
                border: none;
                border-radius: 5px;
                padding: 4px 8px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel("🟢 En veille")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

        self.icon_label = QLabel()
        self.icon_label.setPixmap(self.icon_idle)
        self.icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.icon_label)

        self.btn_quit = QPushButton("Quitter")
        self.btn_quit.clicked.connect(self.quit_app)
        layout.addWidget(self.btn_quit)

        self.setLayout(layout)
        self.resize(120, 140)

        # --- Position : coin supérieur droit ---
        screen_geometry = QApplication.primaryScreen().geometry()
        print(screen_geometry)
        self.move(screen_geometry.width() - self.width() - 20, 20)

        # --- Watchdog ---
        parent_folder = Path(log_file).parent
        event_handler = LsyncdLogWatcher(log_file=log_file, handler=self)
        self.observer = Observer()
        self.observer.schedule(event_handler=event_handler, path=parent_folder, recursive=False)
        self.observer.start()

        # --- Animation via QTimer (remplace thread pystray) ---
        self.timer = QTimer()
        self.timer.timeout.connect(self._blink_icon)
        self.timer.start(300)  # 300 ms

    # -------------------------------
    # Gestion Watcher
    # -------------------------------

    def notify(self, line):
        """Appelée par le watcher pour chaque nouvelle ligne de log."""
        print(f"Line: {line}")
        if 'copy_start' in line:
            self.start_animation()
        elif 'copy_end' in line:
            self.stop_animation()

    def start_animation(self):
        self._animating.set()
        self.label.setText("🔵 En activité")

    def stop_animation(self):
        self._animating.clear()
        self.label.setText("🟢 En veille")
        self.icon_label.setPixmap(self.icon_idle)

    def _blink_icon(self):
        """Animation clignotante pendant l'activité."""
        if self._animating.is_set():
            next_icon = next(self._anim_cycle)
            self.icon_label.setPixmap(next_icon)

    # -------------------------------
    # Gestion application
    # -------------------------------

    def quit_app(self):
        self._stop_event.set()
        self._animating.clear()
        if self.observer:
            self.observer.stop()
            self.observer.join()
        QApplication.quit()


def main():
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # pour Ctrl+C dans le terminal

    log_file = '/Users/robin/DEV/lxpanel-logtracker/logs/lsyncd.log'  # ou ton chemin spécifique
    app = QApplication(sys.argv)
    widget = LogMonitorWidget(log_file)
    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()