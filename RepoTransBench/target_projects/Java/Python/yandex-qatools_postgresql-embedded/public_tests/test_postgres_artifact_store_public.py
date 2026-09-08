import pytest

class PostgresArtifactStoreFake:
    def __init__(self, artifact):
        self.artifact = artifact

    def get_artifact(self):
        return self.artifact

    def set_artifact(self, artifact):
        self.artifact = artifact

def test_stores_artifact_name_with_different_value():
    store = PostgresArtifactStoreFake("public-art-unique-192")
    assert store.get_artifact() == "public-art-unique-192"

def test_set_artifact_updates_artifact_with_another_value():
    store = PostgresArtifactStoreFake("start-art-public-1")
    store.set_artifact("set-artifact-public-2")
    assert store.get_artifact() == "set-artifact-public-2"