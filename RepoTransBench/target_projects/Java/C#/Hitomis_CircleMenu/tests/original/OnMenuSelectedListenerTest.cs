using Xunit;

namespace Hitomis_CircleMenu.Tests
{
    public class OnMenuSelectedListenerTest
    {
        class TestListener : IOnMenuSelectedListener
        {
            public int LastSelectedIndex = -1;
            public void OnMenuSelected(int index)
            {
                LastSelectedIndex = index;
            }
        }

        [Fact]
        public void TestOnMenuSelectedCalled()
        {
            var listener = new TestListener();
            listener.OnMenuSelected(2);
            Assert.Equal(2, listener.LastSelectedIndex);
            listener.OnMenuSelected(0);
            Assert.Equal(0, listener.LastSelectedIndex);
        }
    }

    public interface IOnMenuSelectedListener
    {
        void OnMenuSelected(int index);
    }
}