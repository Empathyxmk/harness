class DockerBuildInformation:
    def __init__(self):
        self._image_id = None
        self._image_name = None
        self._tags = None
    def setImageId(self, val): self._image_id = val
    def setImageName(self, val): self._image_name = val
    def setTags(self, val): self._tags = val
    def getImageId(self): return self._image_id
    def getImageName(self): return self._image_name
    def getTags(self): return self._tags

def test_build_info_setter_getter_public():
    info = DockerBuildInformation()
    info.setImageId("publicId2")
    info.setImageName("publicName2")
    info.setTags(["publicTag1","publicTag2"])
    assert info.getImageId() == "publicId2"
    assert info.getImageName() == "publicName2"
    assert info.getTags() == ["publicTag1","publicTag2"]