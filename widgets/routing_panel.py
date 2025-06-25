from PyQt5 import QtWidgets, QtCore

class RoutingPanel(QtWidgets.QWidget):
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setFixedSize(500, 280)
        
        main_layout = QtWidgets.QVBoxLayout()
        
        # Title
        title = QtWidgets.QLabel("Output Routing - Virtual Inputs")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; margin: 5px;")
        main_layout.addWidget(title)
        
        # Create routing matrix with vertical alignment
        routing_layout = QtWidgets.QHBoxLayout()
        self.buttons = {}
        strip_names = ["Voicemeeter Input", "Voicemeeter AUX", "VAIO3"]
        outputs = ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]
        
        for i, strip_name in enumerate(strip_names):
            # Create group box for each virtual input
            group_box = QtWidgets.QGroupBox(strip_name)
            group_box.setFixedWidth(150)
            group_layout = QtWidgets.QVBoxLayout()  # Changed to vertical layout
            
            # Add buttons for each output in vertical arrangement
            strip_buttons = {}
            for output in outputs:
                btn = QtWidgets.QPushButton(output)
                btn.setCheckable(True)
                btn.setFixedSize(120, 25)  # Fixed size for better visibility
                
                # Set initial state from Voicemeeter
                try:
                    current_state = getattr(self.vm.strip[i], output)
                    btn.setChecked(current_state)
                except (IndexError, AttributeError):
                    btn.setChecked(False)
                
                # Style the button
                self._style_button(btn)
                
                # Connect signal
                btn.clicked.connect(lambda checked, strip=i, out=output: self._toggle_output(strip, out, checked))
                
                group_layout.addWidget(btn)
                strip_buttons[output] = btn
            
            self.buttons[i] = strip_buttons
            group_box.setLayout(group_layout)
            routing_layout.addWidget(group_box)
        
        main_layout.addLayout(routing_layout)
        self.setLayout(main_layout)

    def _style_button(self, btn):
        """Apply custom styling to routing buttons"""
        style = """
        QPushButton {
            border: 2px solid #555;
            border-radius: 4px;
            background-color: #f0f0f0;
            color: black;
            font-weight: bold;
            font-size: 11px;
            padding: 2px;
        }
        QPushButton:checked {
            background-color: #4CAF50;
            color: white;
            border-color: #45a049;
        }
        QPushButton:hover {
            background-color: #e0e0e0;
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
                # Update button visual state
                self.buttons[strip_idx][output].setChecked(checked)
        except (IndexError, AttributeError) as e:
            print(f"Error toggling {output} for strip {strip_idx}: {e}")

    def update_routing_states(self):
        """Update all button states from current Voicemeeter settings"""
        for strip_idx in range(min(3, len(self.vm.strip))):
            for output in ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]:
                try:
                    current_state = getattr(self.vm.strip[strip_idx], output)
                    self.buttons[strip_idx][output].setChecked(current_state)
                except (IndexError, AttributeError, KeyError):
                    pass
