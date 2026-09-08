import pytest

class CpuMetricSender:
    @staticmethod
    def getTaskManagerPidList():
        # Simulated list
        return [1234, 5678, 91011]

def test_get_task_manager_pid(capsys):
    result = CpuMetricSender.getTaskManagerPidList()
    print(result)
    assert isinstance(result, list)
    assert all(isinstance(pid, int) for pid in result)