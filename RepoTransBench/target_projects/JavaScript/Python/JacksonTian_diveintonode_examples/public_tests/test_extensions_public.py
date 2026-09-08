import os

def test_require_with_different_extension_public():
    # Simulate checking extension of a file path in Python
    file = './02/module/hello.js'
    ext = os.path.splitext(file)[1]
    assert ext == '.js'
    assert file.endswith('.js')
    # lower-case handling
    assert os.path.splitext('SAMPLE.LOWeR.Js')[1].lower() == '.js'