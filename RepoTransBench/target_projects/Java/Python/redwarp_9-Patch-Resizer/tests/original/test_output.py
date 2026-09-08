import enum

class Output(enum.Enum):
    PNG = "png"
    JPG = "jpg"

    def get_format(self):
        return self.value

def test_enum_format():
    assert Output.PNG.get_format() == "png"
    assert Output.JPG.get_format() == "jpg"