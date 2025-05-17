import pytest
from unittest.mock import patch, MagicMock
from pn532_init import init_pn532, read_nfc_with_retry
import sys
sys.path.append('/home/maxi/PythonCodes/code')

def test_init_pn532():
    assert init_pn532() is not None
    assert init_pn532().firmware_version is not None
    assert init_pn532().SAM_configuration() is None
    assert init_pn532().read_passive_target is not None


def test_read_nfc_with_retry():
    pn532 = init_pn532()
    uid = read_nfc_with_retry(pn532)
    assert uid is None

