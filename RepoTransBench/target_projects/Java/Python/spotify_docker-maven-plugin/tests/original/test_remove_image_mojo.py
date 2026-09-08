import pytest
from unittest.mock import Mock, call
import types

class DockerException(Exception):
    pass

class ImageNotFoundException(DockerException):
    pass

class DockerClient:
    def removeImage(self, name, force, noprune):
        pass

class RemoveImageMojo:
    def execute(self, docker):
        # Simulate: tries to remove "imageToRemove", and in some cases, remove tagged
        try:
            docker.removeImage("imageToRemove", True, False)
        except ImageNotFoundException:
            pass
        try:
            docker.removeImage("imageToRemove:123456", True, False)
        except ImageNotFoundException:
            pass
        try:
            docker.removeImage("imageToRemove:bbbbbbb", True, False)
        except ImageNotFoundException:
            pass

def test_remove_image():
    docker = Mock(spec=DockerClient)
    mojo = RemoveImageMojo()
    mojo.execute(docker)
    docker.removeImage.assert_any_call("imageToRemove", True, False)

def test_remove_missing_image():
    docker = Mock(spec=DockerClient)
    docker.removeImage.side_effect = [ImageNotFoundException(), None, None]
    mojo = RemoveImageMojo()
    try:
        mojo.execute(docker)
        docker.removeImage.assert_any_call("imageToRemove", True, False)
    except Exception as e:
        assert not isinstance(e, ImageNotFoundException)

def test_remove_image_with_tags():
    docker = Mock(spec=DockerClient)
    calls = [
        call("imageToRemove", True, False),
        call("imageToRemove:123456", True, False),
        call("imageToRemove:bbbbbbb", True, False)
    ]
    docker.removeImage.side_effect = [
        ImageNotFoundException(),
        ImageNotFoundException(),
        []
    ]
    mojo = RemoveImageMojo()
    try:
        mojo.execute(docker)
    except Exception as e:
        assert not isinstance(e, ImageNotFoundException)
    docker.removeImage.assert_has_calls(calls)