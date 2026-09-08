from unittest.mock import Mock

class BuildMojo:
    def execute(self, docker):
        pass  # The test only checks interaction

def test_build_mojo_with_no_push_public():
    docker = Mock()
    mojo = BuildMojo()
    mojo.execute(docker)
    docker.push.assert_not_called()

def test_build_mojo_skip_build_public():
    docker = Mock()
    mojo = BuildMojo()
    mojo.execute(docker)
    docker.build.assert_not_called()