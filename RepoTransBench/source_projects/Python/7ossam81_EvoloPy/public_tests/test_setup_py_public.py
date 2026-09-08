import os

def test_readme_exists_and_not_empty_public():
    assert os.path.exists("README.md")
    with open("README.md") as f:
        content = f.read()
    assert len(content.strip()) > 10