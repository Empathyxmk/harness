import pytest
import platform
import sys

class JavaSpecification:
    def __init__(self, version):
        self.version = version

    def get_version(self):
        return self.version

class OperationSystem:
    def __init__(self, name, arch):
        self.name = name
        self.arch = arch

    def get_name(self):
        return self.name

    def get_architecture(self):
        return self.arch

class TestsEnvironment:
    def __init__(self, java_specification, operation_system):
        self.java_specification = java_specification
        self.operation_system = operation_system

    def is_windows(self):
        return 'Windows' in self.operation_system.get_name()

    def is_amd64_architecture(self):
        return self.operation_system.get_architecture() == "amd64"

    def get_java_version(self):
        return self.java_specification.get_version()

class SUT:
    def __init__(self):
        self.jobs = []
    def has_job_to_run(self):
        return len(self.jobs) > 0
    def run(self, job=None):
        if job:
            self.jobs.append(job)

class Job: pass

@pytest.fixture
def environment():
    java_spec = JavaSpecification(platform.python_version())
    os_name = platform.system()
    os_arch = "amd64" if sys.maxsize > 2**32 else "x86"
    op_sys = OperationSystem(os_name, os_arch)
    return TestsEnvironment(java_spec, op_sys)

@pytest.fixture
def system_under_test():
    return SUT()

@pytest.mark.skipif(not platform.system().startswith('Windows'), reason="Test assumes Windows OS")
def test_no_job_to_run(environment, system_under_test):
    # only run test if environment.is_windows() returns True
    if not environment.is_windows():
        pytest.skip("not Windows")

    # assume the version check is always false for demonstration
    if environment.get_java_version() == "1.8":
        assert not system_under_test.has_job_to_run()
    else:
        assert True  # Skips assumption?

@pytest.mark.skipif(not (platform.system().startswith('Windows') and (sys.maxsize > 2**32)), reason="Test assumes AMD64 on Windows")
def test_job_to_run(environment, system_under_test):
    if not (environment.is_windows() and environment.is_amd64_architecture()):
        pytest.skip("not Windows/amd64")
    system_under_test.run(Job())
    assert system_under_test.has_job_to_run()