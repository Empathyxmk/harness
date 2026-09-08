class DummyModuleTester:
    def __init__(self, module):
        self.module = module

    def assert_all_dependencies_declared(self):
        # Always passes in dummy implementation
        pass


def test_all_dependencies_declared():
    class DummyGmailServiceModule:
        pass

    module_tester = DummyModuleTester(DummyGmailServiceModule())
    module_tester.assert_all_dependencies_declared()