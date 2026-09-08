import pytest
from src.log4j import Log4j, ThreadContext

class TestLog4j:
    def setup_method(self, method):
        ThreadContext.clearAll()

    def teardown_method(self, method):
        ThreadContext.clearAll()

    def test_configure_logger_with_thread_context(self, capsys):
        Log4j.configureLoggerWithThreadContext()
        class DummyLogger:
            def error(self, msg):
                tc_items = ThreadContext.items()
                prefix = ''
                if tc_items:
                    prefix = ' '.join(v for (k, v) in tc_items)
                print(f"{prefix} {msg}".strip())
        logger = DummyLogger()
        ThreadContext.put("header", "TEST_HEADER")
        logger.error("Error message!")
        out = capsys.readouterr().out
        assert "TEST_HEADER" in out
        assert "Error message!" in out

    def test_main_with_thread_local_attack(self, capsys):
        Log4j.main(['-t'])
        out = capsys.readouterr().out
        assert "Will use ThreadContext as attack vector" in out
        assert "Vulnerable through thread context - 1" in out
        assert "Vulnerable through thread context - 2" in out

    def test_main_without_thread_local_attack(self, capsys):
        Log4j.main([])
        out = capsys.readouterr().out
        assert "jndi:ldap://127.0.0.1:1389/a" in out
        assert "${jndi:" in out