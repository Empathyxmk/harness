import pytest
import io
import sys
from unittest.mock import patch

# Mock the minimal BeaconPrintf for test purposes
def BeaconPrintf(log_type, fmt, *args):
    """Simulates BeaconPrintf, captures output to stdout for assertion."""
    sys.stdout.write(fmt % args + '\n')

# Simulated registry key struct and minimal behaviour for mock registry
class PublicFakeRegistry:
    def __init__(self):
        self.key = ""
        self.value = ""

# Global registry mock for test isolation (Python equivalent of C global struct)
public_fake_registry = PublicFakeRegistry()

# New mock "SetValue" and "DeleteValue" with different public test data logic
def RegistryPersistence_SetValue(path: str, key: str, value: str) -> int:
    """Simulates setting a registry value."""
    public_fake_registry.key = f"{path}\\{key}"
    public_fake_registry.value = value
    return 0 # success

def RegistryPersistence_DeleteValue(path: str, key: str) -> int:
    """Simulates deleting a registry value."""
    # Just blank out for public test
    public_fake_registry.key = ""
    public_fake_registry.value = ""
    return 0 # success

class TestRegistryPersistencePublic:
    # Reset the global fake registry before each test to ensure isolation
    def setup_method(self):
        global public_fake_registry
        public_fake_registry = PublicFakeRegistry()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_registry_persistence_case_overwrite(self, mock_stdout):
        test_path = "HKEY_LOCAL_MACHINE\\Software\\Rvrsh3ll\\UnitPublic"
        test_key = "SampleKey"
        test_value = "FirstVal"
        test_value2 = "ChangedVal"

        # Set, verify set
        assert RegistryPersistence_SetValue(test_path, test_key, test_value) == 0
        assert public_fake_registry.key == f"{test_path}\\{test_key}"
        assert public_fake_registry.value == "FirstVal"

        # Overwrite and verify
        assert RegistryPersistence_SetValue(test_path, test_key, test_value2) == 0
        assert public_fake_registry.key == f"{test_path}\\{test_key}"
        assert public_fake_registry.value == "ChangedVal"

        # Delete and verify removed
        assert RegistryPersistence_DeleteValue(test_path, test_key) == 0
        assert public_fake_registry.key == ""
        assert public_fake_registry.value == ""

        BeaconPrintf(0, "public_registry_persistence_test_case_overwrite passed.")
        assert "public_registry_persistence_test_case_overwrite passed." in mock_stdout.getvalue()

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_public_registry_persistence_case_unicode(self, mock_stdout):
        test_path = "HKEY_LOCAL_MACHINE\\Software\\ΩTest"
        test_key = "ユニコード"
        test_value = "值🎉"

        assert RegistryPersistence_SetValue(test_path, test_key, test_value) == 0
        assert public_fake_registry.key == f"{test_path}\\{test_key}"
        assert public_fake_registry.value == "值🎉"

        assert RegistryPersistence_DeleteValue(test_path, test_key) == 0
        assert public_fake_registry.key == "" # Check if key is truly cleared
        assert public_fake_registry.value == "" # Check if value is truly cleared

        BeaconPrintf(0, "public_registry_persistence_test_case_unicode passed.")
        assert "public_registry_persistence_test_case_unicode passed." in mock_stdout.getvalue()