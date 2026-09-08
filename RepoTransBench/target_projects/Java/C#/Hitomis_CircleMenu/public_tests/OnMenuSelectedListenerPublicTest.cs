using Xunit;

namespace Hitomis_CircleMenu.PublicTests
{
    public class OnMenuSelectedListenerPublicTest
    {
        [Fact]
        public void Test_OnMenuSelected_WithDifferentIndex()
        {
            var wasCalled = false;
            IOnMenuSelectedListener listener = new TestListener(i =>
            {
                Assert.Equal(2, i);
                wasCalled = true;
            });
            listener.OnMenuSelected(2);
            Assert.True(wasCalled);
        }

        public interface IOnMenuSelectedListener
        {
            void OnMenuSelected(int index);
        }
        public class TestListener : IOnMenuSelectedListener
        {
            private readonly System.Action<int> action;
            public TestListener(System.Action<int> action) { this.action = action; }
            public void OnMenuSelected(int index) { action(index); }
        }
    }
}