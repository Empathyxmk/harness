import logging
from claude_to_chatgpt.logger import get_logger

def test_public_get_logger_level():
    # Different logger name
    logger = get_logger("publicLoggerTest")
    assert isinstance(logger, logging.Logger)
    # Level should default to WARNING or lower, but try change to ERROR to check setLevel
    logger.setLevel(logging.ERROR)
    assert logger.level == logging.ERROR or logger.getEffectiveLevel() == logging.ERROR

def test_public_get_logger_name():
    # Different logger name string
    logger_name = "unique_logger_name"
    logger = get_logger(logger_name)
    assert logger.name == logger_name