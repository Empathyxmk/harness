def test_image_deps_from_other_modules_public():
    major = 2
    minor = 6
    assert major + minor == 8
    assert minor % 2 == 0
    assert not (major < 2)