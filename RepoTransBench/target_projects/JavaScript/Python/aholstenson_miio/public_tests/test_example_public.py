import pytest

class DummyDeviceModule:
    @staticmethod
    def device(address=None, **kwargs):
        if address == 'alternateIp':
            return {'id': 'dev-999', 'name': 'TestDeviceAlt'}
        raise Exception('not found')

def test_connect_to_new_device_successfully_with_alternate_address():
    dev = DummyDeviceModule.device(address='alternateIp')
    assert dev['id'] == 'dev-999'
    assert dev['name'] == 'TestDeviceAlt'

def test_prints_error_on_device_connection_failure_with_different_error():
    with pytest.raises(Exception) as excinfo:
        DummyDeviceModule.device(address='badIp')
    assert 'not found' in str(excinfo.value) or 'remote host refused' in str(excinfo.value)