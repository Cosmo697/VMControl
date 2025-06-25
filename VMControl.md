# Voicemeeter System Tray Utility

## Feature Blueprint

---

### App Positioning & Interface

- Resides in the **Windows System Tray**
- Supports a **custom icon** (e.g. N.C. branding or Voicemeeter-styled)
- **Clicking the icon** opens a sleek popup window near the tray:
  - Displays **5 vertical sliders** for A1–A5
  - Optionally auto-hides the window when it loses focus

---

### Volume Control Panel (A1–A5 Outputs)

- Individual vertical sliders for:
  - A1
  - A2
  - A3
  - A4
  - A5
- Features:
  - Clean visual design
  - Real-time synchronization with Voicemeeter
  - Display of dB values (e.g. −6.2 dB)

---

### Output Routing Toggle

- For each input strip (e.g., Voicemeeter Input, AUX, VAIO3):
  - Toggle output routing to:
    - A1–A5 (hardware outputs)
    - B1–B3 (virtual outputs)
- Visual indicators:
  - Clearly marked active/inactive states

---

### Strip Controls (Per Input Strip)

- Quick toggles for:
  - **M.C.** (Mono Channel)
  - **Solo**
  - **Mute**
- Applies to each active input strip
- Toggle states reflect the live status in Voicemeeter

---

### Restore Audio Defaults Button

- One-click action to restore preferred Windows default devices:
  - **Playback Default**: Voicemeeter Input
  - **Communications Default**: Voicemeeter AUX Input
- Accessible via tray menu or popup window
- Methods:
  - Uses Windows Registry or app-level configuration to remember defaults

---

### App Settings (Tray Menu)

- Run at Startup toggle
- Auto-hide popup after inactivity
- Dark / Light theme toggle
- Option to remember last session's gain levels

---

### Installer & Startup Integration

- Packaged with `pyinstaller`
- Optional installer via **Inno Setup** or **NSIS**:
  - Adds Start Menu shortcut
  - Adds to Windows Startup folder
- Launches minimized to tray and starts with system boot

---

### Additional Enhancements (Optional)

- Combined matrix panel for strip-to-output routing
- Save/load system for routing presets and gain configurations

---

### Clarifications

1. Popup controls appear directly above the system tray icon
2. Restoring audio defaults is performed manually via a dedicated button

---

### Working Name Ideas

- VMControl

