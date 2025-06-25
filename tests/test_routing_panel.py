import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from widgets.routing_panel import RoutingPanel
from PyQt5 import QtWidgets

class DummyStrip:
    def __init__(self):
        for label in ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]:
            setattr(self, label, False)

class DummyVM:
    def __init__(self):
        self.strip = [DummyStrip(), DummyStrip(), DummyStrip()]

class TestRoutingPanel(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.vm = DummyVM()
        self.panel = RoutingPanel(self.vm)

    def test_button_count(self):
        # Should have 3 strips with 8 buttons each
        self.assertEqual(len(self.panel.buttons), 3)
        for strip_idx in self.panel.buttons:
            self.assertEqual(len(self.panel.buttons[strip_idx]), 8)

    def test_toggle_output(self):
        # Test toggling for first strip
        strip_idx = 0
        output = "A1"
        self.panel._toggle_output(strip_idx, output, True)
        self.assertTrue(getattr(self.vm.strip[strip_idx], output))
        self.assertTrue(self.panel.buttons[strip_idx][output].isChecked())

if __name__ == '__main__':
    unittest.main()
