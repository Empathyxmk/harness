import pytest
import os

class Utils:
    @staticmethod
    def parseImageName(name):
        if name is None:
            raise Exception()
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
    @staticmethod
    def pushImage(*args, **kwargs):
        pass
    @staticmethod
    def writeImageInfoFile(image, tag, file):
        with open(file, "w") as f:
            f.write('{"image": "%s", "tag": "%s"}' % (image, tag))

def test_parse_image_name_for_another_format():
    input = "registry.example.com/newrepo/sample:mytag"
    result = Utils.parseImageName(input)
    assert result[0] == "registry.example.com/newrepo/sample"
    assert result[1] == "mytag"

def test_parse_image_name_when_no_tag_provided():
    input = "ubuntu"
    result = Utils.parseImageName(input)
    assert result == ["ubuntu", None]

def test_push_image_no_push():
    Utils.pushImage(None, False, "image:tag", None, "skip", None, None, None)

def test_write_image_info_file(tmp_path):
    target_fn = tmp_path / "image_pub_info.json"
    Utils.writeImageInfoFile("image:pub", "imagetag", str(target_fn))
    assert os.path.exists(target_fn)
    os.remove(target_fn)