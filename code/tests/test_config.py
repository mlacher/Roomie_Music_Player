import pytest
import json
from unittest.mock import mock_open, patch
import sys

sys.path.append('/home/maxi/PythonCodes/code')

from config import load_config

def test_load_config_valid_file():
    # Beispielinhalt der config.json
    mock_config = {
        "spotify": {
            "client_id": "test_client_id",
            "client_secret": "test_client_secret"
        }
    }
    # JSON-String erzeugen
    mock_data = json.dumps(mock_config)

    # `open()` mocken
    with patch("builtins.open", mock_open(read_data=mock_data)):
        config = load_config()
        assert config == mock_config

def test_load_config_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            load_config()

def test_load_config_invalid_json():
    # Ungültiges JSON
    invalid_json = "{ invalid json }"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with pytest.raises(json.JSONDecodeError):
            load_config()
