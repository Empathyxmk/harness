import pytest
import sys
import time
import logging
from unittest.mock import patch, MagicMock
import threading
import os

# Configure logging for better visibility during testing
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Suppress some noisy logs if necessary
# logging.getLogger('gattlib').setLevel(logging.WARNING)


# These will be mocked, but imported to simulate the C structure
try:
    from src.gattlib import (
        GATTLIB_SUCCESS, GATTLIB_BUSY, GATTLIB_ERROR, GATTLIB_LOG,
        gattlib_adapter_open, gattlib_adapter_scan_enable, gattlib_adapter_scan_disable,
        gattlib_adapter_close, gattlib_connect, gattlib_disconnect, gattlib_mainloop
    )
except ImportError:
    # Fallback for direct execution outside of pytest discovery that sets up sys.path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))
    from gattlib import (
        GATTLIB_SUCCESS, GATTLIB_BUSY, GATTLIB_ERROR, GATTLIB_LOG,
        gattlib_adapter_open, gattlib_adapter_scan_enable, gattlib_adapter_scan_disable,
        gattlib_adapter_close, gattlib_connect, gattlib_disconnect, gattlib_mainloop
    )

# PUBLIC TEST uses different constants
BLE_CONNECT_LOOP_COUNT_PUBLIC = 5   # Was 20 in original
BLE_SCAN_TIMEOUT_PUBLIC = 60  # Was 180 in original

# Global variables, mimicing C's static variables
adapter_name = None
reference_mac_address = "00:11:22:33:44:77" # Public dummy MAC, different from original

# Condition variable equivalent to C's pthread_cond_t/pthread_mutex_t
m_connection_terminated = {
    'condition': threading.Condition(),
    'value': False
}

def on_device_connect_public(adapter, dst, connection, error, user_data):
    """
    Translated from C's on_device_connect (public variant)
    """
    GATTLIB_LOG("INFO", f"on_device_connect_public called for {dst} with error {error}")
    if error != 0:
        GATTLIB_LOG("ERROR", f"Failed to connect to device '{reference_mac_address}': Error {error}")
        return

    ret = gattlib_disconnect(connection, True) # wait_disconnection
    assert ret == GATTLIB_SUCCESS, "gattlib_disconnect failed in public test"

    GATTLIB_LOG("DEBUG", f"Bluetooth device '{reference_mac_address}' should be disconnected.")

    with m_connection_terminated['condition']:
        m_connection_terminated['value'] = True
        m_connection_terminated['condition'].notify_all()

def stricmp(a, b):
    """
    Simple case-insensitive string comparison.
    Translated from C's stricmp
    """
    return a.lower() == b.lower()

def ble_discovered_device_public(adapter, addr, name, user_data):
    """
    Translated from C's ble_discovered_device (public variant)
    """
    GATTLIB_LOG("INFO", f"ble_discovered_device_public: Discovered device '{name}' at '{addr}'")

    if not stricmp(addr, reference_mac_address):
        GATTLIB_LOG("DEBUG", f"Ignoring device '{addr}', not '{reference_mac_address}'")
        return

    GATTLIB_LOG("INFO", f"Found bluetooth device '{reference_mac_address}'")

    for i in range(BLE_CONNECT_LOOP_COUNT_PUBLIC):
        GATTLIB_LOG("INFO", f"Connecting to the bluetooth device '{addr}' {i+1}/{BLE_CONNECT_LOOP_COUNT_PUBLIC}")

        with m_connection_terminated['condition']:
            m_connection_terminated['value'] = False # Reset for each connection attempt

        ret = GATTLIB_BUSY # Initialize to busy to enter the while loop
        while ret == GATTLIB_BUSY:
            ret = gattlib_connect(adapter, addr, None, on_device_connect_public, adapter) # GATTLIB_CONNECTION_OPTIONS_NONE is 0
            if ret == GATTLIB_BUSY:
                GATTLIB_LOG("DEBUG", f"Failed to connect to the bluetooth device '{addr}' because busy. Try again")
                time.sleep(0.0001) # Equivalent to g_usleep(100)

        if ret != GATTLIB_SUCCESS:
            GATTLIB_LOG("ERROR", f"Failed to connect to the bluetooth device '{addr}': {ret}")
            continue

        # Wait for the device to be connected/disconnected by on_device_connect_public
        with m_connection_terminated['condition']:
            if not m_connection_terminated['condition'].wait(timeout=5): # 5 seconds timeout
                pytest.fail(f"Timeout waiting for connection/disconnection callback for {addr} in public test")
            if not m_connection_terminated['value']:
                pytest.fail(f"Connection/disconnection callback did not set value for {addr} in public test")

def ble_task_public(arg):
    """
    Translated from C's ble_task (public variant)
    """
    global adapter_name
    GATTLIB_LOG("INFO", "Starting BLE public task...")
    adapter = None
    try:
        ret, adapter = gattlib_adapter_open(adapter_name)
        if ret != GATTLIB_SUCCESS:
            GATTLIB_LOG("ERROR", "Failed to open adapter in public test.")
            pytest.fail("Failed to open adapter in public test.")

        # This mock will be configured by the calling test function (test_continuous_connection_public_logic)
        # We no longer patch it inside this function.
        ret = gattlib_adapter_scan_enable(adapter, ble_discovered_device_public, BLE_SCAN_TIMEOUT_PUBLIC, None)
        if ret != GATTLIB_SUCCESS:
            GATTLIB_LOG("ERROR", "Failed to scan in public test.")
            pytest.fail("Failed to scan in public test.")

        gattlib_adapter_scan_disable(adapter)
        GATTLIB_LOG("INFO", "Scan completed in public test.")

    finally:
        if adapter:
            gattlib_adapter_close(adapter)
    GATTLIB_LOG("INFO", "BLE public task finished.")
    return GATTLIB_SUCCESS

@patch('src.gattlib.gattlib_adapter_open', side_effect=gattlib_adapter_open)
@patch('src.gattlib.gattlib_adapter_scan_enable') # This will be the mock_enable argument
@patch('src.gattlib.gattlib_adapter_scan_disable', side_effect=gattlib_adapter_scan_disable)
@patch('src.gattlib.gattlib_adapter_close', side_effect=gattlib_adapter_close)
@patch('src.gattlib.gattlib_connect', side_effect=gattlib_connect)
@patch('src.gattlib.gattlib_disconnect', side_effect=gattlib_disconnect)
@patch('src.gattlib.gattlib_mainloop', side_effect=gattlib_mainloop)
def test_continuous_connection_public_logic(mock_mainloop, mock_disconnect, mock_connect, mock_close, mock_disable, mock_enable, mock_open):
    """
    Translated from C's tests/test_continuous_connection/test_continuous_connection_public.c
    Tests the logic of continuous BLE connection and disconnection with public constants.
    """
    global adapter_name, reference_mac_address
    
    # Configure mock_enable to immediately call ble_discovered_device_public
    mock_enable.return_value = GATTLIB_SUCCESS
    def _mock_scan_enable_side_effect(adapter, discovered_callback, timeout, user_data):
        # Simulate discovery of the target device
        discovered_callback(adapter, reference_mac_address, "MockTargetDevicePublic", user_data)
        return GATTLIB_SUCCESS
    mock_enable.side_effect = _mock_scan_enable_side_effect

    GATTLIB_LOG("INFO", "Starting public continuous connection test...")
    ret = gattlib_mainloop(ble_task_public, None)

    assert ret == GATTLIB_SUCCESS, "gattlib_mainloop did not return success in public test"
    GATTLIB_LOG("INFO", "Public continuous connection test finished successfully.")