import enum

class Output(enum.Enum):
    PNG = "png"
    JPG = "jpg"

    def get_format(self):
        return self.value

def test_enum_format():
    # reversed order and check equality still
    assert Output.PNG.get_format().lower() == "png"
    assert Output.JPG.get_format().upper() == "JPG"