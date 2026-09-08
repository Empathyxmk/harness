def test_require_source():
    # Simulate importing all modules. If import fails, this will throw.
    import d3polygon.area
    import d3polygon.centroid
    import d3polygon.contains
    import d3polygon.cross
    import d3polygon.hull
    import d3polygon.index
    import d3polygon.length
    assert True