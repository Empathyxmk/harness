using Xunit;
using EasyLoadingBtn.Models;

namespace EasyLoadingBtn.PublicTests
{
    public class LoadingButtonPublicTest
    {
        private LoadingButton loadingButton;

        public LoadingButtonPublicTest()
        {
            // Setup (equivalent to @Before)
            loadingButton = new LoadingButton();
        }

        [Fact]
        public void TestInitialState_PublicVariant()
        {
            Assert.False(loadingButton.IsCompleted());
            Assert.False(loadingButton.IsShowArc());
        }

        [Fact]
        public void TestSetTargetProgress_SetsDifferentProgress()
        {
            loadingButton.SetTargetProgress(250); // public test uses 250
            Assert.Equal(250, loadingButton.GetTargetProgress());
        }

        [Fact]
        public void TestSetAndGetCallback_Public()
        {
            bool flag = false;
            LoadingButton.Callback cb = () => { flag = true; };
            loadingButton.SetCallback(cb);
            loadingButton.PerformCompleteCallback();
            Assert.True(flag);
        }

        [Fact]
        public void TestSetCompleted_AlternatePattern()
        {
            loadingButton.SetCompleted(false);
            Assert.False(loadingButton.IsCompleted());
            loadingButton.SetCompleted(true);
            Assert.True(loadingButton.IsCompleted());
        }

        [Fact]
        public void TestOnClick_WithCompleted_Public()
        {
            loadingButton.SetCompleted(true);
            Assert.True(loadingButton.IsCompleted());
            bool result = loadingButton.PerformClick();
            Assert.True(result);
        }

        [Fact]
        public void TestOnClick_WithNotCompleted_Public()
        {
            loadingButton.SetCompleted(false);
            bool result = loadingButton.PerformClick();
            Assert.False(result);
        }

        [Fact]
        public void TestSetShowArc_Public()
        {
            loadingButton.SetShowArc(false);
            Assert.False(loadingButton.IsShowArc());
            loadingButton.SetShowArc(true);
            Assert.True(loadingButton.IsShowArc());
        }
    }
}