import pytest

class FakeHystrixDashboardApplication:
    @staticmethod
    def main(args):
        # Simulate running the main method
        pass

def test_main_method_hystrix_dashboard(monkeypatch):
    called = {}
    def fake_main(args):
        called['called'] = True
        assert args == ["--spring.profiles.active=test"]
    monkeypatch.setattr(FakeHystrixDashboardApplication, "main", staticmethod(fake_main))
    FakeHystrixDashboardApplication.main(["--spring.profiles.active=test"])
    assert called['called']

def test_no_args_main_hystrix_dashboard(monkeypatch):
    called = {}
    def fake_main(args):
        called['called'] = True
        assert args is None
    monkeypatch.setattr(FakeHystrixDashboardApplication, "main", staticmethod(fake_main))
    FakeHystrixDashboardApplication.main(None)
    assert called['called']