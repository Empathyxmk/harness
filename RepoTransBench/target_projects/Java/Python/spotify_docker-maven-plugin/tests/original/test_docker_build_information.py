import pytest

class DockerBuildInformation:
    def __init__(self, image=None, log=None):
        self._image = image
        self._digest = None
        self._image_id = None
        self._image_name = None
        self._tags = None
    def getImage(self):
        return self._image
    def setDigest(self, digest):
        self._digest = digest
    def getDigest(self):
        return self._digest
    def setImageId(self, val):
        self._image_id = val
    def setImageName(self, val):
        self._image_name = val
    def setTags(self, lst):
        self._tags = lst
    def getImageId(self):
        return self._image_id
    def getImageName(self):
        return self._image_name
    def getTags(self):
        return self._tags
    def toJsonBytes(self):
        import json
        return json.dumps({"digest": self._digest, "image": self._image}).encode()

def test_constructor_and_getters():
    dbi = DockerBuildInformation("theImage")
    assert dbi.getImage() == "theImage"
    dbi.setDigest("digestVal")
    assert dbi.getDigest() == "digestVal"

def test_to_json_bytes():
    dbi = DockerBuildInformation("testing")
    dbi.setDigest("digest")
    json_bytes = dbi.toJsonBytes()
    s = json_bytes.decode()
    assert "\"digest\"" in s
    assert "\"image\"" in s