def test_geohash_private_constructor():
    class GeoHash:
        def __new__(cls):
            return super().__new__(cls)
    g = GeoHash()
    assert isinstance(g, GeoHash)