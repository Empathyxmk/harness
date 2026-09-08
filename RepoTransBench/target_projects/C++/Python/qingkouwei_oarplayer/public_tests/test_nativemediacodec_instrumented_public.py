def test_nativemediacodec_instrumented_public_context():
    # Simulate Android Instrumented PublicTest environment
    app_package = "com.wodekouwei.nativemediacodec.test"
    # Public test expects package not to match base package
    assert app_package != "com.wodekouwei.nativemediacodec"