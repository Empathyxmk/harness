import pytest

from src.easyloadingbtn.loading_button import LoadingButton

class TestLoadingButtonPublic:
    def setup_method(self):
        class DummyLoadingButton(LoadingButton):
            def getDrawable(self, id):
                return object()
        self.loadingButton = DummyLoadingButton()

    def testInitialState_publicVariant(self):
        assert not self.loadingButton.isCompleted()
        assert not self.loadingButton.isShowArc()

    def testSetTargetProgress_setsDifferentProgress(self):
        self.loadingButton.setTargetProgress(250)
        assert self.loadingButton.getTargetProgress() == 250

    def testSetAndGetCallback_public(self):
        flag = [False]
        class CB(LoadingButton.Callback):
            def complete(self_):
                flag[0] = True
        self.loadingButton.setCallback(CB())
        self.loadingButton.performCompleteCallback()
        assert flag[0]

    def testSetCompleted_alternatePattern(self):
        self.loadingButton.setCompleted(False)
        assert not self.loadingButton.isCompleted()
        self.loadingButton.setCompleted(True)
        assert self.loadingButton.isCompleted()

    def testOnClick_withCompleted_Public(self):
        self.loadingButton.setCompleted(True)
        assert self.loadingButton.isCompleted()
        self.loadingButton.performClick()  # nothing more to check

    def testOnClick_withNotCompleted_Public(self):
        self.loadingButton.setCompleted(False)
        self.loadingButton.performClick()  # nothing more to check

    def testSetShowArc_public(self):
        self.loadingButton.setShowArc(False)
        assert not self.loadingButton.isShowArc()
        self.loadingButton.setShowArc(True)
        assert self.loadingButton.isShowArc()