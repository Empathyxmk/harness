using System;
using Xunit;
using Moq;
using xzr.hkf;

namespace libxzr_HorizonKernelFlasher.PublicTests
{
    public class MainActivityPublicTests
    {
        private MainActivity _activity;

        public MainActivityPublicTests()
        {
            _activity = new MainActivity();
            _activity.logView = new Mock<ITextView>().Object;
            _activity.scrollView = new Mock<IScrollView>().Object;
            MainActivity.cur_status = MainActivity.Status.Normal;
        }

        [Fact]
        public void TestAppendLog_DEBUG_Public()
        {
            MainActivity.DEBUG = true;
            var mockAct = new Mock<MainActivity>();
            mockAct.Setup(a => a.RunOnUiThread(It.IsAny<Action>()));
            MainActivity._appendLog("world", _activity);
            MainActivity.appendLog("foobar", _activity);
            MainActivity.DEBUG = false;
        }

        [Fact]
        public void TestAppendLog_ui_print_Public()
        {
            var mockAct = new Mock<MainActivity>();
            mockAct.Setup(a => a.RunOnUiThread(It.IsAny<Action>())).Callback<Action>(a => a());
            mockAct.Object.logView = new Mock<ITextView>().Object;
            mockAct.Object.scrollView = new Mock<IScrollView>().Object;
            MainActivity.appendLog("ui_print log with different msg", mockAct.Object);
        }

        [Fact]
        public void TestFlashNew_NotFlashing_Public()
        {
            MainActivity.cur_status = MainActivity.Status.Normal;
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.UpdateTitle());
            activitySpy.Setup(a => a.RunWithFilePath(It.IsAny<object>(), It.IsAny<object>()));
            activitySpy.Object.logView = new Mock<ITextView>().Object;
            activitySpy.Object.flash_new();
            activitySpy.Verify(a => a.UpdateTitle());
            activitySpy.Verify(a => a.RunWithFilePath(It.IsAny<object>(), It.IsAny<object>()));
        }

        [Fact]
        public void TestOnBackPressed_FlashingAndOther_Public()
        {
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            MainActivity.cur_status = MainActivity.Status.Normal;
            activitySpy.Setup(a => a.SuperOnBackPressed());
            activitySpy.Object.onBackPressed();
            MainActivity.cur_status = MainActivity.Status.Error;
            activitySpy.Object.onBackPressed();
        }

        [Fact]
        public void TestOnCreateOptionsMenu_Public()
        {
            var mockMenu2 = new Mock<IMenu>();
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.GetMenuInflater()).Returns(new Mock<IMenu>().Object);
            Assert.True(activitySpy.Object.onCreateOptionsMenu(mockMenu2.Object));
        }

        [Fact]
        public void TestOnOptionsItemSelected_about_Public()
        {
            var item = new Mock<IMenuItem>();
            item.Setup(i => i.GetItemId()).Returns((int)ResourceId.Help);
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.GetAlertDialogBuilder()).Returns(new Mock<IAlertDialogBuilder>().Object);
            Assert.True(activitySpy.Object.onOptionsItemSelected(item.Object));
        }

        [Fact]
        public void TestOnOptionsItemSelected_flash_new_Public()
        {
            var item = new Mock<IMenuItem>();
            item.Setup(i => i.GetItemId()).Returns(-12345);
            var activitySpy = new Mock<MainActivity>() { CallBase = true };
            activitySpy.Setup(a => a.flash_new());
            Assert.True(activitySpy.Object.onOptionsItemSelected(item.Object));
        }

        [Fact]
        public void TestRunWithFilePath_Public()
        {
            var mock = new Mock<MainActivity>();
            var worker2 = new Mock<IMainActivityFileWorker>().Object;
            mock.Setup(a => a.StartActivityForResult(It.IsAny<object>(), It.IsAny<int>()));
            MainActivity.runWithFilePath(mock.Object, worker2);
            Assert.NotNull(worker2);
        }
    }
}