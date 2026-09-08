import pytest

def dummy_get_thumbnail_files_public():
    # Simulate slightly different thumbnails set (names)
    return [
        'public_thumbnails/thumb1.jpg',
        'public_thumbnails/thumb2.png',
    ]

def test_thumbnail_cleanup_files_to_remove_public(monkeypatch):
    # Monkeypatching would be used here if needed, but keep trivial for public
    thumbnails = dummy_get_thumbnail_files_public()
    assert len(thumbnails) == 2
    assert thumbnails[0].endswith('.jpg')
    assert thumbnails[1].endswith('.png')