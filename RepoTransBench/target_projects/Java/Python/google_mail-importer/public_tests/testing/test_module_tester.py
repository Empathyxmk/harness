def test_different_module_tester_runs():
    class ModuleTester:
        def test(self):
            return True

    tester = ModuleTester()
    assert tester.test() is True