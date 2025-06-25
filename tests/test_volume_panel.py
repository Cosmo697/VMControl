import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from widgets.volume_panel import VolumePanel
from PyQt5 import QtWidgets

class DummyStrip:
    def __init__(self, gain):
        self.gain = gain

class DummyVM:
    def __init__(self):
        self.strip = [DummyStrip(-10), DummyStrip(-20), DummyStrip(-30)]

class TestVolumePanel(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.vm = DummyVM()
        self.panel = VolumePanel(self.vm)

    def test_slider_count(self):
        # Should have 3 sliders for the 3 virtual inputs
        self.assertEqual(len(self.panel.sliders), 3)

    def test_update_sliders(self):
        for i, strip in enumerate(self.vm.strip):
            strip.gain = -5 * (i+1)
        self.panel.update_sliders()
        for i, slider in enumerate(self.panel.sliders):
            self.assertEqual(slider.value(), int(self.vm.strip[i].gain))

    def test_extended_range(self):
        # Test that sliders support the extended range (-60 to +12dB)
        for slider in self.panel.sliders:
            self.assertEqual(slider.minimum(), -60)
            self.assertEqual(slider.maximum(), 12)

if __name__ == '__main__':
    unittest.main()
