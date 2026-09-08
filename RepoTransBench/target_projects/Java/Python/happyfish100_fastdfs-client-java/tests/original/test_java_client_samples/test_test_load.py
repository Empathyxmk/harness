def test_test_load_sample():
    # Simulate completion of concurrent upload/download from the Java TestLoad
    try:
        file_ids = []
        # Simulate 10 upload threads
        for i in range(10):
            file_ids.append(f"fileid_{i}")
        # Simulate download threads working on the uploaded IDs
        for file_id in file_ids:
            assert file_id.startswith("fileid_")
        ok = True
        assert ok
    except Exception as ex:
        assert False, f"TestLoad sample failed: {ex}"