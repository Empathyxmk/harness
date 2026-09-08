import pytest
from unittest.mock import Mock

class DockerException(Exception):
    pass

class DockerClient:
    def push(self, name, handler): ...
    def __init__(self): pass

class RegistryAuth:
    def __init__(self, username, password, email):
        self._username = username
        self._password = password
        self._email = email
    def username(self):
        return self._username
    def password(self):
        return self._password
    def email(self):
        return self._email

class PushMojo:
    def __init__(self, skip_docker_push=False, skip_docker=False):
        self._skip_docker_push = skip_docker_push
        self._skip_docker = skip_docker
    def isSkipDockerPush(self):
        return self._skip_docker_push
    def isSkipDocker(self):
        return self._skip_docker
    def registryAuth(self):
        return RegistryAuth("dxia3", "SxpxdUQA2mvX7oj", "dxia+3@spotify.com")
    def execute(self, docker=None):
        if self._skip_docker:
            return
        if self._skip_docker_push:
            return
        if docker:
            docker.push("busybox", None)

def test_push():
    docker = Mock(spec=DockerClient)
    mojo = PushMojo()
    mojo.execute(docker)
    docker.push.assert_called_with("busybox", None)

def test_push_skip_push():
    docker = Mock(spec=DockerClient)
    mojo = PushMojo(skip_docker_push=True)
    mojo.execute(docker)
    docker.push.assert_not_called()

def test_push_skip_docker():
    mojo = PushMojo(skip_docker=True)
    mojo.execute()  # Should not call anything

def test_push_private_repo():
    mojo = PushMojo()
    auth = mojo.registryAuth()
    assert auth.username() == "dxia3"
    assert auth.password() == "SxpxdUQA2mvX7oj"
    assert auth.email() == "dxia+3@spotify.com"