using Xunit;
using KeepAwakeLib;

namespace KeepAwakePublicTests
{
    /// <summary>
    /// Public tests for the KeepAwake class.
    /// These tests follow the same logic and functionality as the private/internal tests,
    /// but use different test data or sequence variations to ensure coverage with new scenarios.
    /// </summary>
    public class KeepAwakePublicTests
    {
        [Fact]
        public void TestNotAwakeAfterConstruction()
        {
            var ka = new KeepAwake();
            // Check initial state remains sleeping and not awake
            Assert.False(ka.IsAwake());
            Assert.NotEqual("Awake", ka.GetStatus());
            Assert.Equal("Sleeping", ka.GetStatus());
        }

        [Fact]
        public void TestActivateFromFalse()
        {
            var ka = new KeepAwake();
            // Activate once, should be awake
            ka.Activate();
            Assert.True(ka.IsAwake());
            // Confirm getStatus gives "Awake"
            Assert.Contains("Awake", ka.GetStatus());
        }

        [Fact]
        public void TestDeactivateAfterActivation()
        {
            var ka = new KeepAwake();
            ka.SetAwake(true); // Activate using setAwake
            ka.Deactivate();
            // Should now be sleeping
            Assert.False(ka.IsAwake());
            Assert.NotEqual("Awake", ka.GetStatus());
        }

        [Fact]
        public void TestMultipleActivatesRemainAwake()
        {
            var ka = new KeepAwake();
            // Activate multiple times
            ka.Activate();
            ka.Activate();
            ka.Activate();
            Assert.True(ka.IsAwake());
            Assert.Equal("Awake", ka.GetStatus());
        }

        [Fact]
        public void TestMultipleDeactivatesRemainSleeping()
        {
            var ka = new KeepAwake();
            ka.Deactivate();
            ka.Deactivate();
            Assert.False(ka.IsAwake());
            Assert.Equal("Sleeping", ka.GetStatus());
        }

        [Fact]
        public void TestSetAwakeToTrueSetsAwakeStatus()
        {
            var ka = new KeepAwake();
            ka.SetAwake(true);
            Assert.True(ka.IsAwake());
            Assert.Equal("Awake", ka.GetStatus());
        }

        [Fact]
        public void TestSetAwakeToFalseFromAwake()
        {
            var ka = new KeepAwake();
            ka.Activate();
            ka.SetAwake(false);
            Assert.False(ka.IsAwake());
            Assert.Equal("Sleeping", ka.GetStatus());
        }

        [Fact]
        public void TestToggleMultipleTimes()
        {
            var ka = new KeepAwake();
            ka.Activate();
            Assert.Equal("Awake", ka.GetStatus());
            ka.Deactivate();
            Assert.Equal("Sleeping", ka.GetStatus());
            ka.Activate();
            Assert.Equal("Awake", ka.GetStatus());
            ka.Deactivate();
            Assert.Equal("Sleeping", ka.GetStatus());
        }
    }
}