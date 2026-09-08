import pytest

class Build:
    class VERSION_CODES:
        N_MR1 = 25
        O = 26

class SdkVersionMocker:
    _sdk_int = Build.VERSION_CODES.O

    @classmethod
    def setSdkVersion(cls, value):
        cls._sdk_int = value
    @classmethod
    def getSdkVersion(cls):
        return cls._sdk_int
    @classmethod
    def resetSdkVersion(cls):
        cls._sdk_int = Build.VERSION_CODES.O

class GoogleModelImpl:
    def setIconBadgeNum(self, application, notification, num):
        if SdkVersionMocker.getSdkVersion() < Build.VERSION_CODES.O:
            raise Exception("google not support before API O")
        # Simulate intended broadcast effects:
        intent = DummyIntent("android.intent.action.BADGE_COUNT_UPDATE")
        intent.setExtra("badge_count", num)
        intent.setExtra("badge_count_package_name", application.getPackageName())
        class_name = application.getUtils().getLaunchIntentForPackage(application)
        intent.setExtra("badge_count_class_name", class_name)
        application.sendBroadcast(intent)

class DummyIntent:
    def __init__(self, action):
        self._extras = {}
        self._action = action
    def setExtra(self, key, value):
        self._extras[key] = value
    def getAction(self):
        return self._action
    def getIntExtra(self, key, default):
        v = self._extras.get(key, default)
        return int(v) if v is not None else default
    def getStringExtra(self, key):
        v = self._extras.get(key, None)
        return str(v) if v is not None else None

class DummyUtils:
    def getLaunchIntentForPackage(self, app):
        return "com.example.package.MainActivity"
    def canResolveBroadcast(self, context, intent):
        return True

import types

class TestGoogleModelImpl:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        # Set up mock application, notification, utils, and package manager
        self.googleModel = GoogleModelImpl()
        self.mockApplication = mocker.Mock()
        self.mockNotification = mocker.Mock()
        self.mockUtils = DummyUtils()
        self.mockApplication.getPackageName.return_value = "com.example.package"
        self.mockApplication.getUtils.return_value = self.mockUtils

        def sendBroadcast(intent):
            self.sent_intent = intent

        self.mockApplication.sendBroadcast = sendBroadcast
        self.sent_intent = None

        SdkVersionMocker.resetSdkVersion()

    def teardown_method(self):
        SdkVersionMocker.resetSdkVersion()

    def test_set_icon_badge_num_sdk_below_o(self):
        SdkVersionMocker.setSdkVersion(Build.VERSION_CODES.N_MR1)
        with pytest.raises(Exception) as exc_info:
            self.googleModel.setIconBadgeNum(self.mockApplication, self.mockNotification, 5)
        assert str(exc_info.value) == "google not support before API O"
        assert not hasattr(self, 'sent_intent') or self.sent_intent is None

    def test_set_icon_badge_num_sdk_at_or_above_o(self):
        SdkVersionMocker.setSdkVersion(Build.VERSION_CODES.O)
        testCount = 7
        # Save original sendBroadcast
        captured = {}

        def sendBroadcast(intent):
            captured['intent'] = intent

        self.mockApplication.sendBroadcast = sendBroadcast
        self.mockApplication.getUtils.return_value = self.mockUtils

        self.googleModel.setIconBadgeNum(self.mockApplication, self.mockNotification, testCount)
        intent = captured['intent']
        assert intent.getAction() == "android.intent.action.BADGE_COUNT_UPDATE"
        assert intent.getIntExtra("badge_count", 0) == testCount
        assert intent.getStringExtra("badge_count_package_name") == "com.example.package"
        assert intent.getStringExtra("badge_count_class_name") == "com.example.package.MainActivity"