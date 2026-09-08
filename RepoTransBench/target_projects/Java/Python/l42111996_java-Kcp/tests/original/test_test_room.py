def test_test_room_packid_count():
    class TpsChannelServerCache:
        def __init__(self, n): self._packids = list(range(n))
        def size(self): return len(self._packids)
        def getSendPackIds(self): return list(self._packids)
    class Ukcp:
        def __init__(self, cache): self._cache = cache
        def user(self):
            class User:
                def getCache(_): return self._cache
            return User()
        def write(self, bb): return True
    class TestRoom:
        def __init__(self):
            self.ukcps = []
        def run(self):
            packIdCount = sum([u.user().getCache().size() for u in self.ukcps])
            return packIdCount
    # Create a room with two clients of 5 packids each
    room = TestRoom()
    room.ukcps.append(Ukcp(TpsChannelServerCache(5)))
    room.ukcps.append(Ukcp(TpsChannelServerCache(5)))
    assert room.run() == 10