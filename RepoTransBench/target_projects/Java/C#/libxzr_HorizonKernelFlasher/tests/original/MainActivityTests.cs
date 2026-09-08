using System;
using Xunit;
using Moq;
using xzr.hkf;
using xzr.hkf.utils;

namespace libxzr_HorizonKernelFlasher.Tests.Original
{
    public class MainActivityTests
    {
        private MainActivity _activity;

        public MainActivityTests()
        {
            _activity = new MainActivity();
            _activity.logView = new Mock<ITextView>().Object;
            _activity.scrollView = new Mock<IScrollView>().Object;
            MainActivity.cur_status = MainActivity.Status.Normal;
        }

        [Fact]
        public void TestAppendLog_DEBUG()
        {
            MainActivity.DEBUG = true;
            var mockAct = new Mock<MainActivity>();
            mockAct.Setup(a => a.RunOnUiThread(It.IsAny<Action>())).Verifiable();
            MainActivity._appendLog("hello", _activity);
            MainActivity.appendLog("anything", _activity);
            MainActivity.DEBUG = false;
        }

        [Fact]
        public void TestAppendLog_ui_print()
        {
            var mockAct = new Mock<MainActivity>();
            mockAct.Setup(a => a.RunOnUiThread(It.IsAny<Action>())).Callback<Action>(a => a());
            mockAct.Object.logView = new Mock<ITextView>().Object;
            mockAct.Object.scrollView = new Mock<IScrollView>().Object;
            MainActivity.appendLog("ui_print this is message", mockAct.Object);
        }

        [Fact]
        public void TestFlashNew_NotFlashing()
        {
            MainActivity.cur_status = MainActivity.Status.Normal;
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.UpdateTitle()).Verifiable();
            activitySpy.Setup(a => a.RunWithFilePath(It.IsAny<object>(), It.IsAny<object>())).Verifiable();
            activitySpy.Object.logView = new Mock<ITextView>().Object;
            activitySpy.Object.flash_new();
            activitySpy.Verify(a => a.UpdateTitle());
            activitySpy.Verify(a => a.RunWithFilePath(It.IsAny<object>(), It.IsAny<object>()));
        }

        [Fact]
        public void TestOnBackPressed_FlashingAndOther()
        {
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            MainActivity.cur_status = MainActivity.Status.Normal;
            activitySpy.Setup(a => a.SuperOnBackPressed()).Verifiable();
            activitySpy.Object.onBackPressed();
            MainActivity.cur_status = MainActivity.Status.Flashing;
            activitySpy.Object.onBackPressed();
        }

        [Fact]
        public void TestOnCreateOptionsMenu()
        {
            var mockMenu = new Mock<IMenu>();
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.GetMenuInflater()).Returns(new Mock<IMenu>().Object);
            Assert.True(activitySpy.Object.onCreateOptionsMenu(mockMenu.Object));
        }

        [Fact]
        public void TestOnOptionsItemSelected_about()
        {
            var item = new Mock<IMenuItem>();
            item.Setup(i => i.GetItemId()).Returns((int)ResourceId.About);
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.GetAlertDialogBuilder()).Returns(new Mock<IAlertDialogBuilder>().Object);
            Assert.True(activitySpy.Object.onOptionsItemSelected(item.Object));
        }

        [Fact]
        public void TestOnOptionsItemSelected_flash_new()
        {
            var item = new Mock<IMenuItem>();
            item.Setup(i => i.GetItemId()).Returns((int)ResourceId.FlashNew);
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.flash_new()).Verifiable();
            Assert.True(activitySpy.Object.onOptionsItemSelected(item.Object));
            activitySpy.Verify(a => a.flash_new());
        }

        [Fact]
        public void TestRunWithFilePath()
        {
            var mockActivity = new Mock<MainActivity>();
            var worker = new Mock<IMainActivityFileWorker>().Object;
            mockActivity.Setup(a => a.StartActivityForResult(It.IsAny<object>(), It.IsAny<int>()));
            MainActivity.runWithFilePath(mockActivity.Object, worker);
            Assert.NotNull(worker);
        }
    }
}