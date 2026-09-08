import pytest

class XiaoMiModelImpl:
    def setIconBadgeNum(self, application, notification, num):
        if notification is None:
            raise Exception("Xiaomi phones must send notification")
        # Use reflection in real code; here simulate logic for TestNotification structure
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

class TestXiaoMiModelImpl:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.xiaoMiModel = XiaoMiModelImpl()
        self.mockApplication = mocker.Mock()

    def test_set_icon_badge_num_null_notification(self):
        with pytest.raises(Exception) as exc_info:
            self.xiaoMiModel.setIconBadgeNum(self.mockApplication, None, 10)
        assert str(exc_info.value) == "Xiaomi phones must send notification"

    def test_set_icon_badge_num_valid_notification(self):
        notification = TestNotification()
        testCount = 5
        result = self.xiaoMiModel.setIconBadgeNum(self.mockApplication, notification, testCount)
        assert result is not None
        assert result is notification
        assert notification.extraNotification.getMessageCount() == testCount