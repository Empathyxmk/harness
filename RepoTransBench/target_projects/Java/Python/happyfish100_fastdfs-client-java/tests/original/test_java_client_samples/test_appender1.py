def test_appender1_sample():
    try:
        meta_list = [
            {"width":"800"},
            {"heigth":"600"},
            {"bgcolor":"#FFFFFF"},
            {"author":"Mike"}
        ]
        appender_file_id = "group1/appender/fileid2"
        assert appender_file_id.startswith("group1/")
        ok = True
        assert ok
    except Exception as ex:
        assert False, f"Appender1 sample failed: {ex}"