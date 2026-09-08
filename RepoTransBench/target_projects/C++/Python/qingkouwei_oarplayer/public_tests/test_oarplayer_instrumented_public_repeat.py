def test_oarplayer_instrumented_public_repeat_context():
    # additional public test for repeated file in summary
    app_package = "com.wodekouwei.srsrtmpplayer.test"
    # Public test expects package not to match base package
    assert app_package != "com.wodekouwei.srsrtmpplayer"