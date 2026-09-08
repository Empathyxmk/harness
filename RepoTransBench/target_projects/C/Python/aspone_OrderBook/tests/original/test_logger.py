import pytest
from src.aspone_orderbook.logger import Logger
import time
import sys

def test_logger_basic(capfd):
    logger = Logger()
    logger.print("hello\n")
    logger.print("world\n")
    # Give the logger time to spawn, queue, and run
    time.sleep(0.06) # 60 milliseconds
    logger.stop_logger()

    captured = capfd.readouterr()
    assert "hello\nworld\n" == captured.out

def test_logger_destructor_on_unused():
    # In Python, __del__ is called when object is garbage collected.
    # We create a logger and then let it go out of scope.
    logger = Logger()
    # No explicit stop_logger() or print() call.
    # The __del__ method should handle stopping the thread cleanly without crashing.
    # We can explicitly delete the object to force garbage collection for test.
    del logger
    time.sleep(0.1) # Give destructor/thread cleanup time

    # This test primarily verifies no crash/error,
    # captured output should be empty as no prints were made.
    # capfd.readouterr() would show nothing relevant.

def test_logger_multiple(capfd):
    logger = Logger()
    logger.print("Msg1\n")
    logger.print("Msg2\n")
    time.sleep(0.03) # 30 milliseconds
    logger.print("Msg3\n")
    time.sleep(0.02) # 20 milliseconds
    logger.stop_logger()

    captured = capfd.readouterr()
    assert "Msg1\nMsg2\nMsg3\n" == captured.out