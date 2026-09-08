import pytest

# Helper class to simulate the C behavior where read_dht_data modifies
# variables passed by pointer. The C tests define a stub for read_dht_data
# within the test file, so this class mimics that standalone behavior.
class MockDhtData:
    def __init__(self):
        self.humidity = 0.0
        self.temperature = 0.0
        self.return_code = -99 # Default unhandled error

    def read_dht_data(self, dht_type: int, pin: int) -> int:
        """
        Simulates the behavior of the C read_dht_data function stub.
        Updates self.humidity and self.temperature and returns a result code.
        """
        self.humidity = 0.0
        self.temperature = 0.0

        if dht_type == 11 and pin == 2:
            self.humidity = 43.0
            self.temperature = 32.0
            self.return_code = 0  # Simulate success
        elif dht_type == 22 and pin == 10:
            self.return_code = -2  # Simulate data error
        else:
            self.return_code = -1  # Simulate timeout/other
        return self.return_code

# Instantiate the mock for use in tests
mock_dht = MockDhtData()

def test_dht_read_returns_success():
    """
    Corresponds to C's test_dht_read_returns_success.
    Tests a successful read scenario with specific mocked values.
    """
    result_code = mock_dht.read_dht_data(11, 2)
    assert result_code == 0
    assert mock_dht.humidity == pytest.approx(43.0)
    assert mock_dht.temperature == pytest.approx(32.0)

def test_dht_read_returns_data_error():
    """
    Corresponds to C's test_dht_read_returns_data_error.
    Tests a data error scenario.
    """
    result_code = mock_dht.read_dht_data(22, 10)
    assert result_code == -2
    # C test does not assert humidity/temperature on error, so we don't either.

def test_dht_read_returns_timeout():
    """
    Corresponds to C's test_dht_read_returns_timeout.
    Tests a timeout or unhandled error scenario.
    """
    result_code = mock_dht.read_dht_data(0, 0)
    assert result_code == -1
    # C test does not assert humidity/temperature on timeout, so we don't either.