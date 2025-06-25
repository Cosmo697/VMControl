from PyQt5 import QtWidgets, QtCore

class VolumePanel(QtWidgets.QWidget):
    def __init__(self, vm):
        super().__init__()
        self.vm = vm
        self.setWindowFlags(
            QtCore.Qt.Tool |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.WindowStaysOnTopHint
        )
        self.setFixedSize(360, 200)
        layout = QtWidgets.QHBoxLayout()
        self.sliders = []

        for i in range(5):
            slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
            slider.setMinimum(-60)
            slider.setMaximum(0)
            slider.setTickInterval(6)
            slider.setSingleStep(1)
            slider.setToolTip(f"A{i+1}")
            slider.setValue(int(self.vm.bus[i].gain))
            slider.valueChanged.connect(
                lambda val, idx=i: setattr(self.vm.bus[idx], "gain", float(val))
            )
            layout.addWidget(slider)
            self.sliders.append(slider)

        self.setLayout(layout)

    def update_sliders(self):
        for i, slider in enumerate(self.sliders):
            slider.setValue(int(self.vm.bus[i].gain))
