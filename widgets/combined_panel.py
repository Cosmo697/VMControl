import math
from PyQt5 import QtWidgets, QtCore, QtGui
from .volume_panel import VolumePanel
from .routing_panel import RoutingPanel

class CombinedControlPanel(QtWidgets.QWidget):
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setFixedSize(520, 650)
        self.setAttribute(QtCore.Qt.WA_ShowWithoutActivating)  # Don't steal focus
        
        # Set up auto-hide timer for mouse leave detection
        self.hide_timer = QtCore.QTimer()
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide)
        
        # Install event filter to track mouse events
        self.installEventFilter(self)
        

        
        # Apply dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: Segoe UI;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                border: 2px solid #555555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #ffffff;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #ffffff;
            }
            QFrame[frameShape="4"] {
                color: #555555;
            }
        """)
        
        main_layout = QtWidgets.QVBoxLayout()
        
        # Main title
        main_title = QtWidgets.QLabel("VMControl - Virtual Inputs")
        main_title.setAlignment(QtCore.Qt.AlignCenter)
        main_title.setStyleSheet("font-weight: bold; font-size: 16px; margin: 10px; color: #ffffff;")
        main_layout.addWidget(main_title)
        
        # Create routing panel (above)
        self.routing_panel = RoutingPanelEmbedded(vm)
        main_layout.addWidget(self.routing_panel)
        
        # Add separator
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.HLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator.setStyleSheet("color: #555555;")
        main_layout.addWidget(separator)
        
        # Create volume panel (below)
        self.volume_panel = VolumePanelEmbedded(vm)
        main_layout.addWidget(self.volume_panel)
        
        self.setLayout(main_layout)
        
    def update_controls(self):
        """Update both routing and volume controls"""
        self.routing_panel.update_routing_states()
        self.volume_panel.update_sliders()
        
    def focusOutEvent(self, event):
        """Hide panel when it loses focus"""
        self.hide()
        super().focusOutEvent(event)
        
    def eventFilter(self, obj, event):
        """Event filter to detect when mouse leaves the window area"""
        if event.type() == 11:  # Leave event
            # Start timer to hide after 500ms if mouse doesn't return
            self.hide_timer.start(500)
        elif event.type() == 10:  # Enter event
            # Cancel hide timer if mouse returns
            self.hide_timer.stop()
        return super().eventFilter(obj, event)
        
    def showEvent(self, event):
        """Reset auto-hide timer when window is shown"""
        self.hide_timer.stop()
        super().showEvent(event)


class RoutingPanelEmbedded(QtWidgets.QWidget):
    """Embedded routing panel without window decorations"""
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        
        main_layout = QtWidgets.QVBoxLayout()
        
        # Title
        title = QtWidgets.QLabel("Output Routing")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin: 5px; color: #ffffff;")
        main_layout.addWidget(title)
        
        # Create routing matrix with vertical alignment
        routing_layout = QtWidgets.QHBoxLayout()
        self.buttons = {}
        strip_names = ["Voicemeeter Input", "Voicemeeter AUX", "VAIO3"]
        outputs = ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]
        
        # Use inputs 5, 6, 7 (indices for inputs 6, 7, 8 in Voicemeeter Potato)
        strip_indices = [5, 6, 7]
        
        for i, (strip_name, strip_idx) in enumerate(zip(strip_names, strip_indices)):
            # Create group box for each virtual input
            group_box = QtWidgets.QGroupBox(strip_name)
            group_box.setFixedWidth(150)
            group_layout = QtWidgets.QVBoxLayout()
            
            # Add buttons for each output in vertical arrangement
            strip_buttons = {}
            for output in outputs:
                btn = QtWidgets.QPushButton(output)
                btn.setCheckable(True)
                btn.setFixedSize(120, 25)
                
                # Set initial state from Voicemeeter (using correct strip index)
                try:
                    current_state = getattr(self.vm.strip[strip_idx], output)
                    btn.setChecked(current_state)
                except (IndexError, AttributeError):
                    btn.setChecked(False)
                
                # Style the button for dark mode
                self._style_button(btn)
                
                # Connect signal with correct strip index
                btn.clicked.connect(lambda checked, strip=strip_idx, out=output: self._toggle_output(strip, out, checked))
                
                group_layout.addWidget(btn)
                strip_buttons[output] = btn
            
            self.buttons[strip_idx] = strip_buttons
            group_box.setLayout(group_layout)
            routing_layout.addWidget(group_box)
        
        main_layout.addLayout(routing_layout)
        self.setLayout(main_layout)

    def _style_button(self, btn):
        """Apply dark mode styling to routing buttons"""
        style = """
        QPushButton {
            border: 2px solid #666666;
            border-radius: 4px;
            background-color: #404040;
            color: #ffffff;
            font-weight: bold;
            font-size: 11px;
            padding: 2px;
        }
        QPushButton:checked {
            background-color: #4CAF50;
            color: #ffffff;
            border-color: #45a049;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:checked:hover {
            background-color: #45a049;
        }
        """
        btn.setStyleSheet(style)

    def _toggle_output(self, strip_idx, output, checked):
        """Toggle output routing for specified strip and output"""
        try:
            if strip_idx < len(self.vm.strip):
                setattr(self.vm.strip[strip_idx], output, checked)
                self.buttons[strip_idx][output].setChecked(checked)
        except (IndexError, AttributeError) as e:
            print(f"Error toggling {output} for strip {strip_idx}: {e}")

    def update_routing_states(self):
        """Update all button states from current Voicemeeter settings"""
        strip_indices = [5, 6, 7]  # Inputs 6, 7, 8
        for strip_idx in strip_indices:
            if strip_idx in self.buttons:
                for output in ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]:
                    try:
                        current_state = getattr(self.vm.strip[strip_idx], output)
                        self.buttons[strip_idx][output].setChecked(current_state)
                    except (IndexError, AttributeError, KeyError):
                        pass


class VolumePanelEmbedded(QtWidgets.QWidget):
    """Embedded volume panel without window decorations"""
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.resetting_strips = set()  # Track which strips are being reset
        
        main_layout = QtWidgets.QVBoxLayout()
        
        # Title
        title = QtWidgets.QLabel("Volume Control")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin: 5px; color: #ffffff;")
        main_layout.addWidget(title)
        
        # Volume controls layout
        volume_layout = QtWidgets.QHBoxLayout()
        self.sliders = []
        self.vu_meters = []
        self.strip_names = ["Voicemeeter Input", "Voicemeeter AUX", "VAIO3"]
        
        # Use inputs 5, 6, 7 (indices for inputs 6, 7, 8 in Voicemeeter Potato)
        strip_indices = [5, 6, 7]
        
        for i, (strip_name, strip_idx) in enumerate(zip(self.strip_names, strip_indices)):
            # Create vertical layout for each strip
            strip_layout = QtWidgets.QVBoxLayout()
            
            # Add strip label
            label = QtWidgets.QLabel(strip_name)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setWordWrap(True)
            label.setStyleSheet("font-weight: bold; font-size: 10px; color: #ffffff;")
            strip_layout.addWidget(label)
            
            # Create VU meter
            vu_meter = VUMeter()
            vu_meter.setFixedSize(20, 150)
            
            try:
                current_gain = int(self.vm.strip[strip_idx].gain)
            except (IndexError, AttributeError):
                current_gain = 0
            
            # Create custom slider that handles double-click
            custom_slider = DoubleClickSlider(QtCore.Qt.Vertical)
            custom_slider.setMinimum(-60)
            custom_slider.setMaximum(12)
            custom_slider.setValue(current_gain)
            custom_slider.valueChanged.connect(lambda val, idx=strip_idx: self._update_gain(idx, val))
            custom_slider.doubleClicked.connect(lambda idx=strip_idx: self._reset_to_zero(idx))
            
            # Apply dark mode styling to slider
            custom_slider.setStyleSheet("""
                QSlider::groove:vertical {
                    background: #404040;
                    width: 8px;
                    border-radius: 4px;
                }
                QSlider::handle:vertical {
                    background: #4CAF50;
                    border: 1px solid #45a049;
                    height: 18px;
                    margin: 0 -5px;
                    border-radius: 9px;
                }
                QSlider::handle:vertical:hover {
                    background: #45a049;
                }
            """)
            
            # Horizontal layout for VU meter and slider
            controls_layout = QtWidgets.QHBoxLayout()
            controls_layout.addWidget(vu_meter)
            controls_layout.addWidget(custom_slider)
            strip_layout.addLayout(controls_layout)
            
            # Add dB value label
            db_label = QtWidgets.QLabel(f"{current_gain}dB")
            db_label.setAlignment(QtCore.Qt.AlignCenter)
            db_label.setObjectName(f"db_label_{strip_idx}")
            db_label.setStyleSheet("color: #ffffff; font-weight: bold;")
            strip_layout.addWidget(db_label)
            
            volume_layout.addLayout(strip_layout)
            self.sliders.append(custom_slider)
            self.vu_meters.append(vu_meter)
        
        main_layout.addLayout(volume_layout)
        self.setLayout(main_layout)
        
        # Set up timer for VU meter updates
        self.vu_timer = QtCore.QTimer()
        self.vu_timer.timeout.connect(self._update_vu_meters)
        self.vu_timer.start(50)  # Update every 50ms for smooth animation

    def _reset_to_zero(self, strip_idx):
        """Reset slider to 0dB on double-click"""
        # Find which slider corresponds to this strip index
        strip_indices = [5, 6, 7]
        if strip_idx in strip_indices:
            slider_index = strip_indices.index(strip_idx)
            
            # Mark this strip as being reset to prevent interference for longer
            self.resetting_strips.add(strip_idx)
            
            # Disconnect the slider signal to prevent any interference
            slider = self.sliders[slider_index]
            try:
                slider.valueChanged.disconnect()
            except TypeError:
                pass  # Signal wasn't connected
            
            # Force set Voicemeeter to 0dB multiple times with more persistence
            for attempt in range(5):
                try:
                    setattr(self.vm.strip[strip_idx], "gain", 0.0)
                    QtCore.QCoreApplication.processEvents()
                    # Verify it was set
                    actual = getattr(self.vm.strip[strip_idx], "gain")
                    if abs(actual) < 0.1:  # Close enough to 0
                        break
                except Exception as e:
                    pass
            
            # Update slider to 0
            slider.setValue(0)
            
            # Reconnect the signal
            slider.valueChanged.connect(lambda val, idx=strip_idx: self._update_gain(idx, val))
            
            # Update the dB label
            db_label = self.findChild(QtWidgets.QLabel, f"db_label_{strip_idx}")
            if db_label:
                db_label.setText("0dB")
            
            # Monitor and enforce the reset over a longer time period
            self._enforce_reset_value(strip_idx, 0, 0)
    
    def _enforce_reset_value(self, strip_idx, target_value, attempts=0):
        """Enforce the reset value by checking and correcting it multiple times"""
        max_attempts = 20  # Increased from 10 to 20 for more persistence
        if attempts >= max_attempts:
            self.resetting_strips.discard(strip_idx)
            return
        
        try:
            current_gain = getattr(self.vm.strip[strip_idx], "gain")
            if abs(current_gain - target_value) > 0.1:  # If not close to target
                # Force it back to target value
                setattr(self.vm.strip[strip_idx], "gain", float(target_value))
                
                # Also update the slider and label to match
                strip_indices = [5, 6, 7]
                if strip_idx in strip_indices:
                    slider_index = strip_indices.index(strip_idx)
                    slider = self.sliders[slider_index]
                    
                    # Temporarily disconnect, update, and reconnect
                    try:
                        slider.valueChanged.disconnect()
                    except TypeError:
                        pass
                    
                    slider.setValue(target_value)
                    slider.valueChanged.connect(lambda val, idx=strip_idx: self._update_gain(idx, val))
                    
                    # Update label
                    db_label = self.findChild(QtWidgets.QLabel, f"db_label_{strip_idx}")
                    if db_label:
                        db_label.setText(f"{target_value}dB")
                
                # Schedule another check sooner for more aggressive correction
                QtCore.QTimer.singleShot(50, lambda: self._enforce_reset_value(strip_idx, target_value, attempts + 1))
            else:
                # Value is correct, but keep monitoring for a bit longer
                if attempts < 15:  # Continue monitoring for 15 more cycles
                    QtCore.QTimer.singleShot(100, lambda: self._enforce_reset_value(strip_idx, target_value, attempts + 1))
                else:
                    self.resetting_strips.discard(strip_idx)
        except Exception as e:
            self.resetting_strips.discard(strip_idx)
    


    def _update_gain(self, strip_idx, val):
        """Update gain and refresh the dB label"""
        try:
            if strip_idx < len(self.vm.strip):
                setattr(self.vm.strip[strip_idx], "gain", float(val))
        except (IndexError, AttributeError) as e:
            pass
            
        db_label = self.findChild(QtWidgets.QLabel, f"db_label_{strip_idx}")
        if db_label:
            db_label.setText(f"{val}dB")

    def update_sliders(self):
        strip_indices = [5, 6, 7]  # Inputs 6, 7, 8
        for i, strip_idx in enumerate(strip_indices):
            # Skip strips that are currently being reset
            if strip_idx in self.resetting_strips:
                continue
                
            try:
                if strip_idx < len(self.vm.strip):
                    current_gain = int(self.vm.strip[strip_idx].gain)
                    
                    # Only update the slider if there's a significant difference
                    # Block signals to prevent triggering value changes in Voicemeeter
                    current_slider_value = self.sliders[i].value()
                    if abs(current_slider_value - current_gain) > 1:  # More than 1dB difference
                        self.sliders[i].blockSignals(True)
                        self.sliders[i].setValue(current_gain)
                        self.sliders[i].blockSignals(False)
                        
                    # Always update the label to show current Voicemeeter value
                    db_label = self.findChild(QtWidgets.QLabel, f"db_label_{strip_idx}")
                    if db_label:
                        db_label.setText(f"{current_gain}dB")
            except (IndexError, AttributeError):
                pass

    def _update_vu_meters(self):
        """Update VU meters with real audio levels from Voicemeeter"""
        strip_indices = [5, 6, 7]  # Inputs 6, 7, 8
        for i, strip_idx in enumerate(strip_indices):
            try:
                if strip_idx < len(self.vm.strip):
                    # Get audio levels using the correct voicemeeterlib API
                    # Get postmute levels (after mute/gain but before fader)
                    levels = self.vm.strip[strip_idx].levels.postmute
                    
                    # levels is a tuple, get the left channel (index 0)
                    if levels and len(levels) > 0:
                        level_db = levels[0]  # Already in dB
                        # Clamp to our expected range
                        level_db = max(-60, min(12, level_db))
                    else:
                        level_db = -60  # No signal
                    
                    # Update the corresponding VU meter
                    if i < len(self.vu_meters):
                        self.vu_meters[i].update_level(level_db)
            except (IndexError, AttributeError, TypeError, ValueError):
                # If we can't get the level, set to minimum
                if i < len(self.vu_meters):
                    self.vu_meters[i].update_level(-60)

class DoubleClickSlider(QtWidgets.QSlider):
    """Custom slider that emits doubleClicked signal"""
    doubleClicked = QtCore.pyqtSignal()
    
    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        super().mouseDoubleClickEvent(event)


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
        """Draw the VU meter with dark theme"""
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        
        # Dark background
        painter.fillRect(self.rect(), QtGui.QColor(20, 20, 20))
        
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
                color = QtGui.QColor(40, 40, 40)  # Dark gray for inactive
                
            painter.fillRect(2, y_pos, meter_width, segment_height, color)
