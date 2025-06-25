# VMControl - Voicemeeter System Tray Utility

A lightweight Windows system tray application for controlling Voicemeeter audio routing and volume levels.

## Features

- **System Tray Integration**: Resides in Windows system tray with custom icon
- **Unified Control Panel**: Combined interface with routing matrix above volume controls
- **Enhanced Volume Control**: 
  - 3 vertical sliders for virtual inputs (Voicemeeter Input, AUX, VAIO3)
  - Extended range (-60dB to +12dB) for full Voicemeeter compatibility
  - Real-time VU meters with color-coded level indicators
  - Double-click sliders to reset to 0dB
  - Live dB value display and tooltips
- **Improved Routing Matrix**: 
  - Clean vertical button layout for better visibility
  - Controls all 3 virtual inputs to A1-A5 (hardware) and B1-B3 (virtual) outputs
  - Color-coded buttons with visual feedback for active/inactive states
- **Real-time Sync**: Live synchronization with Voicemeeter settings

## Requirements

- Windows 10/11
- Python 3.7+
- Voicemeeter (Potato edition recommended)
- PyQt5
- voicemeeterlib

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

### System Tray
- Click the tray icon to open the unified control panel
- Right-click for context menu with Show Controls and Exit options

### Unified Control Panel
- **Routing Matrix (Top)**: Toggle output routing for all 3 virtual inputs
  - Vertically aligned buttons for better visibility and organization
  - Each virtual input (Voicemeeter Input, AUX, VAIO3) has its own column
  - Toggle routing to A1-A5 (hardware outputs) and B1-B3 (virtual outputs)
  
- **Volume Control (Bottom)**: 
  - 3 volume sliders for virtual inputs with extended -60dB to +12dB range
  - Real-time VU meters showing current audio levels with color coding:
    - Green: Below -12dB (safe levels)
    - Yellow: -12dB to 0dB (caution levels)  
    - Red: Above 0dB (clipping risk)
  - Double-click any slider to instantly reset to 0dB
  - Live dB value display below each slider

## Project Structure

```
VMControl/
├── main.py                 # Main application entry point
├── tray_icon.ico          # System tray icon
├── widgets/
│   ├── combined_panel.py  # Unified control panel with routing and volume
│   ├── volume_panel.py    # Volume control with VU meters and double-click reset
│   └── routing_panel.py   # Matrix routing panel with vertical layout
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

- VU meters update in real-time but require Voicemeeter to be running
- Volume sliders sync with Voicemeeter on panel open
- Routing panel requires Voicemeeter to be running for proper functionality
- Double-click reset feature works on volume sliders only

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
