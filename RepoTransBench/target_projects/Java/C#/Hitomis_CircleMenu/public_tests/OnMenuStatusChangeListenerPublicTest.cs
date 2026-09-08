using Xunit;

namespace Hitomis_CircleMenu.PublicTests
{
    public class OnMenuStatusChangeListenerPublicTest
    {
        [Fact]
        public void Test_OnMenuOpened_And_OnMenuClosed_Different()
        {
            var menuListener = new Listener();
            menuListener.OnMenuOpened();
            menuListener.OnMenuClosed();
            Assert.Equal("OpenedPublic", menuListener.OpenedStatus);
            Assert.Equal("ClosedPublic", menuListener.ClosedStatus);
        }

        private class Listener : IOnMenuStatusChangeListener
        {
            public string OpenedStatus = null, ClosedStatus = null;
            public void OnMenuOpened() { OpenedStatus = "OpenedPublic"; Assert.Equal("OpenedPublic", OpenedStatus); }
            public void OnMenuClosed() { ClosedStatus = "ClosedPublic"; Assert.Equal("ClosedPublic", ClosedStatus); }
        }

        private interface IOnMenuStatusChangeListener
        {
            void OnMenuOpened();
            void OnMenuClosed();
        }
    }
}