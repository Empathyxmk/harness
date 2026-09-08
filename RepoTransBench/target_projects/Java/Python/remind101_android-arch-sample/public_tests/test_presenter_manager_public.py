import unittest

class DummyPresenter:
    pass

class PresenterManager:
    _instance = None

    def __init__(self, max_size=8, timeout=3, unit="minutes"):
        self._store = {}
        self._used = set()
        self.max_size = max_size
        self.timeout = timeout
        self.unit = unit

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = PresenterManager()
        return cls._instance

    def savePresenter(self, presenter, bundle):
        presenter_id = id(presenter)
        bundle['presenter_id'] = presenter_id
        self._store[presenter_id] = presenter
        self._used.discard(presenter_id)

    def restorePresenter(self, bundle):
        presenter_id = bundle.get('presenter_id')
        if presenter_id is None:
            return None
        if presenter_id in self._store and presenter_id not in self._used:
            self._used.add(presenter_id)
            return self._store[presenter_id]
        else:
            return None

class TestPresenterManagerPublic(unittest.TestCase):
    def setUp(self):
        PresenterManager._instance = None
        self.presenterManager = PresenterManager(8, 3, "minutes")

    def tearDown(self):
        PresenterManager._instance = None

    def testSaveAndRestorePresenterWithDifferentInstance(self):
        bundle = {}
        presenter = DummyPresenter()
        self.presenterManager.savePresenter(presenter, bundle)
        restored = self.presenterManager.restorePresenter(bundle)
        self.assertIsNotNone(restored)
        self.assertEqual(presenter, restored)

    def testRestorePresenterReturnsNullAfterRestoreWithDifferentTimings(self):
        bundle = {}
        presenter = DummyPresenter()
        self.presenterManager.savePresenter(presenter, bundle)
        firstRestore = self.presenterManager.restorePresenter(bundle)
        self.assertIsNotNone(firstRestore)
        secondRestore = self.presenterManager.restorePresenter(bundle)
        self.assertIsNone(secondRestore)

    def testGetInstanceReturnsSameSingletonInstance(self):
        instance1 = PresenterManager.getInstance()
        instance2 = PresenterManager.getInstance()
        self.assertIs(instance1, instance2)

if __name__ == "__main__":
    unittest.main()