using Xunit;
using Moq;
using ProjectName;

namespace OriginalTests
{
    public class DelayedProgressDialogTests
    {
        private object _appContext = new object();

        [Fact]
        public void TestMakeMethods()
        {
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "title", "message"));
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "title", "message", true));
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "title", "message", true, true));
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "title", "message", true, true, null));
            var dialogWithTheme = new DelayedProgressDialog(_appContext, 1);
            Assert.NotNull(dialogWithTheme);
        }

        [Fact]
        public void TestShowDelayedMethods()
        {
            DelayedProgressDialog.ShowDelayed(_appContext, "title", "message").Dismiss();
            DelayedProgressDialog.ShowDelayed(_appContext, "title", "message", true).Dismiss();
            DelayedProgressDialog.ShowDelayed(_appContext, "title", "message", true, true).Dismiss();
            DelayedProgressDialog.ShowDelayed(_appContext, "title", "message", true, true, null).Dismiss();
        }

        [Fact]
        public void TestDismissBeforeMinDelay_ShouldNotShow()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(1000);
            dialog.SetMinShowTime(500);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            // Sim 200ms
            Assert.False(dialog.IsShowing());
            dialog.Dismiss();
            // Sim advance
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestDismissAfterMinDelayButBeforeMinShowTime_ShouldShowForMinShowTime()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(500);
            dialog.SetMinShowTime(1000);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            // Simulate 200ms showing
            dialog.Dismiss();
            Assert.True(dialog.IsShowing());
            // Simulate 799 more ms (still showing)
            Assert.True(dialog.IsShowing());
            // Simulate 1 ms pass for total 1000ms
            dialog.Test_AdvanceHide();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestDismissAfterMinShowTime_ShouldDismissImmediately()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(500);
            dialog.SetMinShowTime(1000);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            // Simulate +1000ms
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestShowWithZeroMinDelay_ShowsImmediately()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(0);
            dialog.SetMinShowTime(500);
            dialog.Show();
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            dialog.Test_AdvanceHide();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestDismissWhenNeverShown_NoOp()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(1000);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            dialog.Dismiss();
            // Simulate time pass
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestOnDetachedFromWindowRemovesCallbacks()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.Show();
            dialog.OnDetachedFromWindow();
            dialog.Dismiss();
            dialog.Test_AdvanceHide();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestSetMinShowTime()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinShowTime(2000);
            dialog.SetMinDelay(0);
            dialog.Show();
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            // Simulate 1999ms
            Assert.True(dialog.IsShowing());
            // Simulate 1 ms tick
            dialog.Test_AdvanceHide();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestSetMinDelay()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(2000);
            dialog.SetMinShowTime(0);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            // Simulate 1999ms
            Assert.False(dialog.IsShowing());
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestMultipleShowDismissCycles()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(100);
            dialog.SetMinShowTime(200);

            // Cycle 1
            dialog.Show();
            // 50ms
            dialog.Dismiss();
            // 500ms
            Assert.False(dialog.IsShowing());

            // Cycle 2
            dialog.Show();
            dialog.Test_AdvanceShow();
            // 200ms
            Assert.True(dialog.IsShowing());
            // +200ms
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            Assert.False(dialog.IsShowing());

            // Cycle 3
            dialog.Show();
            dialog.Test_AdvanceShow();
            // 100ms
            Assert.True(dialog.IsShowing());
            // +100ms
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            Assert.True(dialog.IsShowing());
            dialog.Test_AdvanceHide();
            Assert.False(dialog.IsShowing());
        }
    }
}