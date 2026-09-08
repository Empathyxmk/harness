import pytest

class DummyComponentName:
    def __init__(self, class_name):
        self._class_name = class_name
    def getClassName(self):
        return self._class_name

class DummyIntent:
    def __init__(self, action=None):
        self._action = action
    def getAction(self):
        return self._action

class DummyResolveInfo:
    pass

class DummyPackageManager:
    def __init__(self):
        self.launch_intent = None
        self.query_intent_map = {}
    def getLaunchIntentForPackage(self, pkg_name):
        return self.launch_intent
    def queryBroadcastReceivers(self, intent, flags):
        return self.query_intent_map.get(intent.getAction(), None)

class DummyContext:
    def __init__(self):
        self._package_name = "com.example.package"
        self._package_manager = DummyPackageManager()
    def getPackageManager(self):
        return self._package_manager
    def getPackageName(self):
        return self._package_name

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

import types

class TestUtils:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.mockContext = DummyContext()
        self.mockContext._package_manager = DummyPackageManager()

    def test_get_instance_singleton(self):
        inst1 = Utils.getInstance()
        inst2 = Utils.getInstance()
        assert inst1 is not None
        assert inst1 is inst2

    def test_can_resolve_broadcast_no_receivers(self):
        context = DummyContext()
        context._package_manager = DummyPackageManager()
        intent = DummyIntent("test_action")
        # First: returns None
        context._package_manager.query_intent_map[intent.getAction()] = None
        assert not Utils.getInstance().canResolveBroadcast(context, intent)
        # Second: returns []
        context._package_manager.query_intent_map[intent.getAction()] = []
        assert not Utils.getInstance().canResolveBroadcast(context, intent)

    def test_can_resolve_broadcast_with_receivers(self):
        context = DummyContext()
        context._package_manager = DummyPackageManager()
        intent = DummyIntent("test_action_with_receivers")
        context._package_manager.query_intent_map[intent.getAction()] = [DummyResolveInfo()]
        assert Utils.getInstance().canResolveBroadcast(context, intent)

    def test_get_launch_intent_for_package(self):
        # Setup
        context = DummyContext()
        context._package_manager = DummyPackageManager()
        mock_launch_intent = DummyIntent()
        mock_component = DummyComponentName("com.example.package.MainActivity")
        mock_launch_intent.getComponent = lambda: mock_component
        context._package_manager.launch_intent = mock_launch_intent
        context._package_name = "com.example.package"

        class_name = Utils.getInstance().getLaunchIntentForPackage(context)
        assert class_name == "com.example.package.MainActivity"

    def test_get_launch_intent_for_package_null_launch_intent(self):
        # Setup
        context = DummyContext()
        context._package_manager = DummyPackageManager()
        context._package_manager.launch_intent = None
        context._package_name = "com.example.package"
        with pytest.raises(Exception) as exc_info:
            Utils.getInstance().getLaunchIntentForPackage(context)
        assert "NullPointerException" in str(exc_info.value)