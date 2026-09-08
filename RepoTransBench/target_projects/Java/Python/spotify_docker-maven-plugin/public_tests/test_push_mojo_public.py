from unittest.mock import Mock

class PushMojo:
    def __init__(self):
        self._skip_docker = False
        self._skip_docker_push = False
    def isSkipDocker(self):
        return self._skip_docker
    def isSkipDockerPush(self):
        return self._skip_docker_push
    def execute(self, docker=None):
        if self._skip_docker:
            return
        if self._skip_docker_push or docker is None:
            return
        docker.push("repo", None)

def test_push_mojo_skipped_docker_public():
    mojo = PushMojo()
    mojo._skip_docker = True
    mocha = mojo
    mocha.execute()
    # Should skip all; nothing to verify.

def test_push_mojo_skipped_push_public():
    docker = Mock()
    mojo = PushMojo()
    mojo._skip_docker_push = True
    mojo.execute(docker)
    docker.push.assert_not_called()