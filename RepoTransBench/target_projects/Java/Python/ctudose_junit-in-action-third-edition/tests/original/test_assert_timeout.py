import pytest
import time

class Job:
    def __init__(self, name):
        self.name = name

class SUT:
    def __init__(self, name):
        self.jobs = []
        self.name = name

    def add_job(self, job):
        self.jobs.append(job)

    def run(self, duration):
        if not self.jobs:
            # This mimics the assertion in test; should raise in a different test
            raise ValueError("No jobs to run")
        time.sleep(duration / 1000.0)  # duration in milliseconds

@pytest.mark.timeout(0.5)
def test_timeout():
    system_under_test = SUT("Our system under test")
    system_under_test.add_job(Job("Job 1"))
    system_under_test.run(200)

@pytest.mark.timeout(0.5)
def test_timeout_preemptively():
    system_under_test = SUT("Our system under test")
    system_under_test.add_job(Job("Job 1"))
    system_under_test.run(200)