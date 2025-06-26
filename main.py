import sys
import os
import signal
import atexit
from PyQt5 import QtWidgets, QtGui, QtCore
from voicemeeterlib import api
from widgets.combined_panel import CombinedControlPanel
from widgets.constants import STRIP_INDICES
from widgets.preset_manager import PresetManager

ICON_PATH = "tray_icon.ico"
LOCK_FILE = "vmcontrol.lock"

class SingleInstanceApp(QtWidgets.QApplication):
    """Application that ensures only one instance can run at a time"""
    def __init__(self, argv, unique_key="VMControl_SingleInstance"):
        super().__init__(argv)
        self.unique_key = unique_key
        self.shared_memory = QtCore.QSharedMemory(unique_key)
        self.is_running = False
        
        # Try to create shared memory segment
        if self.shared_memory.create(1):
            # First instance - we're good to go
            self.is_running = False
            # Register cleanup on exit
            atexit.register(self.cleanup)
        else:
            # Another instance is already running
            self.is_running = True
            
    def cleanup(self):
        """Clean up shared memory on exit"""
        if self.shared_memory.isAttached():
            self.shared_memory.detach()

class TrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon_path, vm, parent=None):
        super().__init__(QtGui.QIcon(icon_path), parent)
        self.vm = vm
        self.control_panel = CombinedControlPanel(vm)
        self.shutting_down = False
        
        # Install application-wide event filter for auto-hide
        QtWidgets.qApp.installEventFilter(self)

        menu = QtWidgets.QMenu(parent)
        menu.addAction("Show Controls", self.toggle_controls)
        menu.addAction("Mute All", self.toggle_all_mutes)
        menu.addAction("Save Preset", self.save_preset)
        menu.addAction("Load Preset", self.load_preset)
        menu.addSeparator()
        menu.addAction("Exit", self.graceful_shutdown)

        self.setContextMenu(menu)
        self.activated.connect(self.icon_clicked)
        
        # Handle system shutdown signals
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Setup graceful shutdown timer
        self.shutdown_timer = QtCore.QTimer()
        self.shutdown_timer.setSingleShot(True)
        self.shutdown_timer.timeout.connect(QtWidgets.qApp.quit)

    def signal_handler(self, signum, frame):
        """Handle system shutdown signals"""
        self.graceful_shutdown()

    def graceful_shutdown(self):
        """Perform graceful shutdown of the application"""
        if self.shutting_down:
            return
            
        self.shutting_down = True
        
        try:
            # Hide the control panel first
            if self.control_panel and self.control_panel.isVisible():
                self.control_panel.hide()
            
            # Stop any timers in the control panel
            if hasattr(self.control_panel, 'volume_panel'):
                volume_panel = self.control_panel.volume_panel
                if hasattr(volume_panel, 'vu_timer') and volume_panel.vu_timer.isActive():
                    volume_panel.vu_timer.stop()
                
                # Clear any ongoing reset operations
                if hasattr(volume_panel, 'resetting_strips'):
                    volume_panel.resetting_strips.clear()
            
            # Stop hide timer if active
            if hasattr(self.control_panel, 'hide_timer') and self.control_panel.hide_timer.isActive():
                self.control_panel.hide_timer.stop()
            
            # Hide the tray icon
            self.hide()
            
        except Exception as e:
            print(f"Error during shutdown: {e}")
        
        # Force quit after a short delay if normal shutdown doesn't work
        self.shutdown_timer.start(1000)  # 1 second timeout
        QtWidgets.qApp.quit()

    def icon_clicked(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.toggle_controls()

    def toggle_all_mutes(self):
        """Toggle mute state for all configured strips."""
        states = []
        for idx in STRIP_INDICES:
            try:
                states.append(getattr(self.vm.strip[idx], "mute"))
            except (IndexError, AttributeError):
                pass
        new_state = not all(states)
        for idx in STRIP_INDICES:
            try:
                setattr(self.vm.strip[idx], "mute", new_state)
            except (IndexError, AttributeError):
                pass
        self.control_panel.volume_panel.update_sliders()

    def save_preset(self):
        """Save current Voicemeeter configuration to a file."""
        path, _ = QtWidgets.QFileDialog.getSaveFileName(
            None, "Save Preset", "vm_preset.json", "JSON Files (*.json)"
        )
        if path:
            PresetManager.save_preset(self.vm, path)

    def load_preset(self):
        """Load Voicemeeter configuration from a preset file."""
        path, _ = QtWidgets.QFileDialog.getOpenFileName(
            None, "Load Preset", "", "JSON Files (*.json)"
        )
        if path:
            PresetManager.load_preset(self.vm, path)
            self.control_panel.update_controls()

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
        # Hide the panel if any mouse press occurs outside of it
        if (
            self.control_panel.isVisible()
            and event.type() == QtCore.QEvent.MouseButtonPress
        ):
            
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

def check_single_instance():
    """Check if another instance is already running"""
    lock_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), LOCK_FILE)
    
    if os.path.exists(lock_file_path):
        try:
            # Try to read the PID from the lock file
            with open(lock_file_path, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if the process is still running (Windows)
            try:
                import psutil
                if psutil.pid_exists(pid):
                    return False  # Another instance is running
            except ImportError:
                # Fallback method for Windows without psutil
                try:
                    os.kill(pid, 0)
                    return False  # Process exists
                except OSError:
                    pass  # Process doesn't exist
        except (ValueError, IOError):
            pass  # Invalid lock file
    
    # Create lock file with current PID
    try:
        with open(lock_file_path, 'w') as f:
            f.write(str(os.getpid()))
        
        # Register cleanup function
        def cleanup_lock():
            try:
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
            except OSError:
                pass
        
        atexit.register(cleanup_lock)
        return True  # We're the first instance
    except IOError:
        return True  # Assume we can run if we can't create lock file

def main():
    # Check for single instance before creating QApplication
    if not check_single_instance():
        print("VMControl is already running!")
        # Try to show a message box if possible
        try:
            temp_app = QtWidgets.QApplication(sys.argv)
            QtWidgets.QMessageBox.warning(
                None, 
                "VMControl", 
                "VMControl is already running!\n\nCheck your system tray for the existing instance.",
                QtWidgets.QMessageBox.Ok
            )
        except:
            pass
        sys.exit(1)
    
    app = SingleInstanceApp(sys.argv)
    
    # Double-check with Qt-based method
    if app.is_running:
        print("VMControl is already running!")
        try:
            QtWidgets.QMessageBox.warning(
                None, 
                "VMControl", 
                "VMControl is already running!\n\nCheck your system tray for the existing instance.",
                QtWidgets.QMessageBox.Ok
            )
        except:
            pass
        sys.exit(1)
    
    try:
        with api("potato") as vm:
            tray = TrayApp(ICON_PATH, vm)
            tray.show()
            
            sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting VMControl: {e}")
        try:
            QtWidgets.QMessageBox.critical(
                None,
                "VMControl Error", 
                f"Failed to start VMControl:\n\n{e}\n\nMake sure Voicemeeter Potato is running.",
                QtWidgets.QMessageBox.Ok
            )
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
