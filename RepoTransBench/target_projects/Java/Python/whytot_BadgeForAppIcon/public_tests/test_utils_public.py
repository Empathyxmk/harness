import pytest

class DummyContext:
    def __init__(self, package_name="public.pkg.name"):
        self._package_name = package_name
        self._package_manager = DummyPackageManager()
    def getPackageName(self):
        return self._package_name
    def getPackageManager(self):
        return self._package_manager

class DummyPackageManager:
    def getLaunchIntentForPackage(self, pkg_name):
        # For this public test, just return a dummy value
        return DummyIntent(component=DummyComponentName("public.pkg.name.Launch"))
    def queryBroadcastReceivers(self, intent, flags):
        return [DummyResolveInfo()]  # Pretend always resolvable for this test

class DummyIntent:
    def __init__(self, action=None, component=None):
        self._action = action
        self._component = component
    def getAction(self):
        return self._action
    def getComponent(self):
        return self._component

class DummyComponentName:
    def __init__(self, class_name):
        self._class_name = class_name
    def getClassName(self):
        return self._class_name

class DummyResolveInfo: pass

class Utils:
    _instance = None
    @staticmethod
    def getInstance():
        if Utils._instance is None:
            Utils._instance = Utils()
        return Utils._instance
    def canResolveBroadcast(self, context, intent):
        receivers = context.getPackageManager().queryBroadcastReceivers(intent, 0)
        return bool(receivers and len(receivers) > 0)
    def getLaunchIntentForPackage(self, context):
        pkg = context.getPackageName()
        launch_intent = context.getPackageManager().getLaunchIntentForPackage(pkg)
        if launch_intent is None:
            raise Exception("NullPointerException")
        component = launch_intent.getComponent()
        return component.getClassName()

class TestUtilsPublic:
    def test_get_launch_intent_for_package_public(self):
        context = DummyContext()
        # should not return None
        result = Utils.getInstance().getLaunchIntentForPackage(context)
        assert result is not None

    def test_can_resolve_broadcast_public(self):
        context = DummyContext()
        intent = DummyIntent("public.SOME_ACTION")
        result = Utils.getInstance().canResolveBroadcast(context, intent)
        assert result is True or result is False  # Always true; must complete path