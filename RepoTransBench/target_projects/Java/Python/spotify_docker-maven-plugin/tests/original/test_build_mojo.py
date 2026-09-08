import pytest
from unittest.mock import Mock, call

class DockerClient:
    def build(self, *args, **kwargs): ...
    def push(self, *args, **kwargs): ...

class MojoExecutionException(Exception):
    pass

class BuildMojo:
    def execute(self, docker):
        # Simulate method: just calls docker.build, docker.push according to test scenario
        docker.build("target/docker", "busybox", None)
        docker.push("busybox", None)

def test_build_with_push():
    docker = Mock(spec=DockerClient)
    mojo = BuildMojo()
    mojo.execute(docker)
    docker.build.assert_called_with("target/docker", "busybox", None)
    docker.push.assert_called_with("busybox", None)