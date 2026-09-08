import pytest
from src.aspone_orderbook.logger import Logger
import time
import sys

def test_public_logger_basic(capfd):
    logger = Logger()
    logger.print("foo\n")
    logger.print("bar\n")
    time.sleep(0.08) # 80 milliseconds, different duration
    logger.stop_logger()

    captured = capfd.readouterr()
    assert "foo\nbar\n" == captured.out

def test_public_logger_destructor_on_unused():
    logger = Logger()
    del logger
    time.sleep(0.1) # Give destructor/thread cleanup time

def test_public_logger_multiple(capfd):
    logger = Logger()
    logger.print("Alpha\n")
    logger.print("Beta\n")
    time.sleep(0.04) # 40 milliseconds
    logger.print("Gamma\n")
    time.sleep(0.015) # 15 milliseconds
    logger.stop_logger()

    captured = capfd.readouterr()
    assert "Alpha\nBeta\nGamma\n" == captured.out