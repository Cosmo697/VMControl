import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from voicemeeterlib import api
from widgets.combined_panel import CombinedControlPanel

ICON_PATH = "tray_icon.ico"

class TrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon_path, vm, parent=None):
        super().__init__(QtGui.QIcon(icon_path), parent)
        self.vm = vm
        self.control_panel = CombinedControlPanel(vm)
        
        # Install application-wide event filter for auto-hide
        QtWidgets.qApp.installEventFilter(self)

        menu = QtWidgets.QMenu(parent)
        menu.addAction("Show Controls", self.toggle_controls)
        menu.addSeparator()
        menu.addAction("Exit", QtWidgets.qApp.quit)

        self.setContextMenu(menu)
        self.activated.connect(self.icon_clicked)

    def icon_clicked(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.toggle_controls()

    def toggle_controls(self):
        if self.control_panel.isVisible():
            self.control_panel.hide()
        else:
            self.control_panel.update_controls()
            self._position_panel(self.control_panel)
            self.control_panel.show()

    def _position_panel(self, panel):
        screen = QtWidgets.QDesktopWidget().availableGeometry()
        pos = QtGui.QCursor.pos()
        w, h = panel.frameGeometry().width(), panel.frameGeometry().height()
        x = min(pos.x(), screen.width() - w)
        y = min(pos.y(), screen.height() - h)
        panel.move(x, y)

    def eventFilter(self, obj, event):
        """Global event filter to hide panel when clicking outside"""
        # MouseButtonPress = 2, MouseButtonRelease = 3
        if (self.control_panel.isVisible() and 
            event.type() == 2):  # MouseButtonPress
            
            # Check if the click is outside the control panel
            try:
                # Get the widget that was clicked
                widget_under_mouse = QtWidgets.qApp.widgetAt(QtGui.QCursor.pos())
                
                # Check if the clicked widget is part of our control panel
                is_inside_panel = False
                current_widget = widget_under_mouse
                
                while current_widget:
                    if current_widget == self.control_panel:
                        is_inside_panel = True
                        break
                    current_widget = current_widget.parent()
                
                # If click is outside the panel, hide it
                if not is_inside_panel:
                    self.control_panel.hide()
                    return True
                    
            except Exception as e:
                print(f"Event filter error: {e}")
                pass
                
        return super().eventFilter(obj, event)

def main():
    app = QtWidgets.QApplication(sys.argv)
    with api("potato") as vm:
        tray = TrayApp(ICON_PATH, vm)
        tray.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
