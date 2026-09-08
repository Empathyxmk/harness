import pytest

class MojoExecutionException(Exception):
    pass

class CompositeImageName:
    def __init__(self, name, tags):
        self._name = name
        self._tags = tags

    @classmethod
    def create(cls, name, image_tags):
        if name is None or name.strip() == "" or name == ":" or name == ":/":
            raise MojoExecutionException()
        base_name = name.split(":")[0]
        tags = []
        if ":" in name:
            tag_part = name.split(":")[1]
            if tag_part:
                tags.append(tag_part)
        if image_tags:
            tags.extend(image_tags)
        elif not tags:
            raise MojoExecutionException()
        return cls(base_name, tags)

    def getName(self):
        return self._name

    def getImageTags(self):
        return self._tags

    @staticmethod
    def containsTag(imageName):
        if not imageName:
            return False
        if "/" in imageName:
            last_part = imageName.split("/")[-1]
        else:
            last_part = imageName
        colon_count = imageName.count(":")
        if colon_count == 0:
            return False
        if "/" in imageName and ":" in imageName and imageName.rfind(":") < imageName.rfind("/"):
            return False
        return True

def test_create_other_name_with_tag_and_image_tags():
    cin = CompositeImageName.create("publicrepo:pub1", ["pub2", "pub3"])
    assert cin.getName() == "publicrepo"
    assert cin.getImageTags() == ["pub1", "pub2", "pub3"]

def test_create_other_name_without_tag_but_with_different_image_tags():
    cin = CompositeImageName.create("publicrepo", ["pub4"])
    assert cin.getName() == "publicrepo"
    assert cin.getImageTags() == ["pub4"]

def test_create_blank_different_name():
    with pytest.raises(MojoExecutionException):
        CompositeImageName.create("   ", ["otherTag"])

def test_create_null_tags_and_no_image_tag_again():
    with pytest.raises(MojoExecutionException):
        CompositeImageName.create("anotherrepo", None)

def test_create_invalid_colon_name():
    with pytest.raises(MojoExecutionException):
        CompositeImageName.create(":/", ["pubTag"])

def test_create_name_with_tag_no_image_tags_other():
    cin = CompositeImageName.create("otherrepo:bar", None)
    assert cin.getName() == "otherrepo"
    assert cin.getImageTags() == ["bar"]

def test_contains_tag_colon_slash_different_logic():
    assert CompositeImageName.containsTag("registry2/publicorigin:mytag")
    assert not CompositeImageName.containsTag("registry2:8080/publicorigin")
    assert CompositeImageName.containsTag("custom:latest")
    assert not CompositeImageName.containsTag("custom")

def test_create_another_tag_with_slash_and_colon():
    cin = CompositeImageName.create("myreg/pubimg:release", ["stable"])
    assert cin.getName() == "myreg/pubimg"
    assert cin.getImageTags() == ["release", "stable"]