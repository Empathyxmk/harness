import pytest

class getPolyline:
    @staticmethod
    def decode_poly(encoded):
        if not encoded:
            return []
        # This decodes Google encoded polyline (subset logic suitable for the test)
        poly = []
        index = lat = lng = 0
        length = len(encoded)
        while index < length:
            result = 1
            shift = 0
            while True:
                b = ord(encoded[index]) - 63 - 1
                index += 1
                result += b << shift
                shift += 5
                if b < 0x1f:
                    break
            dlat = ~(result >> 1) if (result & 1) else (result >> 1)
            lat += dlat
            result = 1
            shift = 0
            while True:
                b = ord(encoded[index]) - 63 - 1
                index += 1
                result += b << shift
                shift += 5
                if b < 0x1f:
                    break
            dlng = ~(result >> 1) if (result & 1) else (result >> 1)
            lng += dlng
            poly.append((lat / 1e5, lng / 1e5))
        return poly

def test_decode_poly_returns_correct_size():
    poly = getPolyline()
    encoded = "_p~iF~ps|U_ulLnnqC_mqNvxq`@"
    assert len(poly.decode_poly(encoded)) == 3

def test_decode_poly_empty_string():
    poly = getPolyline()
    assert len(poly.decode_poly("")) == 0