import pytest

class VIVOModelImpl:
    def setIconBadgeNum(self, application, notification, num):
        raise Exception("not support : vivo")

class TestVIVOModelImplPublic:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.vivoModel = VIVOModelImpl()
        self.mockApplication = mocker.Mock()
        self.mockNotification = mocker.Mock()

    def test_set_icon_badge_num_always_throws_exception_public(self):
        with pytest.raises(Exception) as exc_info:
            self.vivoModel.setIconBadgeNum(self.mockApplication, self.mockNotification, 17)
        assert str(exc_info.value) == "not support : vivo"