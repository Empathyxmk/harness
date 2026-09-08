import pytest

class XiaoMiModelImpl:
    def setIconBadgeNum(self, application, notification, num):
        if notification is None:
            raise Exception("Xiaomi phones must send notification")
        if hasattr(notification, 'extraNotification') and hasattr(notification.extraNotification, 'setMessageCount'):
            notification.extraNotification.setMessageCount(num)
        return notification

class TestNotification:
    def __init__(self):
        self.extraNotification = self.TestExtraNotification()
    class TestExtraNotification:
        def __init__(self):
            self.messageCount = 0
        def setMessageCount(self, count):
            self.messageCount = count
        def getMessageCount(self):
            return self.messageCount

class TestXiaoMiModelImplPublic:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.xiaoMiModel = XiaoMiModelImpl()
        self.mockApplication = mocker.Mock()

    def test_set_icon_badge_num_null_notification_public(self):
        with pytest.raises(Exception) as exc_info:
            self.xiaoMiModel.setIconBadgeNum(self.mockApplication, None, 99)
        assert str(exc_info.value) == "Xiaomi phones must send notification"

    def test_set_icon_badge_num_valid_notification_public(self):
        notification = TestNotification()
        testCount = 12
        result = self.xiaoMiModel.setIconBadgeNum(self.mockApplication, notification, testCount)
        assert result is not None
        assert result is notification
        assert notification.extraNotification.getMessageCount() == testCount