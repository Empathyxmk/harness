import pytest

# Helper class to simulate the C behavior for public tests,
# with distinct stub logic from the original tests.
class MockDhtDataPublic:
    def __init__(self):
        self.humidity = 0.0
        self.temperature = 0.0
        self.return_code = -99 # Default unhandled error

    def read_dht_data(self, dht_type: int, pin: int) -> int:
        """
        Simulates the behavior of the C read_dht_data function stub for public tests.
        """
        self.humidity = 0.0
        self.temperature = 0.0

        if dht_type == 21 and pin == 4:
            self.humidity = 31.5
            self.temperature = 18.3
            self.return_code = 0  # Simulate success, different data
        elif dht_type == 12 and pin == 13:
            self.return_code = -2  # Simulate data error on different input
        else:
            self.return_code = -9  # Simulate a different code for other/unexpected
        return self.return_code

# Instantiate the mock for public tests
mock_dht_public = MockDhtDataPublic()

def test_dht_read_public_returns_success():
    """
    Corresponds to C's public test_dht_read_returns_success.
    Tests a successful read scenario with specific mocked values for public tests.
    """
    result_code = mock_dht_public.read_dht_data(21, 4)
    assert result_code == 0
    assert mock_dht_public.humidity == pytest.approx(31.5)
    assert mock_dht_public.temperature == pytest.approx(18.3)

def test_dht_read_public_returns_data_error():
    """
    Corresponds to C's public test_dht_read_returns_data_error.
    Tests a data error scenario for public tests.
    """
    result_code = mock_dht_public.read_dht_data(12, 13)
    assert result_code == -2

def test_dht_read_public_returns_custom_error():
    """
    Corresponds to C's public test_dht_read_returns_custom_error.
    Tests a custom error scenario for public tests.
    """
    result_code = mock_dht_public.read_dht_data(1, 1)
    assert result_code == -9