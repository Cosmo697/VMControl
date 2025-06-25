import subprocess
import sys
import win32com.client
from PyQt5.QtWidgets import QMessageBox

def _set_default_device(device_name, role):
    # role: 0 = eConsole, 1 = eMultimedia, 2 = eCommunications
    try:
        policy_config = win32com.client.Dispatch('PolicyConfigClient.PolicyConfigClient')
        device_enum = win32com.client.Dispatch('MMDeviceEnumerator')
        devices = device_enum.EnumAudioEndpoints(0, 1)  # 0: eRender, 1: DEVICE_STATE_ACTIVE
        found = False
        for i in range(devices.Count):
            device = devices.Item(i)
            if device.FriendlyName.startswith(device_name):
                policy_config.SetDefaultEndpoint(device.Id, role)
                found = True
        return found
    except Exception as e:
        QMessageBox.warning(None, "Audio Restore Error", f"Failed to set default device: {e}")
        return False

def restore_default_audio():
    """Restore default playback and communications devices using Windows API."""
    playback = _set_default_device("Voicemeeter Input (VB-Audio Voicemeeter VAIO)", 0)
    comm = _set_default_device("Voicemeeter AUX Input (VB-Audio Voicemeeter AUX VAIO)", 2)
    if playback and comm:
        QMessageBox.information(None, "Audio Restore", "Default audio devices restored successfully.")
    else:
        QMessageBox.warning(None, "Audio Restore Error", "Failed to restore default audio devices.\nCheck device names and permissions.")
