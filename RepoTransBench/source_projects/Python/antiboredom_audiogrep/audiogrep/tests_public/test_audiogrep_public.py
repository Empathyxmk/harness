import audiogrep

def test_get_files_public(tmp_path):
    # Using different filenames/extensions than original
    a = tmp_path / "file1.aac"
    b = tmp_path / "file2.m4a"
    c = tmp_path / "file3.txt"
    for f in [a, b, c]:
        f.write_text("test abc")

    # Should only get audio files
    fs = set(audiogrep.get_files(str(tmp_path), [".aac", ".m4a"]))
    expected = {str(a), str(b)}
    assert fs == expected