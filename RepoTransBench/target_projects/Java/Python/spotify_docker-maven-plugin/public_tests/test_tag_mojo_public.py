import re
from unittest.mock import Mock

class TagMojo:
    def __init__(self):
        self.image = "imageToTag"
        self.repo = "newRepo"
        self.tag = "newTag"

    def execute(self, docker):
        docker.tag(self.image, f"{self.repo}:{self.tag}", True)

def test_tag_alpha():
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
    assert split[1] == "newTag"

def test_tag_force():
    docker = Mock()
    captured = {}
    def tag(image, name, force):
        captured['image'] = image
        captured['name'] = name
        captured['force'] = force
    docker.tag.side_effect = tag
    mojo = TagMojo()
    mojo.execute(docker)
    assert captured['force']