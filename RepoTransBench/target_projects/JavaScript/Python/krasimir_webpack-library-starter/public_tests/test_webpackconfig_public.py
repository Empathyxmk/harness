def test_webpackconfig_has_devtool_string():
    config = {
        'mode': 'development',
        'entry': './src/index.js',
        'output': {
            'filename': 'library.amd.min.js',
            'libraryTarget': 'umd',
        },
        'devtool': 'source-map'
    }
    assert "devtool" in config
    assert isinstance(config['devtool'], str)

def test_webpackconfig_output_librarytarget_umd_and_valid_mode():
    config = {
        'mode': 'development',
        'entry': './src/index.js',
        'output': {
            'filename': 'library.amd.min.js',
            'libraryTarget': 'umd',
        },
        'devtool': 'source-map'
    }
    assert config['output']['libraryTarget'] == "umd"
    assert config['entry'].endswith('/src/index.js')
    assert config['mode'] in ['development', 'production']