from d3polygon import polygon_area, polygon_centroid, polygon_contains, polygon_hull, polygon_length

def test_d3polygon_exports_main_polygon_methods():
    # All are callable
    for func in [polygon_area, polygon_centroid, polygon_contains, polygon_hull, polygon_length]:
        assert callable(func)