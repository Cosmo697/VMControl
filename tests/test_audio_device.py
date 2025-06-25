import unittest
from unittest.mock import patch
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import audio_device

class TestAudioDevice(unittest.TestCase):
    @patch('utils.audio_device._set_default_device')
    @patch('utils.audio_device.QMessageBox')
    def test_restore_default_audio_success(self, mock_msgbox, mock_set):
        mock_set.side_effect = [True, True]
        audio_device.restore_default_audio()
        mock_msgbox.information.assert_called_once()
        mock_msgbox.warning.assert_not_called()

    @patch('utils.audio_device._set_default_device')
    @patch('utils.audio_device.QMessageBox')
    def test_restore_default_audio_failure(self, mock_msgbox, mock_set):
        mock_set.side_effect = [True, False]
        audio_device.restore_default_audio()
        mock_msgbox.warning.assert_called_once()
        mock_msgbox.information.assert_not_called()

if __name__ == '__main__':
    unittest.main()
