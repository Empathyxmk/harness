import threading
import pytest

class Generator:
    '''A Python reimplementation of the Java Generator base class, using threading and yield.'''
    def __init__(self):
        self._queue = []
        self._exception = None
        self._finished = threading.Event()
        self._lock = threading.Lock()
        self._has_value = threading.Condition(self._lock)
        self._started = False
        self._producer_thread = None

    def _producer(self):
        try:
            self.run()
        except Exception as e:
            self._exception = e
        finally:
            with self._lock:
                self._finished.set()
                self._has_value.notify_all()

    def run(self):
        raise NotImplementedError()

    def iterator(self):
        if not self._started:
            self._producer_thread = threading.Thread(target=self._producer)
            self._producer_thread.daemon = True
            self._producer_thread.start()
            self._started = True

        class GenIter:
            def __init__(gself, outer):
                gself.outer = outer
                gself.index = 0
                gself.current = None
            def __iter__(gself):
                return gself
            def __next__(gself):
                outer = gself.outer
                with outer._lock:
                    while len(outer._queue) == 0 and not outer._finished.is_set():
                        outer._has_value.wait()
                    if outer._exception:
                        raise outer._exception
                    if len(outer._queue) > 0:
                        return outer._queue.pop(0)
                    if outer._finished.is_set():
                        if outer._exception:
                            raise outer._exception
                        raise StopIteration()
                    raise StopIteration()
            def has_next(gself):
                outer = gself.outer
                with outer._lock:
                    while len(outer._queue) == 0 and not outer._finished.is_set():
                        outer._has_value.wait()
                    if outer._exception:
                        raise outer._exception
                    return len(outer._queue) > 0
        return GenIter(self)

    def yield_(self, value):
        with self._lock:
            self._queue.append(value)
            self._has_value.notify_all()

    @property
    def producer(self):
        return self._producer_thread

    def finalize(self):
        # wait for thread to finish
        if self._producer_thread is not None:
            self._producer_thread.join(timeout=3)

def list_from_iterable(iterable):
    return list(iterable)

def testEmptyGenerator():
    class EmptyGenerator(Generator):
        def run(self):
            pass
    assert list_from_iterable(EmptyGenerator().iterator()) == []

def testOneEltGenerator():
    class ListGenerator(Generator):
        def __init__(self, elements):
            super().__init__()
            self.elements = elements
        def run(self):
            for elt in self.elements:
                self.yield_(elt)
    oneEltList = [1]
    assert list_from_iterable(ListGenerator(oneEltList).iterator()) == oneEltList

def testTwoEltGenerator():
    class ListGenerator(Generator):
        def __init__(self, elements):
            super().__init__()
            self.elements = elements
        def run(self):
            for elt in self.elements:
                self.yield_(elt)
    twoEltList = [1, 2]
    assert list_from_iterable(ListGenerator(twoEltList).iterator()) == twoEltList

def testInfiniteGenerator():
    NUM_ELTS_TO_INSPECT = 1000
    class InfiniteGenerator(Generator):
        def run(self):
            while True:
                self.yield_(1)
    generator = InfiniteGenerator()
    iter_ = generator.iterator()
    for _ in range(NUM_ELTS_TO_INSPECT):
        assert iter_.has_next()
        assert next(iter_) == 1

def testInfiniteGeneratorLeavesNoRunningThreads():
    NUM_ELTS_TO_INSPECT = 1000
    class InfiniteGenerator(Generator):
        def run(self):
            for _ in range(NUM_ELTS_TO_INSPECT):
                self.yield_(1)
    generator = InfiniteGenerator()
    iter_ = generator.iterator()
    for _ in range(NUM_ELTS_TO_INSPECT):
        assert iter_.has_next()
        assert next(iter_) == 1
    generator.finalize()
    # The thread should have terminated
    assert generator.producer is not None
    assert not generator.producer.is_alive()

class CustomRuntimeException(Exception):
    pass

def testGeneratorRaisingExceptionHasNext():
    class GeneratorRaisingException(Generator):
        def run(self):
            raise CustomRuntimeException()
    generator = GeneratorRaisingException()
    iter_ = generator.iterator()
    with pytest.raises(CustomRuntimeException):
        iter_.has_next()

def testGeneratorRaisingExceptionNext():
    class GeneratorRaisingException(Generator):
        def run(self):
            raise CustomRuntimeException()
    generator = GeneratorRaisingException()
    iter_ = generator.iterator()
    with pytest.raises(CustomRuntimeException):
        next(iter_)