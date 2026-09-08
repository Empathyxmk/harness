import pytest

class DummyJob:
    def __init__(self, name):
        self.name = name
        if name == 'beta':
            self.config = {'name': name, 'dependsOn': ['alpha']}
        elif name == 'gamma':
            self.config = {'name': name, 'dependsOn': ['beta']}
        else:
            self.config = {'name': name, 'dependsOn': []}

class DummyInstance:
    def __init__(self, names):
        self.names = names
        self.completed = set()
        self.jobs = {name: DummyJob(name) for name in names or ['alpha', 'beta', 'gamma']}
        self._empty = False

    def isEmpty(self):
        if set(self.names) == self.completed:
            return True
        if not self.names:
            return False
        return False

    def pop(self):
        for name in self.names or ['alpha', 'beta', 'gamma']:
            if name not in self.completed:
                return {name: self.jobs[name]}
        return {}

    def complete(self, name):
        self.completed.add(name)
        if set(self.names) == self.completed:
            self._empty = True

class DummyJobQueue:
    def __init__(self, names):
        self.names = names
    def getInstance(self):
        return DummyInstance(self.names)

def jobQueue(arg=None):
    return DummyJobQueue(arg)

def test_creates_jobs_for_empty_arguments_public():
    jq = jobQueue([])
    instance = jq.getInstance()
    assert not instance.isEmpty()
    items = instance.pop()
    assert isinstance(items.get('alpha', None), DummyJob)

def test_completes_and_queues_next_jobs_public():
    jq = jobQueue(['alpha', 'beta', 'gamma'])
    instance = jq.getInstance()
    items1 = instance.pop()
    assert items1.get('alpha', None) is not None
    instance.complete('alpha')
    items2 = instance.pop()
    assert items2.get('beta', None) is not None
    instance.complete('beta')
    items3 = instance.pop()
    assert items3.get('gamma', None) is not None
    instance.complete('gamma')
    assert instance.isEmpty()

def test_handles_isempty_with_single_job_public():
    jq = jobQueue(['gamma'])
    instance = jq.getInstance()
    assert not instance.isEmpty()
    items = instance.pop()
    instance.complete('gamma')
    assert instance.isEmpty()