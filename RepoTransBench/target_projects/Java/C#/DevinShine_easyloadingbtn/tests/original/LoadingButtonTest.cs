using Xunit;
using EasyLoadingBtn.Models;

namespace EasyLoadingBtn.Tests.Original
{
    public class LoadingButtonTest
    {
        private LoadingButton loadingButton;

        public LoadingButtonTest()
        {
            // Setup (equivalent to @Before)
            loadingButton = new LoadingButton();
        }

        [Fact]
        public void TestInitialState()
        {
            Assert.False(loadingButton.IsCompleted());
            Assert.False(loadingButton.IsShowArc());
        }

        [Fact]
        public void TestSetTargetProgress_SetsProgress()
        {
            loadingButton.SetTargetProgress(180);
            Assert.Equal(180, loadingButton.GetTargetProgress());
        }

        [Fact]
        public void TestSetAndGetCallback()
        {
            bool wasCalled = false;
            LoadingButton.Callback cb = () => { wasCalled = true; };
            loadingButton.SetCallback(cb);
            loadingButton.PerformCompleteCallback();
            Assert.True(wasCalled);
        }

        [Fact]
        public void TestSetCompleted()
        {
            loadingButton.SetCompleted(true);
            Assert.True(loadingButton.IsCompleted());
            loadingButton.SetCompleted(false);
            Assert.False(loadingButton.IsCompleted());
        }

        [Fact]
        public void TestOnClick_WithNotCompleted()
        {
            loadingButton.SetCompleted(false);
            bool result = loadingButton.PerformClick();
            // We expect PerformClick to NOT return true for not completed
            Assert.False(result);
        }

        [Fact]
        public void TestOnClick_WithCompleted()
        {
            loadingButton.SetCompleted(true);
            Assert.True(loadingButton.IsCompleted());
            bool result = loadingButton.PerformClick();
            // PerformClick should return true if completed
            Assert.True(result);
        }

        [Fact]
        public void TestSetShowArc()
        {
            loadingButton.SetShowArc(true);
            Assert.True(loadingButton.IsShowArc());
            loadingButton.SetShowArc(false);
            Assert.False(loadingButton.IsShowArc());
        }
    }
}