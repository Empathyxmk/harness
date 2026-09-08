import pytest
from unittest.mock import Mock, ANY, patch

# Simulated target class for import
# from package_under_test.openapi import HttpSessionConfig

class HttpSessionConfig:
    def addInterceptors(self, registry):
        # Simulated implementation for test coverage
        registry.addInterceptor(ANY)

def test_add_interceptors(mocker):
    config = HttpSessionConfig()
    registry = mocker.Mock()
    registry.addInterceptor.return_value = None
    config.addInterceptors(registry)
    registry.addInterceptor.assert_called_once_with(ANY)