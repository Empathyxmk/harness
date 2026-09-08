def test_filter_folders():
    # folders: "folder1", "@folder2", "!folder3"
    folders = [
        {"name": "folder1", "full_name": "folder1"},
        {"name": "@folder2", "full_name": "@folder2"},
        {"name": "!folder3", "full_name": "!folder3"}
    ]

    expected = [folders[0], folders[2]]

    def filter_folders(folder_list):
        return [f for f in folder_list if not f['name'].startswith("@")]

    filtered = filter_folders(folders)
    # Simulate assertThat(filteredFolders).containsExactlyElementsIn(expectedFolders)
    assert filtered == expected


def test_create_local_message():
    # Simulate message in ThunderbirdMailStorage
    message = {"folder": {"full_name": "/abc/root/xyz/pdq.sbd", "name": "pdq.sbd"}}
    root_folder = {"full_name": "/abc/root"}

    def create_local_message(msg):
        full_name = msg["folder"]["full_name"]
        root_name = root_folder["full_name"]
        suffix = full_name[len(root_name):]
        if suffix.startswith('/'):
            suffix = suffix[1:]
        # Remove ".sbd"
        if suffix.endswith('.sbd'):
            suffix = suffix[:-4]
        folders = [suffix.replace(".sbd", "")]
        return folders

    folders = create_local_message(message)
    assert folders == ["xyz/pdq"]