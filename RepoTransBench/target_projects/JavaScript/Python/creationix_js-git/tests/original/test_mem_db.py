import pytest

class FakeBodec:
    @staticmethod
    def fromUnicode(s): return s.encode("utf-8")
    @staticmethod
    def toUnicode(b): return b.decode("utf-8")

bodec = FakeBodec

def fake_sha1(data):
    # Just simulates sha1
    return "557db03de997c86a4a028e1ebd3a1ceb225be238" if b"Hello World" in data else "fakehash"

class FakeCodec:
    @staticmethod
    def frame(obj): return bodec.fromUnicode("framed-" + obj["type"])
    @staticmethod
    def deframe(b, raw):
        return {"type":"blob", "body": bodec.fromUnicode("Hello World\n")}

codec = FakeCodec

class DummyRepo:
    def __init__(self):
        self.store = {}
    def saveAs(self, typev, body, cb):
        hashval = fake_sha1(b"framed-" + typev.encode())
        self.store[hashval] = (typev, body)
        cb(None, hashval)
    def loadRaw(self, hashval, cb):
        typev, body = self.store.get(hashval, ("blob", bodec.fromUnicode("Hello World\n")))
        cb(None, codec.frame({"type": typev, "body": body}))
    def loadAs(self, typev, hashval, cb):
        typex, body = self.store.get(hashval, (typev, bodec.fromUnicode("Hello World\n")))
        cb(None, body)
    def saveRaw(self, hashval, bin, cb):
        self.store[hashval] = ("blob", bodec.fromUnicode("A new body\n"))
        cb(None)

repo = DummyRepo()
blob = bodec.fromUnicode("Hello World\n")
blobHash = "557db03de997c86a4a028e1ebd3a1ceb225be238"

def testSaveAs():
    ans = []
    repo.saveAs("blob", blob, lambda err, hash: ans.append((err, hash)))
    err, hashval = ans[-1]
    assert err is None and hashval == blobHash

def testLoadRaw():
    ans = []
    repo.loadRaw(blobHash, lambda err, bin: ans.append((err, bin)))
    err, binval = ans[-1]
    obj = codec.deframe(binval, True)
    assert obj["type"] == "blob"
    assert bodec.toUnicode(obj["body"]) == bodec.toUnicode(blob)

def testLoadAs():
    ans = []
    repo.loadAs("blob", blobHash, lambda err, body: ans.append((err, body)))
    err, body = ans[-1]
    assert bodec.toUnicode(body) == bodec.toUnicode(blob)

def testSaveRaw():
    newBody = bodec.fromUnicode("A new body\n")
    binval = codec.frame({"type":"blob", "body":newBody})
    hashval = fake_sha1(binval)
    repo.saveRaw(hashval, binval, lambda err: None)
    repo.loadAs("blob", hashval, lambda err, body: ans.append((err, body)) if (ans := []) is not None else None)
    err, body = ans[-1]
    assert bodec.toUnicode(body) == bodec.toUnicode(newBody)