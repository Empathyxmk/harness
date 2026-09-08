# openwifipass/Keys.py

BLE_MFG_ID = 0x004C  # Apple BLE Manufacturer ID
PWS_TYPE = 0x0F      # PWS TLV8 type

def get_ble_vendor():
    return BLE_MFG_ID

def get_pws_type():
    return PWS_TYPE

class SessionKeys:
    # Dummy implementation to maintain API for import in GrantorHandler
    def __init__(self):
        self.key = "dummy_session_key"
    def get(self):
        return self.key