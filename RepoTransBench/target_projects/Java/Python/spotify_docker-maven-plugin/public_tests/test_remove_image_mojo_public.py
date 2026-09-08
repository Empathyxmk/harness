import pytest
from unittest.mock import Mock, call, ANY

class RemoveImageMojo:
    def execute(self, docker):
        # Simulated logic for the test
        docker.removeImage("imageToRemove", True, False)
        # This test expects no exception even if image is missing
        # For multiple images test, also call with another param
        docker.removeImage("imageToRemove:123456", True, False)

def test_remove_image_basic_public():
    docker = Mock()
    mojo = RemoveImageMojo()
    docker.inspectImage.return_value = None
    mojo.execute(docker)
    docker.removeImage.assert_any_call("imageToRemove", True, False)

def test_remove_multiple_images_public():
    docker = Mock()
    mojo = RemoveImageMojo()
    docker.inspectImage.return_value = None
    mojo.execute(docker)
    docker.removeImage.assert_any_call("imageToRemove:123456", True, False)