import unittest
from cloudconvert.job import Job

class TestJob(unittest.TestCase):
    def test_job_creation(self):
        # Example test
        job = Job()
        self.assertIsNotNone(job)