import unittest
from unittest.mock import MagicMock
from widgets.routing_panel import RoutingPanel
from PyQt5 import QtWidgets

class DummyStrip:
    def __init__(self):
        for label in ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]:
            setattr(self, label, False)

class DummyVM:
    def __init__(self):
        self.strip = [DummyStrip()]

class TestRoutingPanel(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.vm = DummyVM()
        self.panel = RoutingPanel(self.vm)

    def test_button_count(self):
        self.assertEqual(len(self.panel.buttons), 8)

    def test_toggle_output(self):
        for label in self.panel.buttons:
            self.panel._toggle_output(label)
            self.assertTrue(getattr(self.vm.strip[0], label))
            self.assertTrue(self.panel.buttons[label].isChecked())

if __name__ == '__main__':
    unittest.main()
