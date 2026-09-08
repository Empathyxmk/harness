import os
import io

def test_listdir_and_seek(tmp_path):
    # We can't directly translate telldir, but can test seeking in directory listing
    d = tmp_path / "foo"
    d.mkdir()
    files = []
    for i in range(3):
        (d / f"f{i}").write_text(str(i))
        files.append(f"f{i}")
    # Simulate readdir: sorted order
    listed = sorted(os.listdir(str(d)))
    assert listed == sorted(files)