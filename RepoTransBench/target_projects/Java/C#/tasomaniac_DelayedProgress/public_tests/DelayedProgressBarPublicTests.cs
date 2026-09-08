using Xunit;
using Moq;
using ProjectName;

namespace PublicTests
{
    public class DelayedProgressBarPublicTests
    {
        private object _appContext = new object();

        [Fact]
        public void TestConstructors_Public()
        {
            var progressBar1 = new DelayedProgressBar(_appContext);
            Assert.False(progressBar1.IsShown());
            var progressBar2 = new DelayedProgressBar(_appContext, null);
            Assert.False(progressBar2.IsShown());
        }

        [Fact]
        public void TestShow_NoDelay_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetMinDelay(300);
            progressBar.SetMinShowTime(700);
            progressBar.Show();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            Assert.Equal(0f, progressBar.GetAlpha(), 3);
        }

        [Fact]
        public void TestShow_WithAnimation_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetAlpha(0f);
            progressBar.SetMinDelay(350);
            progressBar.Show(true);
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            Assert.Equal(1.0f, progressBar.GetAlpha(), 3);
        }

        [Fact]
        public void TestShow_WithAnimationAndEndAction_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            var endAction = new Mock<System.Action>();
            progressBar.SetAlpha(0f);
            progressBar.SetMinDelay(250);
            progressBar.Show(true, endAction.Object);
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            endAction.Verify(a => a.Invoke(), Times.Once);
        }

        [Fact]
        public void TestHideBeforeMinDelay_ShouldNotShow_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetMinDelay(400);
            progressBar.Show();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            // Simulate 150ms tick
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            progressBar.Hide();
            // Simulate more
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }

        [Fact]
        public void TestHideAfterMinDelayButBeforeMinShowTime_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetMinDelay(350);
            progressBar.SetMinShowTime(650);
            progressBar.Show();
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // Simulate 250ms
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            progressBar.Hide();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // 399ms
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // 1ms more
            progressBar.Test_AdvanceHide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }

        [Fact]
        public void TestHideAfterMinShowTime_ShouldHideImmediately_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetMinDelay(280);
            progressBar.SetMinShowTime(420);
            progressBar.Show();
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // 420ms more
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            progressBar.Hide();
            progressBar.Test_AdvanceHide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }

        [Fact]
        public void TestHideWithAnimation_HidesWithFade_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetMinDelay(220);
            progressBar.SetMinShowTime(330);
            progressBar.Show();
            progressBar.Test_AdvanceShow();
            progressBar.SetAlpha(1.0f);
            progressBar.Hide(true);
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            progressBar.Test_AdvanceHide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            Assert.Equal(0f, progressBar.GetAlpha(), 3);
        }

        [Fact]
        public void TestHideWithAnimationAndEndAction_HidesWithFadeAndRunsEndAction_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            var endAction = new Mock<System.Action>();
            progressBar.SetMinDelay(420);
            progressBar.SetMinShowTime(350);
            progressBar.Show();
            progressBar.Test_AdvanceShow();
            progressBar.SetAlpha(1.0f);
            progressBar.Hide(true, endAction.Object);
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            progressBar.Test_AdvanceHide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            endAction.Verify(a => a.Invoke(), Times.Once);
        }

        [Fact]
        public void TestOnDetachedFromWindowRemovesCallbacks_Public()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetMinDelay(290);
            progressBar.Show();
            // Simulate scheduled callback

            progressBar.OnDetachedFromWindow();
            // Callbacks cleared

            progressBar.SetMinDelay(310);
            progressBar.Show();
            progressBar.Test_AdvanceShow();
            progressBar.Hide();
            // Simulate scheduled callback

            progressBar.OnDetachedFromWindow();
            // Callbacks cleared
        }
    }
}