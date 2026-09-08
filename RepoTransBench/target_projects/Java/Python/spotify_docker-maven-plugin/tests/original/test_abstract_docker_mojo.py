import pytest
from unittest.mock import Mock, patch
from types import SimpleNamespace

class AbstractDockerMojo:
    def replaceRegistryUrl(self, old, new):
        return new

def test_registry_url_replace():
    mojo = AbstractDockerMojo()
    url = mojo.replaceRegistryUrl("index.docker.io", "my.other.io")
    assert url == "my.other.io"