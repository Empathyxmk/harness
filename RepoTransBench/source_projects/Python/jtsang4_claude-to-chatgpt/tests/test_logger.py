def test_logger_importable():
    # Just test that the logger object exists and is a logger
    from claude_to_chatgpt.logger import logger
    import logging
    assert isinstance(logger, logging.Logger)