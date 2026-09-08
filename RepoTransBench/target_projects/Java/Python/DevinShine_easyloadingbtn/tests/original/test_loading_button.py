import pytest

from src.easyloadingbtn.loading_button import LoadingButton

class TestLoadingButton:
    def setup_method(self):
        # Use a real LoadingButton as mock Drawable is not needed
        class DummyLoadingButton(LoadingButton):
            def getDrawable(self, id):
                # Not needed for Python version: stub for resource images
                return object()
        self.loadingButton = DummyLoadingButton()

    def testInitialState(self):
        assert not self.loadingButton.isCompleted()
        assert not self.loadingButton.isShowArc()

    def testSetTargetProgress_setsProgress(self):
        self.loadingButton.setTargetProgress(180)
        assert self.loadingButton.getTargetProgress() == 180

    def testSetAndGetCallback(self):
        wasCalled = [False]
        class MyCallback(LoadingButton.Callback):
            def complete(self_):
                wasCalled[0] = True
        self.loadingButton.setCallback(MyCallback())
        self.loadingButton.performCompleteCallback()
        assert wasCalled[0]

    def testSetCompleted(self):
        self.loadingButton.setCompleted(True)
        assert self.loadingButton.isCompleted()
        self.loadingButton.setCompleted(False)
        assert not self.loadingButton.isCompleted()

    def testOnClick_withNotCompleted(self):
        self.loadingButton.setCompleted(False)
        # Should not throw
        self.loadingButton.performClick()

    def testOnClick_withCompleted(self):
        self.loadingButton.setCompleted(True)
        assert self.loadingButton.isCompleted()
        # Should return immediately (no-op)
        self.loadingButton.performClick()

    def testSetShowArc(self):
        self.loadingButton.setShowArc(True)
        assert self.loadingButton.isShowArc()
        self.loadingButton.setShowArc(False)
        assert not self.loadingButton.isShowArc()