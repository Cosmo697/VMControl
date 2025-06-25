import unittest
from unittest.mock import MagicMock
from widgets.volume_panel import VolumePanel
from PyQt5 import QtWidgets

class DummyBus:
    def __init__(self, gain):
        self.gain = gain

class DummyVM:
    def __init__(self):
        self.bus = [DummyBus(-10), DummyBus(-20), DummyBus(-30), DummyBus(-40), DummyBus(-50)]

class TestVolumePanel(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
        self.vm = DummyVM()
        self.panel = VolumePanel(self.vm)

    def test_slider_count(self):
        self.assertEqual(len(self.panel.sliders), 5)

    def test_update_sliders(self):
        for i, bus in enumerate(self.vm.bus):
            bus.gain = -5 * (i+1)
        self.panel.update_sliders()
        for i, slider in enumerate(self.panel.sliders):
            self.assertEqual(slider.value(), int(self.vm.bus[i].gain))

if __name__ == '__main__':
    unittest.main()
