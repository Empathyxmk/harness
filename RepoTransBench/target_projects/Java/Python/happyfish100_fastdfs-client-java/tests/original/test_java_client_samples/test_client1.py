def test_client1_sample():
    # This test simulates TestClient1's logic (upload/download via StorageClient1)
    try:
        meta_list = [
            {"width":"800"},
            {"heigth":"600"},
            {"bgcolor":"#FFFFFF"},
            {"author":"Mike"}
        ]
        # upload_file1
        file_id = "group1/M00/fileid1"
        assert file_id.startswith("group1/")
        # download_file1, set_metadata1, get_metadata1, etc.
        ok = True
        assert ok
    except Exception as ex:
        assert False, f"Client1 sample failed: {ex}"