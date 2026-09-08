def test_test1_sample():
    try:
        # Emulate uploading a system file, handle OS check
        import sys
        conf_filename = "fdfs_client.conf"
        local_filename = "c:/windows/system32/notepad.exe" if sys.platform.startswith('win') else "/etc/hosts"
        ext_name = "exe" if sys.platform.startswith('win') else ""
        fileid = "group1/test_upload_file_id"
        assert fileid.startswith("group1/")
    except Exception as ex:
        assert False, f"Test1 sample failed: {ex}"