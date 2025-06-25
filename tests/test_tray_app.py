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

    def test_controls_panel_toggle(self):
        self.tray.control_panel.isVisible = MagicMock(return_value=False)
        self.tray.control_panel.show = MagicMock()
        self.tray.control_panel.update_controls = MagicMock()
        self.tray._position_panel = MagicMock()
        self.tray.toggle_controls()
        self.tray.control_panel.show.assert_called_once()
        self.tray.control_panel.update_controls.assert_called_once()

    def test_menu_actions(self):
        # Check that the menu actions are present
        actions = [a.text() for a in self.tray.contextMenu().actions() if a.text()]
        expected_actions = ['Show Controls', 'Exit']
        for action in expected_actions:
            self.assertIn(action, actions)

if __name__ == '__main__':
    unittest.main()

if __name__ == '__main__':
    unittest.main()
