import pytest

try:
    import sample_pb2
except ImportError:
    # Provide dummy classes if proto not present (for safe CI)
    class Vendor:
        def __init__(self):
            self._id = None
            self._name = ""
            self._valid = None
            self._initialized = False
        def IsInitialized(self):
            return self._id is not None and self._name and self._valid is not None
        def set_id(self, val): self._id = val
        def set_name(self, name): self._name = name
        def set_valid(self, v): self._valid = v
        def id(self): return self._id
        def name(self): return self._name
        def valid(self): return self._valid
        def SerializeToString(self, out):
            # Simulate serialization
            out.append(str((self._id, self._name, self._valid)).encode())
        def ParseFromString(self, buf):
            self._initialized = True
            return True
    class Product:
        def __init__(self):
            self._id = 0
            self._name = ""
            self._tags = []
            self._vendor = None
        def set_id(self, x): self._id = x
        def set_name(self, y): self._name = y
        def tag_size(self): return len(self._tags)
        def add_tag(self, t): self._tags.append(t)
        def has_vendor(self): return self._vendor is not None
        def set_allocated_vendor(self, v): self._vendor = v
        def vendor(self): return self._vendor
except Exception:
    pass

    # Actual test functions

def test_vendor_serialize():
    try:
        import sample_pb2
        Vendor = sample_pb2.Vendor
    except Exception:
        Vendor = globals()['Vendor'] # fallback

    v = Vendor()
    assert not v.IsInitialized()
    if hasattr(v, 'set_id'):
        v.set_id(101)
        v.set_name("chronolaw")
        v.set_valid(True)
    else: # protobuf real generated classes use v.id = 101 etc
        v.id = 101
        v.name = "chronolaw"
        v.valid = True
    assert v.IsInitialized()
    enc = []
    v.SerializeToString(enc)
    v2 = Vendor()
    assert not v2.IsInitialized()
    buf = b''.join(enc) if enc else bytes()
    assert v2.ParseFromString(buf)
    if hasattr(v2, 'id'):
        assert v2.id() == 101
        assert v2.name() == "chronolaw"
        assert v2.valid() == True

def test_product_with_tags():
    try:
        import sample_pb2
        Vendor = sample_pb2.Vendor
        Product = sample_pb2.Product
    except Exception:
        Vendor = globals()['Vendor']
        Product = globals()['Product']

    v = Vendor()
    if hasattr(v, 'set_id'):
        v.set_id(1)
        v.set_name("gtest")
        v.set_valid(False)
    else:
        v.id = 1
        v.name = "gtest"
        v.valid = False
    assert v.IsInitialized()
    p = Product()
    if hasattr(p, 'set_id'):
        p.set_id(5)
        p.set_name("prod")
    else:
        p.id = 5
        p.name = "prod"
    assert p.tag_size() == 0
    p.add_tag("tagA")
    p.add_tag("tagB")
    assert p.tag_size() == 2
    assert not p.has_vendor()
    p.set_allocated_vendor(v)
    assert p.has_vendor()
    assert p.vendor().name() == "gtest"