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
        # Similar to logic in Java: tag if colon after last slash, unless in port
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
            # colon before last slash: port, not tag
            return False
        # Now, has colon, and after last slash
        return True

def test_create_name_with_tag_and_image_tags():
    cin = CompositeImageName.create("repo:tag1", ["tag2","tag3"])
    assert cin.getName() == "repo"
    assert cin.getImageTags() == ["tag1", "tag2", "tag3"]

def test_create_name_without_tag_but_with_image_tags():
    cin = CompositeImageName.create("repo", ["tag2"])
    assert cin.getName() == "repo"
    assert cin.getImageTags() == ["tag2"]

def test_create_blank_name():
    with pytest.raises(MojoExecutionException):
        CompositeImageName.create("", ["atag"])

def test_create_null_tags_and_no_image_tag():
    with pytest.raises(MojoExecutionException):
        CompositeImageName.create("repo", None)

def test_create_only_colon():
    with pytest.raises(MojoExecutionException):
        CompositeImageName.create(":", ["someTag"])

def test_create_name_with_tag_no_image_tags():
    cin = CompositeImageName.create("repo:foo", None)
    assert cin.getName() == "repo"
    assert cin.getImageTags() == ["foo"]

def test_contains_tag_colon_slash_logic():
    assert CompositeImageName.containsTag("myregistry/origin:tag1") is True
    assert CompositeImageName.containsTag("myregistry:5000/origin") is False
    assert CompositeImageName.containsTag("image:tag") is True
    assert CompositeImageName.containsTag("image") is False

def test_create_tag_with_slash_and_colon():
    cin = CompositeImageName.create("reg/some:image", ["more"])
    assert cin.getName() == "reg/some"
    assert cin.getImageTags() == ["image", "more"]