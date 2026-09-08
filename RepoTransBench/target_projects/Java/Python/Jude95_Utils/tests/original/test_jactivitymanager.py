import unittest

class DummyActivity:
    def __init__(self, name):
        self._name = name
    def __eq__(self, other):
        if other is None:
            return False
        return isinstance(other, DummyActivity) and self._name == other._name
    def getName(self):
        return self._name

class ActivityStackManager:
    _stack = []
    _current = None
    @classmethod
    def clear(cls):
        cls._stack = []
        cls._current = None
    @classmethod
    def add_activity(cls, activity):
        cls._stack.append(activity)
        ActivityStackManager._current = activity
    @classmethod
    def remove_activity(cls, activity):
        cls._stack = [a for a in cls._stack if a != activity]
        if cls._stack:
            cls._current = cls._stack[-1]
        else:
            cls._current = None
    @classmethod
    def get_current(cls):
        return cls._current
    @classmethod
    def get_activity_stack(cls):
        return list(cls._stack)
    @classmethod
    def close_activity(cls, activity):
        cls.remove_activity(activity)
    @classmethod
    def close_all_activity(cls):
        cls._stack.clear()
        cls._current = None
    @classmethod
    def close_activity_by_name(cls, name):
        to_remove = [a for a in cls._stack if a.getName() == name.split(".")[-1]]
        for a in to_remove:
            cls.remove_activity(a)
    @classmethod
    def get_current_activity_name(cls):
        if cls._current is not None:
            return f"com.jude.utils.{cls._current.getName()}"
        return ""

class ApplicationLifecycleCallbacks:
    def onActivityResumed(self, activity):
        ActivityStackManager.add_activity(activity)
    def onActivityDestroyed(self, activity):
        ActivityStackManager.remove_activity(activity)

class JActivityManager:
    @staticmethod
    def getActivityStack():
        return ActivityStackManager.get_activity_stack()
    @staticmethod
    def currentActivity():
        return ActivityStackManager.get_current()
    @staticmethod
    def getActivityLifecycleCallbacks():
        return ApplicationLifecycleCallbacks()
    @staticmethod
    def closeActivity(activity):
        ActivityStackManager.close_activity(activity)
    def closeAllActivity(self):
        ActivityStackManager.close_all_activity()
    @staticmethod
    def closeActivityByName(name):
        ActivityStackManager.close_activity_by_name(name)
    @staticmethod
    def getCurrentActivityName():
        return ActivityStackManager.get_current_activity_name()


class TestJActivityManager(unittest.TestCase):

    def setUp(self):
        ActivityStackManager.clear()

    def testStackAdditionAndRetrieval(self):
        a1 = DummyActivity("A1")
        a2 = DummyActivity("A2")
        stack = JActivityManager.getActivityStack()
        stack.clear()
        self.assertIsNone(JActivityManager.currentActivity())

        cb = JActivityManager.getActivityLifecycleCallbacks()
        cb.onActivityResumed(a1)
        self.assertEqual(a1, JActivityManager.currentActivity())
        cb.onActivityResumed(a2)
        self.assertEqual(a2, JActivityManager.currentActivity())
        cb.onActivityDestroyed(a1)
        self.assertEqual(a2, JActivityManager.currentActivity())
        cb.onActivityDestroyed(a2)
        self.assertIsNone(JActivityManager.currentActivity())

    def testCloseActivity(self):
        a1 = DummyActivity("A1")
        a2 = DummyActivity("A2")
        cb = JActivityManager.getActivityLifecycleCallbacks()
        cb.onActivityResumed(a1)
        cb.onActivityResumed(a2)

        JActivityManager.closeActivity(a2)
        self.assertEqual(a1, JActivityManager.currentActivity())

        JActivityManager.closeActivity(None)
        self.assertEqual(a1, JActivityManager.currentActivity())

    def testCloseAllActivity(self):
        a1 = DummyActivity("A1")
        a2 = DummyActivity("A2")
        cb = JActivityManager.getActivityLifecycleCallbacks()
        cb.onActivityResumed(a1)
        cb.onActivityResumed(a2)
        JActivityManager().closeAllActivity()
        self.assertIsNone(JActivityManager.currentActivity())

    def testCloseActivityByName(self):
        a1 = DummyActivity("ActivityA")
        a2 = DummyActivity("ActivityB")
        cb = JActivityManager.getActivityLifecycleCallbacks()
        cb.onActivityResumed(a1)
        cb.onActivityResumed(a2)
        JActivityManager.closeActivityByName("com.jude.utils.ActivityB")
        self.assertEqual(a1, JActivityManager.currentActivity())

    def testGetCurrentActivityName(self):
        a1 = DummyActivity("MainScreen")
        cb = JActivityManager.getActivityLifecycleCallbacks()
        cb.onActivityResumed(a1)
        self.assertEqual("com.jude.utils.MainScreen", JActivityManager.getCurrentActivityName())
        cb.onActivityDestroyed(a1)
        self.assertEqual("", JActivityManager.getCurrentActivityName())

    def testGetActivityStack(self):
        a1 = DummyActivity("AA")
        cb = JActivityManager.getActivityLifecycleCallbacks()
        cb.onActivityResumed(a1)
        stack1 = JActivityManager.getActivityStack()
        self.assertFalse(len(stack1) == 0)
        stack2 = JActivityManager.getActivityStack()
        self.assertEqual(stack1, stack2)

if __name__ == "__main__":
    unittest.main()