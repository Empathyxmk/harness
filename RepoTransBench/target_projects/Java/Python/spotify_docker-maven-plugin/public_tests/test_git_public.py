import pytest
from unittest.mock import Mock

class MojoExecutionException(Exception):
    pass

class DockerException(Exception):
    pass

class Git:
    def __init__(self):
        self._repo = None

    def setRepo(self, repo):
        self._repo = repo

    def getCommitId(self):
        if self._repo is None:
            raise MojoExecutionException()
        commit = self._repo.resolve("HEAD")
        if commit is None:
            return None
        return commit

def test_get_commit_id_when_repo_still_null_throws_exception():
    git = Git()
    git.setRepo(None)
    with pytest.raises(MojoExecutionException):
        git.getCommitId()

def test_get_commit_id_when_head_is_missing_returns_none():
    repo = Mock()
    repo.resolve.return_value = None
    git = Git()
    git.setRepo(repo)
    commit_id = git.getCommitId()
    assert commit_id is None