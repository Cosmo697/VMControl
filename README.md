# VMControl - Voicemeeter System Tray Utility

A lightweight Windows system tray application for controlling Voicemeeter audio routing and volume levels.

## Features

- **System Tray Integration**: Resides in Windows system tray with custom icon
- **Volume Control**: 5 vertical sliders for A1-A5 hardware outputs with real-time sync
- **Output Routing**: Toggle routing for input strips to A1-A5 (hardware) and B1-B3 (virtual) outputs
- **Audio Device Management**: One-click restoration of Windows default audio devices
- **Modern UI**: Clean, responsive interface with popup panels

## Requirements

- Windows 10/11
- Python 3.7+
- Voicemeeter (Potato edition recommended)
- PyQt5
- voicemeeterlib
- pywin32

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/VMControl.git
cd VMControl
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Voicemeeter is installed and running

4. Run the application:
```bash
python main.py
```

## Usage

### System Tray
- Click the tray icon to open volume control panel
- Right-click for context menu with additional options

### Volume Control
- Adjust A1-A5 output levels using vertical sliders
- Real-time synchronization with Voicemeeter settings

### Routing Control
- Toggle output routing for input strips
- Visual indicators for active/inactive states

### Audio Device Restore
- One-click restoration of preferred Windows default devices:
  - Playback Default: Voicemeeter Input
  - Communications Default: Voicemeeter AUX Input

## Project Structure

```
VMControl/
├── main.py                 # Main application entry point
├── tray_icon.ico          # System tray icon
├── utils/
│   └── audio_device.py    # Windows audio device management
├── widgets/
│   ├── volume_panel.py    # Volume control panel
│   └── routing_panel.py   # Output routing panel
├── tests/                 # Unit tests
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Development

### Running Tests
```bash
python -m unittest discover -s tests
```

### Building Executable
```bash
pyinstaller --windowed --onefile --icon=tray_icon.ico main.py
```

## Known Issues

- Audio device restoration requires exact device name matching
- COM object registration may be required for some Windows configurations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Voicemeeter](https://vb-audio.com/Voicemeeter/) by VB-Audio
- [voicemeeterlib](https://github.com/onyx-and-iris/voicemeeter-api-python) for Python API
