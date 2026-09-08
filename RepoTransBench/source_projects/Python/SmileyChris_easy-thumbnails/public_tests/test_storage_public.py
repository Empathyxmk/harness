import pytest
from easy_thumbnails.storage import generate_filename

def test_generate_filename_unique_string_public():
    # Different test value and structure
    path = generate_filename('pictures/avatars/alice.png', 'custom_id_54321')
    assert path.startswith('pictures/avatars/')
    assert 'custom_id_54321' in path or path.endswith('_alice.png')

def test_generate_filename_extension_public():
    # Non-png extension to ensure robustness
    path = generate_filename('pictures/backgrounds/image123.gif', 'id_777')
    assert path.endswith('_image123.gif')
    assert 'id_777' in path or 'image123' in path