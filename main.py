import sys
from PyQt5 import QtWidgets, QtGui
from voicemeeterlib import api
from widgets.volume_panel import VolumePanel
from widgets.routing_panel import RoutingPanel
from utils.audio_device import restore_default_audio

ICON_PATH = "tray_icon.ico"

class TrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon_path, vm, parent=None):
        super().__init__(QtGui.QIcon(icon_path), parent)
        self.vm = vm
        self.volume_panel = VolumePanel(vm)
        self.routing_panel = RoutingPanel(vm)

        menu = QtWidgets.QMenu(parent)
        menu.addAction("Show Volume Sliders", self.toggle_volume)
        menu.addAction("Show Routing Controls", self.toggle_routing)
        menu.addSeparator()
        menu.addAction("Restore Default Audio Devices", restore_default_audio)
        menu.addSeparator()
        menu.addAction("Exit", QtWidgets.qApp.quit)

        self.setContextMenu(menu)
        self.activated.connect(self.icon_clicked)

    def icon_clicked(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.toggle_volume()

    def toggle_volume(self):
        if self.volume_panel.isVisible():
            self.volume_panel.hide()
        else:
            self.volume_panel.update_sliders()
            self._position_panel(self.volume_panel)
            self.volume_panel.show()

    def toggle_routing(self):
        if self.routing_panel.isVisible():
            self.routing_panel.hide()
        else:
            self._position_panel(self.routing_panel)
            self.routing_panel.show()

    def _position_panel(self, panel):
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        pos = QtGui.QCursor.pos()
        w, h = panel.frameGeometry().width(), panel.frameGeometry().height()
        x = min(pos.x(), screen.width() - w)
        y = min(pos.y(), screen.height() - h)
        panel.move(x, y)

def main():
    app = QtWidgets.QApplication(sys.argv)
    with api("potato") as vm:
        tray = TrayApp(ICON_PATH, vm)
        tray.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
