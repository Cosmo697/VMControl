from PyQt5 import QtWidgets, QtCore

class RoutingPanel(QtWidgets.QWidget):
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.strip = self.vm.strip[0]
        self.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setFixedSize(480, 60)
        layout = QtWidgets.QHBoxLayout()
        self.buttons = {}

        outputs = ["A1", "A2", "A3", "A4", "A5", "B1", "B2", "B3"]
        for label in outputs:
            btn = QtWidgets.QPushButton(label)
            btn.setCheckable(True)
            btn.setChecked(getattr(self.strip, label))
            btn.clicked.connect(lambda _, l=label: self._toggle_output(l))
            layout.addWidget(btn)
            self.buttons[label] = btn

        self.setLayout(layout)

    def _toggle_output(self, label):
        current = getattr(self.strip, label)
        setattr(self.strip, label, not current)
        self.buttons[label].setChecked(not current)
