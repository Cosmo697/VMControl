import json
from pathlib import Path
from .constants import STRIP_INDICES


class PresetManager:
    """Utility class to save and load Voicemeeter presets."""

    @staticmethod
    def save_preset(vm, file_path):
        """Save current strip settings to ``file_path``."""
        data = {}
        for idx in STRIP_INDICES:
            if idx >= len(vm.strip):
                continue
            strip = vm.strip[idx]
            routing = {out: bool(getattr(strip, out, False))
                       for out in ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]}
            data[idx] = {
                "gain": getattr(strip, "gain", 0),
                "mute": getattr(strip, "mute", False),
                "routing": routing,
            }
        path = Path(file_path)
        with path.open("w") as fh:
            json.dump(data, fh)

    @staticmethod
    def load_preset(vm, file_path):
        """Load strip settings from ``file_path``."""
        path = Path(file_path)
        try:
            with path.open() as fh:
                data = json.load(fh)
        except (OSError, json.JSONDecodeError):
            return

        for idx_str, strip_data in data.items():
            idx = int(idx_str)
            if idx >= len(vm.strip):
                continue
            strip = vm.strip[idx]
            setattr(strip, "gain", float(strip_data.get("gain", 0)))
            setattr(strip, "mute", bool(strip_data.get("mute", False)))
            routing = strip_data.get("routing", {})
            for out, state in routing.items():
                setattr(strip, out, bool(state))

