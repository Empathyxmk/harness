from tests.original.test_get_polyline import getPolyline

def test_decode_polyline_different_coords_public():
    test_polyline = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
    result = getPolyline.decode_poly(test_polyline)
    assert len(result) >= 2