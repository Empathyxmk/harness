using Xunit;
using KeepAwakeLib;

namespace KeepAwakeTests
{
    public class KeepAwakeTests
    {
        [Fact]
        public void TestInitialState()
        {
            var ka = new KeepAwake();
            Assert.False(ka.IsAwake());
            Assert.Equal("Sleeping", ka.GetStatus());
        }

        [Fact]
        public void TestActivate()
        {
            var ka = new KeepAwake();
            ka.Activate();
            Assert.True(ka.IsAwake());
            Assert.Equal("Awake", ka.GetStatus());
        }

        [Fact]
        public void TestDeactivate()
        {
            var ka = new KeepAwake();
            ka.Activate();
            ka.Deactivate();
            Assert.False(ka.IsAwake());
            Assert.Equal("Sleeping", ka.GetStatus());
        }

        [Fact]
        public void TestActivateIdempotence()
        {
            var ka = new KeepAwake();
            ka.Activate();
            ka.Activate();
            Assert.True(ka.IsAwake());
        }

        [Fact]
        public void TestDeactivateIdempotence()
        {
            var ka = new KeepAwake();
            ka.Deactivate();
            Assert.False(ka.IsAwake());
        }

        [Fact]
        public void TestSetAwakeTrue()
        {
            var ka = new KeepAwake();
            ka.SetAwake(true);
            Assert.True(ka.IsAwake());
        }

        [Fact]
        public void TestSetAwakeFalse()
        {
            var ka = new KeepAwake();
            ka.SetAwake(true);
            ka.SetAwake(false);
            Assert.False(ka.IsAwake());
        }

        [Fact]
        public void TestMultipleTransitions()
        {
            var ka = new KeepAwake();
            ka.SetAwake(true);
            Assert.Equal("Awake", ka.GetStatus());
            ka.SetAwake(false);
            Assert.Equal("Sleeping", ka.GetStatus());
            ka.SetAwake(true);
            Assert.Equal("Awake", ka.GetStatus());
        }
    }
}