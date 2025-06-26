from PyQt5 import QtWidgets, QtCore, QtGui
from .constants import VU_UPDATE_INTERVAL_MS

class VolumePanel(QtWidgets.QWidget):
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setFixedSize(500, 350)
        
        main_layout = QtWidgets.QVBoxLayout()
        
        # Title
        title = QtWidgets.QLabel("Volume Control - Virtual Inputs")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin: 5px;")
        main_layout.addWidget(title)
        
        # Volume controls layout
        volume_layout = QtWidgets.QHBoxLayout()
        self.sliders = []
        self.vu_meters = []
        self.strip_names = ["Voicemeeter Input", "Voicemeeter AUX", "VAIO3"]
        
        for i, strip_name in enumerate(self.strip_names):
            # Create vertical layout for each strip
            strip_layout = QtWidgets.QVBoxLayout()
            
            # Add strip label
            label = QtWidgets.QLabel(strip_name)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setWordWrap(True)
            label.setStyleSheet("font-weight: bold; font-size: 10px;")
            strip_layout.addWidget(label)
            
            # Create VU meter
            vu_meter = VUMeter()
            vu_meter.setFixedSize(20, 150)
            
            # Create slider with extended range to +12dB
            slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
            slider.setMinimum(-60)
            slider.setMaximum(12)
            slider.setTickInterval(6)
            slider.setSingleStep(1)
            
            try:
                current_gain = int(self.vm.strip[i].gain)
            except (IndexError, AttributeError):
                current_gain = 0
                
            slider.setValue(current_gain)
            slider.setToolTip(f"{strip_name}: {current_gain}dB")
            slider.valueChanged.connect(lambda val, idx=i: self._update_gain(idx, val))
            
            # Double-click to reset to 0dB
            slider.mouseDoubleClickEvent = lambda event, idx=i: self._reset_to_zero(idx)
            
            # Horizontal layout for VU meter and slider
            controls_layout = QtWidgets.QHBoxLayout()
            controls_layout.addWidget(vu_meter)
            controls_layout.addWidget(slider)
            strip_layout.addLayout(controls_layout)
            
            # Add dB value label
            db_label = QtWidgets.QLabel(f"{current_gain}dB")
            db_label.setAlignment(QtCore.Qt.AlignCenter)
            db_label.setObjectName(f"db_label_{i}")
            strip_layout.addWidget(db_label)
            
            volume_layout.addLayout(strip_layout)
            self.sliders.append(slider)
            self.vu_meters.append(vu_meter)
        
        main_layout.addLayout(volume_layout)
        self.setLayout(main_layout)

        # Use a QTimer for periodic VU updates instead of a thread
        self.vu_timer = QtCore.QTimer(self)
        self.vu_timer.timeout.connect(self._update_vu_meters)
        self.vu_timer.start(VU_UPDATE_INTERVAL_MS)

    def _reset_to_zero(self, idx):
        """Reset slider to 0dB on double-click"""
        self.sliders[idx].setValue(0)
        self._update_gain(idx, 0)

    def _update_gain(self, idx, val):
        """Update gain and refresh the dB label"""
        try:
            if idx < len(self.vm.strip):
                setattr(self.vm.strip[idx], "gain", float(val))
        except (IndexError, AttributeError):
            pass
            
        db_label = self.findChild(QtWidgets.QLabel, f"db_label_{idx}")
        if db_label:
            db_label.setText(f"{val}dB")
        self.sliders[idx].setToolTip(f"{self.strip_names[idx]}: {val}dB")

    def _update_vu_meters(self):
        """Update VU meters with current levels"""
        for i, vu_meter in enumerate(self.vu_meters):
            if i < len(self.vm.strip):
                try:
                    level = getattr(self.vm.strip[i], 'level', [0, 0])
                    if isinstance(level, (list, tuple)) and len(level) > 0:
                        db_level = level[0] if level[0] > -60 else -60
                    else:
                        db_level = -60
                except Exception:
                    db_level = -60
                vu_meter.update_level(db_level)

    def update_sliders(self):
        for i, slider in enumerate(self.sliders):
            try:
                if i < len(self.vm.strip):
                    current_gain = int(self.vm.strip[i].gain)
                    slider.setValue(current_gain)
                    db_label = self.findChild(QtWidgets.QLabel, f"db_label_{i}")
                    if db_label:
                        db_label.setText(f"{current_gain}dB")
                    slider.setToolTip(f"{self.strip_names[i]}: {current_gain}dB")
            except (IndexError, AttributeError):
                pass


class VUMeter(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.level = -60  # dB level
        self.setMinimumSize(20, 150)
        
    def update_level(self, db_level):
        """Update the VU meter level"""
        self.level = max(-60, min(12, db_level))
        self.update()
        
    def paintEvent(self, event):
        """Draw the VU meter"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Background
        painter.fillRect(self.rect(), QtGui.QColor(30, 30, 30))
        
        # Calculate meter height
        meter_height = self.height() - 10
        meter_width = self.width() - 4
        
        # Convert dB to pixel position (0dB at top, -60dB at bottom)
        level_ratio = (self.level + 60) / 72  # Range: -60dB to +12dB
        level_height = int(level_ratio * meter_height)
        
        # Draw segments
        segment_height = 3
        segment_gap = 1
        segments_per_meter = meter_height // (segment_height + segment_gap)
        
        for i in range(segments_per_meter):
            y_pos = self.height() - 5 - (i * (segment_height + segment_gap))
            
            if i * (segment_height + segment_gap) < level_height:
                # Determine color based on dB level
                segment_db = -60 + (i / segments_per_meter) * 72
                if segment_db > 0:
                    color = QtGui.QColor(255, 0, 0)  # Red for > 0dB
                elif segment_db > -12:
                    color = QtGui.QColor(255, 255, 0)  # Yellow for -12dB to 0dB
                else:
                    color = QtGui.QColor(0, 255, 0)  # Green for < -12dB
            else:
                color = QtGui.QColor(60, 60, 60)  # Dark gray for inactive
                
            painter.fillRect(2, y_pos, meter_width, segment_height, color)
