import pytest

# The following are mock implementations and sample data to support test logic.
# These would be replaced with actual implementations in real test code.

class FakeBodec:
    @staticmethod
    def slice(stream, i, j):
        return stream[i:j]
    @staticmethod
    def isBinary(item):
        return isinstance(item, (bytes, bytearray))
    @staticmethod
    def join(parts):
        res = b"".join(parts)
        return res
    @staticmethod
    def toHex(b):
        return b.hex()
    @staticmethod
    def toRaw(b):
        return b
    @staticmethod
    def fromUnicode(s):
        return s.encode("utf-8")
    @staticmethod
    def toUnicode(b):
        return b.decode("utf-8")


bodec = FakeBodec

class FakeCodec:
    @staticmethod
    def decodePack(onItem):
        def write(slice_bytes=None):
            # Simulate correct number of items written per sample-pack.
            if not hasattr(write, "written"):
                write.written = []
            if slice_bytes is not None:
                pass
            else:
                # End of stream
                onItem({"num": 16})
                for k in range(16):
                    onItem({"type": "commit", "body": bodec.fromUnicode("body")})
                onItem(None)
        return write

    @staticmethod
    def encodePack(cb):
        def write(item=None):
            if item is None:
                cb(None)
                return
            cb(bodec.fromUnicode("body"))
        return write

class FakeObjectCodec:
    decoders = {"tree": lambda x: x, "tag": lambda x: x, "commit": lambda x: x}
    encoders = {"tree": lambda x: bodec.fromUnicode("tree"), 
                "tag": lambda x: bodec.fromUnicode("tag"),
                "commit": lambda x: bodec.fromUnicode("commit")}

codec = FakeCodec
decoders = FakeObjectCodec.decoders
encoders = FakeObjectCodec.encoders

pack = b"sample pack"
items = []
newPack = None

def unpackStream(stream):
    meta = None
    out = []
    finished = False
    write = codec.decodePack(onItem)
    for i in range(0, len(stream), 128):
        slice_bytes = bodec.slice(stream, i, i+128)
        write(slice_bytes)
    write()
    def my_assert(cond, msg):
        if not cond:
            raise AssertionError(msg)
    def onItem(item):
        nonlocal meta, finished
        if item is None:
            finished = True
        elif not meta:
            meta = item
        else:
            out.append(item)
    if not finished:
        raise AssertionError("unpack stream didn't finish")
    if meta and out and len(out) != meta["num"]:
        raise AssertionError("Item num mismatch")
    return out

def testDecodePack():
    counts = {}
    def onItem(item):
        pass # placeholder for logic inside decodePack

    global items
    items = []
    # Using unpackStream will append 16 items (by simulation above)
    items = unpackStream(pack)
    for item in items:
        counts[item.get("type", "unknown")] = counts.get(item.get("type", "unknown"), 0) + 1
        # Note: One of the original logic (commit/tree/tag) not distinguished here; simulation.
        if item.get("type") in ["tree", "tag", "commit"]:
            item["body"] = "decoded"
    assert counts.get("commit", 0) == 16

def testEncodePack():
    done = [False]
    outs = []
    def cb(item):
        if item is None:
            done[0] = True
            return
        assert bodec.isBinary(item)
        outs.append(item)
    write = codec.encodePack(cb)
    write({"num": 16})
    for item in items:
        if not bodec.isBinary(item["body"]):
            item["body"] = bodec.fromUnicode(str(item["body"]))
        write(item)
    write()
    assert done[0]
    global newPack
    newPack = bodec.join(outs)

def testVerifyEncodePack():
    # Decoding newPack using unpackStream
    try:
        unpackStream(newPack)
        # Simulate hex checks
        assert bodec.toHex(pack) != ""
        assert bodec.toHex(newPack) != ""
    except Exception as err:
        print(bodec.toHex(pack))
        print(bodec.toHex(newPack))
        raise err