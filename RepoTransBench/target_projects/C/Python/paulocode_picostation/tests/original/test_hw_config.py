# tests/original/test_hw_config.py

from src import hw_config_mock

def test_sd_spi_device_existence():
    """Test at least one SD card and SPI device are reported."""
    assert hw_config_mock.sd_get_num() == 1
    assert hw_config_mock.spi_get_num() == 1

def test_sd_spi_get_by_num_valid_invalid():
    """Test sd_get_by_num and spi_get_by_num for valid and invalid indices."""
    assert hw_config_mock.sd_get_by_num(0) is not None
    assert hw_config_mock.sd_get_by_num(1) is None
    assert hw_config_mock.spi_get_by_num(0) is not None
    assert hw_config_mock.spi_get_by_num(1) is None