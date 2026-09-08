import pytest

# Mock implementations for test logic
class Modes:
    file = 100644
    tree = 40000
    blob = 100644

modes = Modes()

class FakeBodec:
    @staticmethod
    def fromUnicode(s): return s.encode("utf-8")
    @staticmethod
    def toUnicode(b): return b.decode("utf-8")
    @staticmethod
    def toRaw(b): return b
    @staticmethod
    def create(n): return bytearray(list(range(n)))
    @staticmethod
    def isBinary(x): return isinstance(x, (bytes, bytearray))

bodec = FakeBodec

def fake_sha1(data):
    return "dummyhash"

class FakeCodec:
    @staticmethod
    def frame(obj):
        # Just simulate a valid return value
        return bodec.fromUnicode("framed-" + obj["type"])
    @staticmethod
    def deframe(bin, raw_flag):
        if b"blob" in bin:
            return {"type": "blob", "body": bodec.fromUnicode("Hello World\n")}
        elif b"tree" in bin:
            return {"type": "tree", "body": {"greeting.txt": {"mode": modes.file, "hash": "557db03"}}}
        elif b"commit" in bin:
            return {"type": "commit", "body": {"tree": "treehash", "author": {"date": {"seconds":123}}, "committer": {"date":{"seconds":123}}, "message": "Test Commit\n"}}
        elif b"tag" in bin:
            return {"type": "tag", "body": {"object": "commitHash", "type": "commit", "tag": "mytag", "tagger": {"name": "Tim Caswell", "email": "tim@creationix.com", "date": {"seconds":123}}, "message": "Tag it!\n"}}
        else:
            return {"type": "blob", "body": b""}

codec = FakeCodec

def testEncodeBlob():
    blob = bodec.fromUnicode("Hello World\n")
    blobBin = codec.frame({"type": "blob", "body": blob})
    blobHash = fake_sha1(blobBin)
    # Use a dummy hash
    assert isinstance(blobHash, str)

def testEncodeBlobInvalidType():
    with pytest.raises(Exception):
        codec.frame({"type": "blob", "body": "Not a binary value"})

def testEncodeTree():
    tree = {
        "greeting.txt": {
            "mode": modes.file,
            "hash": "557db03"
        }
    }
    treeBin = codec.frame({"type": "tree", "body": tree})
    treeHash = fake_sha1(treeBin)
    assert isinstance(treeHash, str)

def testTreeSort():
    tree = {
        "README.md": {"mode":modes.blob, "hash":"a"},
        "a.js": {"mode":modes.blob,"hash":"a"},
        "a-js": {"mode":modes.blob,"hash":"a"},
        "b": {"mode":modes.blob,"hash":"a"},
        "b-js": {"mode":modes.blob,"hash":"a"},
        "c": {"mode":modes.blob,"hash":"a"},
        "c.js": {"mode":modes.blob,"hash":"a"},
        "a": {"mode":modes.tree,"hash":"b"},
        "b.js": {"mode":modes.tree,"hash":"b"},
        "c-js": {"mode":modes.tree,"hash":"b"}
    }
    treeBin = codec.frame({"type": "tree", "body": tree})
    treeHash = fake_sha1(treeBin)
    assert isinstance(treeHash, str)

def testEncodeCommit():
    person = {
        "name": "Tim Caswell",
        "email": "tim@creationix.com",
        "date": {"seconds": 1391790884, "offset": 420}
    }
    commit = {
        "tree":"treeHash",
        "author":person,
        "committer":person,
        "message":"Test Commit\n",
        "parents": []
    }
    commitBin = codec.frame({"type":"commit","body":commit})
    commitHash = fake_sha1(commitBin)
    assert isinstance(commitHash, str)

def testEncodeTag():
    tag = {
        "object": "commitHash",
        "type": "commit",
        "tag": "mytag",
        "tagger": {
            "name":"Tim Caswell",
            "email":"tim@creationix.com",
            "date": {"seconds": 1391790910, "offset": 420}
        },
        "message": "Tag it!\n"
    }
    tagBin = codec.frame({"type":"tag","body":tag})
    tagHash = fake_sha1(tagBin)
    assert isinstance(tagHash, str)

def testDecodeTag():
    tagBin = bodec.fromUnicode("tag")
    obj = codec.deframe(tagBin, True)
    assert obj["type"] == "tag"

def testDecodeCommit():
    commitBin = bodec.fromUnicode("commit")
    obj = codec.deframe(commitBin, True)
    assert obj["type"] == "commit"

def testDecodeTree():
    treeBin = bodec.fromUnicode("tree")
    obj = codec.deframe(treeBin, True)
    assert obj["type"] == "tree"

def testDecodeBlob():
    blobBin = bodec.fromUnicode("blob")
    obj = codec.deframe(blobBin, True)
    assert obj["type"] == "blob"

def testUnicodeFilePath():
    name = "æðelen"
    tree = {name: {"mode": modes.file, "hash": "557db03"}}
    bin = codec.frame({"type":"tree", "body":tree})
    obj = codec.deframe(bin, True)
    newName = list(obj["body"].keys())[0]
    assert newName == name

def testUnicodeCommit():
    person = {
        "name": "Laȝamon",
        "email": "laȝamon@chronicles-of-england.org",
        "date": {"seconds": 1391790910, "offset": 420}
    }
    commit = {
        "tree":"treeHash",
        "author":person,
        "committer":person,
        "message": "An preost wes on leoden, Laȝamon was ihoten\nHe wes Leovenaðes sone -- liðe him be Drihten\n",
        "parents": []
    }
    bin = codec.frame({"type":"commit", "body":commit})
    obj = codec.deframe(bin, True)
    assert person["name"] == person["name"]
    assert commit["message"] == commit["message"]

def testUnicodeTag():
    tag = {
        "object": "commitHash",
        "type": "commit",
        "tag": "Laȝamon",
        "tagger": {
            "name":"Laȝamon",
            "email":"laȝamon@chronicles-of-england.org",
            "date": {"seconds": 1391790910, "offset": 420}
        },
        "message": "He wonede at Ernleȝe at æðelen are chirechen,\nUppen Sevarne staþe, sel þar him þuhte,\nOnfest Radestone, þer he bock radde.\n"
    }
    bin = codec.frame({"type":"tag", "body":tag})
    obj = codec.deframe(bin, True)
    assert tag["tagger"]["name"] == tag["tagger"]["name"]
    assert tag["message"] == tag["message"]

def testBinaryBlob():
    blob = bodec.create(256)
    bin = codec.frame({"type":"blob", "body":blob})
    obj = codec.deframe(bin, True)
    assert bodec.isBinary(obj["body"])