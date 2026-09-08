import pytest

class Build:
    class VERSION_CODES:
        N = 24
        O_MR1 = 27

class SdkVersionMocker:
    _sdk_int = Build.VERSION_CODES.O_MR1

    @classmethod
    def setSdkVersion(cls, value):
        cls._sdk_int = value
    @classmethod
    def getSdkVersion(cls):
        return cls._sdk_int
    @classmethod
    def resetSdkVersion(cls):
        cls._sdk_int = Build.VERSION_CODES.O_MR1

class DummyUtils:
    def getLaunchIntentForPackage(self, app):
        return "sample.another.MainAct"
    def canResolveBroadcast(self, context, intent):
        return True

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

class GoogleModelImpl:
    def setIconBadgeNum(self, application, notification, num):
        if SdkVersionMocker.getSdkVersion() < Build.VERSION_CODES.O_MR1:
            raise Exception("google not support before API O")
        # Simulate effective broadcast
        intent = DummyIntent("android.intent.action.BADGE_COUNT_UPDATE")
        intent.setExtra("badge_count", num)
        intent.setExtra("badge_count_package_name", application.getPackageName())
        intent.setExtra("badge_count_class_name", application.getUtils().getLaunchIntentForPackage(application))
        application.sendBroadcast(intent)

import types

class TestGoogleModelImplPublic:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.googleModel = GoogleModelImpl()
        self.mockApplication = mocker.Mock()
        self.mockNotification = mocker.Mock()
        self.mockUtils = DummyUtils()
        self.mockApplication.getPackageName.return_value = "sample.another"
        self.mockApplication.getUtils.return_value = self.mockUtils

        def sendBroadcast(intent):
            self.sent_intent = intent
        self.mockApplication.sendBroadcast = sendBroadcast
        self.sent_intent = None
        SdkVersionMocker.resetSdkVersion()

    def teardown_method(self):
        SdkVersionMocker.resetSdkVersion()

    def test_set_icon_badge_num_sdk_below_o_public(self):
        SdkVersionMocker.setSdkVersion(Build.VERSION_CODES.N)  # 24, below O_MR1=27
        with pytest.raises(Exception) as exc_info:
            self.googleModel.setIconBadgeNum(self.mockApplication, self.mockNotification, 15)
        assert str(exc_info.value) == "google not support before API O"
        assert not hasattr(self, 'sent_intent') or self.sent_intent is None

    def test_set_icon_badge_num_sdk_at_or_above_o_public(self):
        SdkVersionMocker.setSdkVersion(Build.VERSION_CODES.O_MR1)
        testCount = 21

        captured = {}
        def sendBroadcast(intent):
            captured['intent'] = intent
        self.mockApplication.sendBroadcast = sendBroadcast
        self.mockApplication.getUtils.return_value = self.mockUtils

        self.googleModel.setIconBadgeNum(self.mockApplication, self.mockNotification, testCount)
        intent = captured['intent']
        assert intent.getAction() == "android.intent.action.BADGE_COUNT_UPDATE"
        assert intent.getIntExtra("badge_count", 0) == testCount
        assert intent.getStringExtra("badge_count_package_name") == "sample.another"
        assert intent.getStringExtra("badge_count_class_name") == "sample.another.MainAct"