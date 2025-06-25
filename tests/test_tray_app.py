import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PyQt5 import QtWidgets

sys.modules['voicemeeterlib'] = MagicMock()
from main import TrayApp

class TestTrayApp(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.vm = MagicMock()
        self.tray = TrayApp('tray_icon.ico', self.vm)

    def test_volume_panel_toggle(self):
        self.tray.volume_panel.isVisible = MagicMock(return_value=False)
        self.tray.volume_panel.show = MagicMock()
        self.tray.volume_panel.update_sliders = MagicMock()
        self.tray._position_panel = MagicMock()
        self.tray.toggle_volume()
        self.tray.volume_panel.show.assert_called_once()
        self.tray.volume_panel.update_sliders.assert_called_once()

    def test_routing_panel_toggle(self):
        self.tray.routing_panel.isVisible = MagicMock(return_value=False)
        self.tray.routing_panel.show = MagicMock()
        self.tray._position_panel = MagicMock()
        self.tray.toggle_routing()
        self.tray.routing_panel.show.assert_called_once()

    def test_restore_default_audio_action(self):
        # Check that the menu action is present
        actions = [a.text() for a in self.tray.contextMenu().actions()]
        self.assertIn('Restore Default Audio Devices', actions)

if __name__ == '__main__':
    unittest.main()
