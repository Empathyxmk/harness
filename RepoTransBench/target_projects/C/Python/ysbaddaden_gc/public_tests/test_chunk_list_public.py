class DummyChunk:
    def __init__(self):
        self.next = None

class ChunkList:
    def __init__(self):
        self.items = []
    def push(self, chunk):
        if self.items:
            self.items[-1].next = chunk
        chunk.next = None
        self.items.append(chunk)

    def remove(self, chunk):
        idx = self.items.index(chunk)
        if idx > 0:
            self.items[idx-1].next = chunk.next
        self.items.remove(chunk)

    def length(self):
        return len(self.items)

    def first(self):
        return self.items[0] if self.items else None

    def last(self):
        return self.items[-1] if self.items else None

def test_ChunkList_init_push_remove_public():
    clist = ChunkList()
    chunkA, chunkB, chunkC, chunkD = DummyChunk(), DummyChunk(), DummyChunk(), DummyChunk()

    clist.push(chunkA)
    clist.push(chunkB)
    clist.push(chunkC)
    clist.push(chunkD)

    assert clist.length() == 4
    assert clist.first() is chunkA
    assert clist.last() is chunkD

    clist.remove(chunkC)
    assert clist.length() == 3
    clist.remove(chunkA)
    assert clist.length() == 2
    clist.remove(chunkD)
    assert clist.length() == 1
    assert clist.first() is chunkB
    assert clist.last() is chunkB
    clist.remove(chunkB)
    assert clist.length() == 0
    assert clist.first() is None
    assert clist.last() is None