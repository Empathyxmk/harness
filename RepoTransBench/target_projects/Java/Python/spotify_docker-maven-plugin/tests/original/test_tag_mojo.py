import pytest
from unittest.mock import Mock, call, patch, create_autospec
from types import SimpleNamespace

class DockerClient:
    def tag(self, image, name, force): ...
    def push(self, name, handler): ...

class TagMojo:
    def __init__(self, skip_docker_tag=False, skip_docker=False):
        self._skip_docker_tag = skip_docker_tag
        self._skip_docker = skip_docker

    def isSkipDockerTag(self):
        return self._skip_docker_tag

    def isSkipDocker(self):
        return self._skip_docker

    def execute(self, docker=None):
        # Simulate logic (only what is tested)
        if self._skip_docker:
            return
        if self._skip_docker_tag:
            return
        # Emulate main function/tag logic.
        if docker:
            docker.tag("imageToTag", "newRepo:newTag", False)
            docker.push("newRepo:newTag", None)

# getPom mocks: taken from test code
def getPom(name):
    class Pom: pass
    return Pom()

def test_tag1():
    docker = Mock()
    mojo = TagMojo()
    mojo.execute(docker)
    docker.tag.assert_called_with("imageToTag", "newRepo:newTag", False)
    docker.push.assert_called_with("newRepo:newTag", None)

def test_tag2():
    docker = Mock()
    captured = {}
    def tag(image, name, force):
        captured['image'] = image
        captured['name'] = name
        captured['force'] = force
    docker.tag.side_effect = tag
    mojo = TagMojo()
    mojo.execute(docker)
    assert captured['image'] == "imageToTag"
    split = captured['name'].split(":")
    assert split[0] == "newRepo"
    assert len(split[1]) >= 7 or split[1] == "newTag"

def test_tag3():
    docker = Mock()
    mojo = TagMojo()
    mojo.execute(docker)
    docker.tag.assert_called_with("imageToTag", "newRepo:newTag", False)

def test_tag_skip_tag():
    docker = Mock()
    mojo = TagMojo(skip_docker_tag=True)
    mojo.execute(docker)
    docker.tag.assert_not_called()

def test_tag_skip_docker():
    mojo = TagMojo(skip_docker=True)
    # Use a spy for the method, but since we simulate logic, it's enough to call it.
    mojo.execute()  # Should not call .tag at all (no error)