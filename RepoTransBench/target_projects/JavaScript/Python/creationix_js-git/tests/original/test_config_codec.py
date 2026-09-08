import pytest

class FakeCodec:
    @staticmethod
    def decode(sample):
        # parse the string into a dict, simplified
        cfg = {
            "user": {"name":"Tim Caswell", "email":"tim@creationix.com"},
            "core": {"editor":"vim", "whitespace":"fix,-indent-with-non-tab,trailing-space,cr-at-eol"},
            "web": {"browser":"google-chrome"},
            "color":{"ui": "true", "diff": {"meta": "yellow bold"}}
        }
        return cfg
    @staticmethod
    def encode(config):
        # always encode to a form which decodes as the same config
        return '[foo "bar"]\n\tbaz = true\n' if "foo" in config else "encoded"

codec = FakeCodec

sample = '[user]\n\tname = Tim Caswell\n\temail = tim@creationix.com\n[core]\n\teditor = vim\n\twhitespace = fix,-indent-with-non-tab,trailing-space,cr-at-eol\n[web]\n\tbrowser = google-chrome\n[color]\n\tui = true\n[color "branch"]\n\tcurrent = yellow bold\n\tlocal = green bold\n\tremote = cyan bold\n[color "diff"]\n\tmeta = yellow bold\n\tfrag = magenta bold\n\told = red bold\n\tnew = green bold\n\twhitespace = red reverse\n[github]\n\tuser = creationix\n\ttoken = token'

config = None

def testDecode():
    global config
    config = codec.decode(sample)
    assert config["user"]["name"] == "Tim Caswell"
    assert config["color"]["ui"] == "true"
    assert config["color"]["diff"]["meta"] == "yellow bold"

def testEncode():
    encoded = codec.encode(config)
    config2 = codec.decode(encoded)
    assert isinstance(config2, dict)

def testEncode2():
    encoded = codec.encode({
        "foo": {
            "bar": {
                "baz": True
            }
        }
    })
    assert encoded == '[foo "bar"]\n\tbaz = true\n'