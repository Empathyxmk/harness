import pytest

class LevelDBError(Exception):
    pass

class DummyFilterPolicy:
    def __init__(self):
        self.calls = []
    def create_filter(self, keys):
        self.calls.append(('create_filter', keys))
        return b'filter'
    def key_may_match(self, key, filter_data):
        self.calls.append(('key_may_match', key, filter_data))
        return True

class DummyWriteBatch:
    def __init__(self):
        self.ops = []

    def put(self, key, value):
        self.ops.append(('put', key, value))

    def delete(self, key):
        self.ops.append(('delete', key))

    def iterate(self, db):
        for op in self.ops:
            if op[0] == 'put':
                db[op[1]] = op[2]
            elif op[0] == 'delete':
                if op[1] in db:
                    del db[op[1]]
        # simulate callback API, but for test we check state after

class DummyIterator:
    def __init__(self, data, snapshot=None):
        # snapshot is ignored in this dummy
        self.items = sorted(data.items())
        self.pos = -1 if not self.items else 0
        self.valid = bool(self.items)

    def seek_to_first(self):
        self.pos = 0 if self.items else -1
        self.valid = bool(self.items)

    def seek_to_last(self):
        self.pos = len(self.items)-1 if self.items else -1
        self.valid = bool(self.items)

    def seek(self, key):
        # Find equal or next greater key
        self.pos = -1
        for i, (k, v) in enumerate(self.items):
            if k >= key:
                self.pos = i
                break
        self.valid = self.pos != -1

    def next(self):
        if not self.valid: return
        if self.pos+1 < len(self.items):
            self.pos += 1
        else:
            self.valid = False

    def prev(self):
        if not self.valid: return
        if self.pos > 0:
            self.pos -= 1
        else:
            self.valid = False

    def key(self):
        if self.valid and self.pos != -1:
            return self.items[self.pos][0]
        raise LevelDBError("Iterator not valid: no key")

    def value(self):
        if self.valid and self.pos != -1:
            return self.items[self.pos][1]
        raise LevelDBError("Iterator not valid: no value")

    def is_valid(self):
        return self.valid

class DummyLevelDB:
    def __init__(self, filter_policy=None):
        self.data = {}
        self.filter_policy = filter_policy or DummyFilterPolicy()
        self.snapshots = []
        self.closed = False

    def put(self, key, value, sync=False):
        if self.closed:
            raise LevelDBError("DB closed")
        self.data[key] = value

    def get(self, key, snapshot=None):
        if self.closed:
            raise LevelDBError("DB closed")
        # In dummy, ignores snapshot
        if key in self.data:
            return self.data[key]
        else:
            raise KeyError("NotFound")

    def delete(self, key, sync=False):
        if self.closed:
            raise LevelDBError("DB closed")
        if key in self.data:
            del self.data[key]
        # in C leveldb NotFound is also 'success'

    def write(self, batch, sync=False):
        if self.closed:
            raise LevelDBError("DB closed")
        batch.iterate(self.data)

    def iterator(self, snapshot=None):
        return DummyIterator(self.data, snapshot)

    def get_snapshot(self):
        snap = dict(self.data)
        self.snapshots.append(snap)
        return snap

    def release_snapshot(self, snapshot):
        if snapshot in self.snapshots:
            self.snapshots.remove(snapshot)

    def get_property(self, prop):
        known = {
            "leveldb.stats": "Dummy stats",
            "leveldb.sstables": "0 files",
            "leveldb.approximate-memory-usage": str(len(self.data)),
        }
        return known.get(prop, None)

    def get_approximate_sizes(self, ranges):
        # Each range is a (start, limit) tuple
        result = []
        for start, limit in ranges:
            count = sum(1 for k in self.data if start <= k < limit)
            result.append(count)  # fake size by num keys in range
        return result

    def close(self):
        self.closed = True

# ==== TEST SUITE ====
def test_simple_operations():
    db = DummyLevelDB()
    # Put and get
    db.put(b'a', b'val0')
    db.put(b'b', b'val1')
    assert db.get(b'a') == b'val0'
    assert db.get(b'b') == b'val1'
    # Overwrite
    db.put(b'a', b'VAL0')
    assert db.get(b'a') == b'VAL0'
    # Delete key
    db.delete(b'b')
    with pytest.raises(KeyError):
        db.get(b'b')
    # Delete non-existent key is a no-op
    db.delete(b'q')

def test_iterator_iteration():
    db = DummyLevelDB()
    for key in [b'a', b'b', b'c', b'd']:
        db.put(key, bytes([key[0]+1]))

    it = db.iterator()
    # Forward order
    it.seek_to_first()
    keys = []
    while it.is_valid():
        keys.append(it.key())
        it.next()
    assert keys == [b'a', b'b', b'c', b'd']

    # Seek to 'b'
    it.seek(b'b')
    assert it.key() == b'b'
    it.next()
    assert it.key() == b'c'
    it.next()
    assert it.key() == b'd'
    it.next()
    assert not it.is_valid()

    # Seek past last
    it.seek(b'x')
    assert not it.is_valid()

    # Backwards order
    it.seek_to_last()
    bwd = []
    while it.is_valid():
        bwd.append(it.key())
        it.prev()
    assert bwd == [b'd', b'c', b'b', b'a']

def test_write_batch():
    db = DummyLevelDB()
    db.put(b'x', b'odd')
    batch = DummyWriteBatch()
    batch.put(b'a', b'vala')
    batch.put(b'b', b'valb')
    batch.delete(b'x')
    db.write(batch)
    assert db.get(b'a') == b'vala'
    assert db.get(b'b') == b'valb'
    with pytest.raises(KeyError):
        db.get(b'x')

def test_snapshot_simulation():
    db = DummyLevelDB()
    db.put(b'a', b'A")
    db.put(b'b', b"B")
    snap = db.get_snapshot()
    db.put(b'a', b"X")
    # simulate snapshot - it should not see new 'X'
    assert snap[b'a'] == b'A'
    assert snap[b'b'] == b'B'
    assert db.get(b'a') == b'X'
    assert db.get(b'b') == b'B'
    db.release_snapshot(snap)

def test_approximate_size_and_property():
    db = DummyLevelDB()
    # Fill some keys
    for i in range(100):
        db.put(bytes([i]), bytes([i+1]))
    size = db.get_approximate_sizes([(b'\x00', b'\x7F'), (b'\x80', b'\xFF')])
    # Should have many in first, few in second
    assert sum(size) <= 100
    assert db.get_property("leveldb.stats").startswith("Dummy")
    assert db.get_property("leveldb.approximate-memory-usage").isdigit()

def test_filter_policy_calls():
    filter_policy = DummyFilterPolicy()
    db = DummyLevelDB(filter_policy)
    db.put(b"x", b"1")
    filt = filter_policy.create_filter([b"x"])
    assert filt == b"filter"
    ok = filter_policy.key_may_match(b"x", filt)
    assert ok is True
    # check calls were logged
    assert ('create_filter', [b"x"]) in filter_policy.calls
    assert ('key_may_match', b"x", b"filter") in filter_policy.calls

def test_error_on_closed_db():
    db = DummyLevelDB()
    db.put(b'A', b"B")
    db.close()
    with pytest.raises(LevelDBError):
        db.put(b'A', b"C")
    with pytest.raises(LevelDBError):
        db.get(b'A')
    with pytest.raises(LevelDBError):
        db.delete(b'A')
    with pytest.raises(LevelDBError):
        batch = DummyWriteBatch()
        db.write(batch)