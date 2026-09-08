from shshsh import Sh

def test_public_redirect_stdout(tmp_path):
    # Use a different filename
    f = tmp_path / "pub_file.txt"
    Sh("echo 8765") > str(f)
    content = f.read_text()
    assert "8765" in content