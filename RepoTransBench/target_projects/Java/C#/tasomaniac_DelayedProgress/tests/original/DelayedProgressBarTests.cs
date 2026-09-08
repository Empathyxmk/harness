using Xunit;
using Moq;
using ProjectName;

namespace OriginalTests
{
    public class DelayedProgressBarTests
    {
        private object _appContext = new object(); // Stub for Application

        [Fact]
        public void TestConstructors()
        {
            var progressBar1 = new DelayedProgressBar(_appContext);
            Assert.False(progressBar1.IsShown());

            var progressBar2 = new DelayedProgressBar(_appContext, null);
            Assert.False(progressBar2.IsShown());
        }

        [Fact]
        public void TestShow_NoDelay()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.Show();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            Assert.Equal(0f, progressBar.GetAlpha(), 3);
        }

        [Fact]
        public void TestShow_WithAnimation()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.SetAlpha(0f);
            Assert.Equal(0f, progressBar.GetAlpha(), 3);
            progressBar.Show(true);
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            Assert.Equal(1.0f, progressBar.GetAlpha(), 3);
        }

        [Fact]
        public void TestShow_WithAnimationAndEndAction()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            var endAction = new Mock<System.Action>();
            progressBar.SetAlpha(0f);
            progressBar.Show(true, endAction.Object);
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            endAction.Verify(a => a.Invoke(), Times.Once);
        }

        [Fact]
        public void TestHideBeforeMinDelay_ShouldNotShow()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.Show();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            // Simulate advance of 200ms
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
            progressBar.Hide();
            // Simulate advance after cancellation
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }

        [Fact]
        public void TestHideAfterMinDelayButBeforeMinShowTime_ShouldShowForMinShowTime()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.Show();
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // Simulate 200ms pass (MIN_SHOW_TIME = 500)
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            progressBar.Hide();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // Simulate 299 more ms
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // Simulate 1 ms passes - now should hide
            progressBar.Test_AdvanceHide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }

        [Fact]
        public void TestHideAfterMinShowTime_ShouldHideImmediately()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.Show();
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            // Simulate extra 500ms for min show
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            progressBar.Hide();
            progressBar.Test_AdvanceHide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }

        [Fact]
        public void TestHideWithAnimation_HidesWithFade()
        {
            var progressBar = new DelayedProgressBar(_appContext);
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
        public void TestHideWithAnimationAndEndAction_HidesWithFadeAndRunsEndAction()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            var endAction = new Mock<System.Action>();
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
        public void TestOnDetachedFromWindowRemovesCallbacks()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.Show();
            // Simulate scheduled callback present

            progressBar.OnDetachedFromWindow();
            // Simulate callbacks cleared

            progressBar.Show();
            progressBar.Test_AdvanceShow();
            progressBar.Hide();
            // Simulate scheduled callback present

            progressBar.OnDetachedFromWindow();
            // Simulate callbacks cleared
        }

        [Fact]
        public void TestImmediateHideWhenNeverShown()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.Hide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }

        [Fact]
        public void TestShowAndHideCalledMultipleTimes()
        {
            var progressBar = new DelayedProgressBar(_appContext);
            progressBar.Show();
            // Simulate 100ms
            progressBar.Hide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());

            progressBar.Show();
            progressBar.Test_AdvanceShow();
            Assert.Equal(AndroidViewVisibility.VISIBLE, progressBar.GetVisibility());
            progressBar.Hide();
            progressBar.Test_AdvanceHide();
            Assert.Equal(AndroidViewVisibility.GONE, progressBar.GetVisibility());
        }
    }
}