import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from widgets.preset_manager import PresetManager
from widgets.constants import STRIP_INDICES

class DummyStrip:
    def __init__(self):
        self.gain = 0
        self.mute = False
        for label in ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]:
            setattr(self, label, False)

class DummyVM:
    def __init__(self):
        self.strip = [DummyStrip() for _ in range(max(STRIP_INDICES) + 1)]


def test_save_and_load_preset(tmp_path):
    vm = DummyVM()
    vm.strip[STRIP_INDICES[0]].gain = -5
    vm.strip[STRIP_INDICES[0]].mute = True
    vm.strip[STRIP_INDICES[0]].A1 = True

    file_path = tmp_path / "preset.json"
    PresetManager.save_preset(vm, file_path)

    # modify values so we know load works
    vm.strip[STRIP_INDICES[0]].gain = 0
    vm.strip[STRIP_INDICES[0]].mute = False
    vm.strip[STRIP_INDICES[0]].A1 = False

    PresetManager.load_preset(vm, file_path)

    assert vm.strip[STRIP_INDICES[0]].gain == -5
    assert vm.strip[STRIP_INDICES[0]].mute is True
    assert vm.strip[STRIP_INDICES[0]].A1 is True
