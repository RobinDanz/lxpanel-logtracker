from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QCursor
import sys

class MiniTray(QWidget):
    def __init__(self):
        super().__init__()

        # --- Apparence générale ---
        self.setWindowFlags(
            Qt.FramelessWindowHint |     # Pas de bordures
            Qt.WindowStaysOnTopHint |    # Toujours au-dessus
            Qt.Tool                      # Fenêtre utilitaire, pas dans la barre des tâches
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                border: 1px solid #5E81AC;
                border-radius: 10px;
                color: white;
                font-family: Sans;
                font-size: 12pt;
            }
            QPushButton {
                background-color: #4C566A;
                border: none;
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #5E81AC;
            }
        """)

        # --- Layout & contenu ---
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)

        layout.addWidget(QLabel("🔧 Mon mini-menu"))
        btn_start = QPushButton("Démarrer")
        btn_stop = QPushButton("Arrêter")
        btn_quit = QPushButton("Quitter")

        layout.addWidget(btn_start)
        layout.addWidget(btn_stop)
        layout.addWidget(btn_quit)
        self.setLayout(layout)

        # --- Actions ---
        btn_quit.clicked.connect(self.close)

        # --- Position ---
        self.reposition()

        # --- Optionnel : fermer automatiquement après 10s ---
        # QTimer.singleShot(10000, self.close)

    def reposition(self):
        """Place la fenêtre près du curseur."""
        pos = QCursor.pos()
        self.move(pos.x() - self.width() // 2, pos.y() - self.height() // 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tray = MiniTray()
    tray.show()
    sys.exit(app.exec_())