using Xunit;

namespace Hitomis_CircleMenu.Tests
{
    public class OnMenuStatusChangeListenerTest
    {
        class TestListener : IOnMenuStatusChangeListener
        {
            public bool opened = false;
            public bool closed = false;
            public void OnMenuOpened()
            {
                opened = true;
            }
            public void OnMenuClosed()
            {
                closed = true;
            }
        }

        [Fact]
        public void TestOnMenuOpenedAndClosed()
        {
            var listener = new TestListener();
            Assert.False(listener.opened);
            Assert.False(listener.closed);

            listener.OnMenuOpened();
            Assert.True(listener.opened);

            listener.OnMenuClosed();
            Assert.True(listener.closed);
        }
    }

    // Provide the interface signature as per the test
    public interface IOnMenuStatusChangeListener
    {
        void OnMenuOpened();
        void OnMenuClosed();
    }
}