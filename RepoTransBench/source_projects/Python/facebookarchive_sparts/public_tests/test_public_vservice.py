from sparts.vservice import VService

def test_public_tasks_attribute():
    class PubTestService(VService):
        TASKS = ['task1', 'task2']
    assert PubTestService.TASKS == ['task1', 'task2']

def test_public_initFromCLI_exists():
    # Just check the method is present
    assert hasattr(VService, "initFromCLI")
    assert callable(VService.initFromCLI)