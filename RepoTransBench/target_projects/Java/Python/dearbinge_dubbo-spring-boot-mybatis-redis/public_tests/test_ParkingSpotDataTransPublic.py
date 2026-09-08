def test_alternative_parking_spot_trans():
    # Different inputs from private: new spotId, different lat/lng.
    spot_id = "PUBLIC_SPOT_102"
    lat = 35.1234
    lng = 135.4321

    # Simulate test logic
    result = spot_id + "_" + str(abs(lat - lng))
    assert result == "PUBLIC_SPOT_102_100.3087"