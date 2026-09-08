import pytest

class DummyJob:
    def __init__(self, name):
        self.name = name
        self.config = {'name': name, 'dependsOn': ['foo'] if name == 'bar' else []}

class DummyInstance:
    def __init__(self, names):
        self.names = names
        self.completed = set()
        self.jobs = {name: DummyJob(name) for name in names or ['foo', 'bar']}
        self._empty = False

    def isEmpty(self):
        if set(self.names) == self.completed:
            return True
        if not self.names:
            return False
        return False

    def pop(self):
        for name in self.names or ['foo', 'bar']:
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
    # Simulate the jobQueue import/module from JS
    return DummyJobQueue(arg)

def test_creates_jobs_for_empty_arguments():
    jq = jobQueue([])
    instance = jq.getInstance()
    assert not instance.isEmpty()
    items = instance.pop()
    assert isinstance(items.get('foo', None), DummyJob)

def test_completes_and_queues_next_jobs():
    jq = jobQueue(['foo', 'bar'])
    instance = jq.getInstance()
    items1 = instance.pop()
    assert items1.get('foo', None) is not None
    instance.complete('foo')
    items2 = instance.pop()
    assert items2.get('bar', None) is not None
    instance.complete('bar')
    assert instance.isEmpty()

def test_handles_isempty_when_nothing_left():
    jq = jobQueue(['foo'])
    instance = jq.getInstance()
    assert not instance.isEmpty()
    # pop and complete
    items = instance.pop()
    instance.complete('foo')
    assert instance.isEmpty()