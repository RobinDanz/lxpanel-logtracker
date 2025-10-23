from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
import sys

app = QApplication(sys.argv)

tray = QSystemTrayIcon(QIcon("/usr/share/icons/Adwaita/16x16/status/dialog-information.png"), app)
menu = QMenu()
quit_action = QAction("Quitter")
quit_action.triggered.connect(app.quit)
menu.addAction(quit_action)
tray.setContextMenu(menu)
tray.show()

sys.exit(app.exec_())