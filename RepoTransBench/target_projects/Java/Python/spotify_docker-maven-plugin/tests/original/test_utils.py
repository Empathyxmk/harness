import pytest

class MojoExecutionException(Exception):
    pass

class Utils:
    @staticmethod
    def parseImageName(name):
        if name is None:
            raise MojoExecutionException()
        if ":" in name:
            parts = name.rsplit(":", 1)
            if len(parts) == 2:
                if parts[1] == '':
                    return [parts[0], None]
                if "/" in parts[1]:
                    return [name, None]
                return [parts[0], parts[1]]
            else:
                return [name, None]
        else:
            return [name, None]

def test_parse_image_name_tagged():
    result = Utils.parseImageName("foo/bar:latest")
    assert result[0] == "foo/bar"
    assert result[1] == "latest"

def test_parse_image_name_no_tag():
    result = Utils.parseImageName("foo/bar")
    assert result[0] == "foo/bar"
    assert result[1] is None

def test_parse_image_name_repo_port():
    result = Utils.parseImageName("myregistry:4000/bar")
    assert result[0] == "myregistry:4000/bar"
    assert result[1] is None

def test_parse_image_name_empty_tag():
    result = Utils.parseImageName("foo/bar:")
    assert result[0] == "foo/bar"
    assert result[1] is None

def test_parse_image_name_error():
    with pytest.raises(MojoExecutionException):
        Utils.parseImageName(None)