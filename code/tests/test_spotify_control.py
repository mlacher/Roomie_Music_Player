import pytest
from unittest.mock import MagicMock
from config import load_config

import sys
sys.path.append('/home/maxi/PythonCodes/code')
from spotify_control import init_spotify, find_song_by_nfc, music_control, restart_raspotify
global sp

def test_restart_spotify():
    restart_raspotify()


def test_init_spotify():
    config = load_config()
    sp = init_spotify(config, "Maxis-Raspi")
    assert sp is not None


def get_available_devices(sp):
    devices = sp.devices()
    assert devices is not None
    assert len(devices['devices']) > 0
    return devices['devices']

def test_find_song_by_nfc():
    # Testdaten
    songs = [
        ("123ABC", "Song A"),
        ("456DEF", "Song B"),
        ("789GHI", "Song C")
    ]

    # Test 1: Vorhandene NFC-ID
    result = find_song_by_nfc("123ABC", songs)
    assert result == (0, ("123ABC", "Song A"))

    # Test 2: Letztes Element
    result = find_song_by_nfc("789GHI", songs)
    assert result == (2, ("789GHI", "Song C"))

   # Test 3: Nicht vorhandene NFC-ID
    result = find_song_by_nfc("000000", songs)
    assert result == (None, None)

    # Test 5: Ungültiges Format (kein Tupel)
    invalid_songs = [
        {"nfc_id": "123ABC", "name": "Song A"},
        {"nfc_id": "456DEF", "name": "Song B"}
    ]

    with pytest.raises(KeyError):
        find_song_by_nfc("123ABC", invalid_songs)
