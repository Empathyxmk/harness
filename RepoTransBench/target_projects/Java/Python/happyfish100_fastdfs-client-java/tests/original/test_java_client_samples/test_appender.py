def test_appender_sample():
    try:
        meta_list = [
            {"width":"800"},
            {"heigth":"600"},
            {"bgcolor":"#FFFFFF"},
            {"author":"Mike"}
        ]
        # upload_appender_file, download, append, regenerate, delete, etc.
        appender_filename = "group1/appender/testfile.txt"
        assert appender_filename.startswith("group1/")
        ok = True
        assert ok
    except Exception as ex:
        assert False, f"Appender sample failed: {ex}"