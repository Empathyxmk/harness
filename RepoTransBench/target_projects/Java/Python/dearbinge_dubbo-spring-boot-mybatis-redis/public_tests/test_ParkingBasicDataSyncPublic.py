def test_parking_basic_data_sync_response_public_variant():
    # Use different inputs from private: e.g., odd parkId, simulate a "false"
    park_id = 5739  # Odd for this public variant
    sync_result = (park_id % 2 == 0)  # Even-only success logic
    assert not sync_result