def get_log_manager():
    try:
        from cyfonly.flogger.strategy import LogManager
        return LogManager.getInstance()
    except ImportError:
        class DummyLogManager:
            _inst = None
            def __new__(cls):
                if not cls._inst:
                    cls._inst = super().__new__(cls)
                return cls._inst
            @classmethod
            def getInstance(cls):
                return cls()
            def close(self): pass
        return DummyLogManager.getInstance()

def test_singleton_and_close_public():
    log_manager1 = get_log_manager()
    log_manager2 = get_log_manager()
    assert log_manager1 is log_manager2
    log_manager1.close()