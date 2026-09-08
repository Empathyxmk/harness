import pytest
from unittest.mock import Mock, ANY

# Stubs to mimic the Java/Android structure and logic, as in original
class PackageManager:
    PERMISSION_GRANTED = 1
    PERMISSION_DENIED = 0

class ConnectivityManager:
    def __init__(self):
        self._network_info = None

    def getActiveNetworkInfo(self):
        return self._network_info

    def setActiveNetworkInfo(self, network_info):
        self._network_info = network_info

class NetworkInfo:
    def __init__(self):
        self._connected = False

    def isConnected(self):
        return self._connected

    def setConnected(self, connected):
        self._connected = connected

class Context:
    CONNECTIVITY_SERVICE = 'connectivity'

    def __init__(self):
        self._pm = None
        self._services = {}
        self._package_name = None

    def getPackageManager(self):
        return self._pm

    def setPackageManager(self, pm):
        self._pm = pm

    def getPackageName(self):
        return self._package_name

    def setPackageName(self, name):
        self._package_name = name

    def getSystemService(self, name):
        return self._services.get(name, None)

    def setSystemService(self, name, service):
        self._services[name] = service

class ConnectionUtils:
    @staticmethod
    def hasAccessNetworkStatePermission(context):
        pm = context.getPackageManager()
        pkg_name = context.getPackageName()
        permission = pm.checkPermission(ANY, pkg_name)
        return permission == PackageManager.PERMISSION_GRANTED

    @staticmethod
    def isOnline(context):
        pm = context.getPackageManager()
        pkg_name = context.getPackageName()
        if pm.checkPermission(ANY, pkg_name) == PackageManager.PERMISSION_GRANTED:
            connectivity = context.getSystemService(Context.CONNECTIVITY_SERVICE)
            if connectivity is None:
                return False
            info = connectivity.getActiveNetworkInfo()
            if info is not None:
                return info.isConnected()
            else:
                return False
        else:
            return True

@pytest.fixture
def setup_context_public():
    mock_context = Context()
    mock_pm = Mock()
    mock_connectivity_manager = ConnectivityManager()
    mock_network_info = NetworkInfo()
    mock_context.setPackageManager(mock_pm)
    # Different package name for public test
    mock_context.setPackageName("eu.inloop.easygcm.publictest")
    return mock_context, mock_pm, mock_connectivity_manager, mock_network_info

def test_has_access_network_state_permission_granted_different(setup_context_public):
    mock_context, mock_pm, _, _ = setup_context_public
    mock_pm.checkPermission.return_value = PackageManager.PERMISSION_GRANTED
    assert ConnectionUtils.hasAccessNetworkStatePermission(mock_context)

def test_has_access_network_state_permission_denied_different(setup_context_public):
    mock_context, mock_pm, _, _ = setup_context_public
    mock_pm.checkPermission.return_value = PackageManager.PERMISSION_DENIED
    assert not ConnectionUtils.hasAccessNetworkStatePermission(mock_context)

def test_is_online_with_permission_and_connected_different(setup_context_public):
    mock_context, mock_pm, mock_connectivity_manager, mock_network_info = setup_context_public
    mock_pm.checkPermission.return_value = PackageManager.PERMISSION_GRANTED
    mock_context.setSystemService(Context.CONNECTIVITY_SERVICE, mock_connectivity_manager)
    mock_connectivity_manager.setActiveNetworkInfo(mock_network_info)
    mock_network_info.setConnected(True)
    assert ConnectionUtils.isOnline(mock_context)

def test_is_online_with_permission_and_not_connected_different(setup_context_public):
    mock_context, mock_pm, mock_connectivity_manager, mock_network_info = setup_context_public
    mock_pm.checkPermission.return_value = PackageManager.PERMISSION_GRANTED
    mock_context.setSystemService(Context.CONNECTIVITY_SERVICE, mock_connectivity_manager)
    mock_connectivity_manager.setActiveNetworkInfo(mock_network_info)
    mock_network_info.setConnected(False)
    assert not ConnectionUtils.isOnline(mock_context)

def test_is_online_with_permission_and_no_network_info_different(setup_context_public):
    mock_context, mock_pm, mock_connectivity_manager, _ = setup_context_public
    mock_pm.checkPermission.return_value = PackageManager.PERMISSION_GRANTED
    mock_context.setSystemService(Context.CONNECTIVITY_SERVICE, mock_connectivity_manager)
    mock_connectivity_manager.setActiveNetworkInfo(None)
    assert not ConnectionUtils.isOnline(mock_context)

def test_is_online_without_permission_different(setup_context_public):
    mock_context, mock_pm, _, _ = setup_context_public
    mock_pm.checkPermission.return_value = PackageManager.PERMISSION_DENIED
    assert ConnectionUtils.isOnline(mock_context)