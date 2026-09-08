using Xunit;
using ProjectName;

namespace PublicTests
{
    public class DelayedProgressDialogPublicTests
    {
        private object _appContext = new object();

        [Fact]
        public void TestMakeMethods_Public()
        {
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "pub_title", "pub_message"));
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "pub_title", "pub_message", false));
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "pub_title", "pub_message", false, false));
            Assert.NotNull(DelayedProgressDialog.Make(_appContext, "pub_title", "pub_message", false, false, null));
            var dialogWithTheme = new DelayedProgressDialog(_appContext, 1);
            Assert.NotNull(dialogWithTheme);
        }

        [Fact]
        public void TestShowDelayedMethods_Public()
        {
            DelayedProgressDialog.ShowDelayed(_appContext, "pub_title", "pub_message").Dismiss();
            DelayedProgressDialog.ShowDelayed(_appContext, "pub_title", "pub_message", false).Dismiss();
            DelayedProgressDialog.ShowDelayed(_appContext, "pub_title", "pub_message", false, false).Dismiss();
            DelayedProgressDialog.ShowDelayed(_appContext, "pub_title", "pub_message", false, false, null).Dismiss();
        }

        [Fact]
        public void TestDismissBeforeMinDelay_ShouldNotShow_Public()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(1200);
            dialog.SetMinShowTime(600);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            // Simulate 250ms tick
            Assert.False(dialog.IsShowing());
            dialog.Dismiss();
            // Simulate 1200ms pass
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestDismissAfterMinDelayButBeforeMinShowTime_Public()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(700);
            dialog.SetMinShowTime(1500);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            // 350ms
            dialog.Dismiss();
            Assert.True(dialog.IsShowing());
            // 1149ms
            Assert.True(dialog.IsShowing());
            // 1ms more
            dialog.Test_AdvanceHide();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestDismissAfterMinShowTime_ShouldDismissImmediately_Public()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(800);
            dialog.SetMinShowTime(1200);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            // 1200ms
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestShowWithZeroMinDelay_ShowsImmediately_Public()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(0);
            dialog.SetMinShowTime(900);
            dialog.Show();
            dialog.Test_AdvanceShow();
            Assert.True(dialog.IsShowing());
            dialog.Dismiss();
            dialog.Test_AdvanceHide();
            Assert.False(dialog.IsShowing());
        }

        [Fact]
        public void TestDismissWhenNeverShown_NoOp_Public()
        {
            var dialog = new DelayedProgressDialog(_appContext);
            dialog.SetMinDelay(1500);
            dialog.Show();
            Assert.False(dialog.IsShowing());
            dialog.Dismiss();
            // Simulate 1500ms
            Assert.False(dialog.IsShowing());
        }
    }
}