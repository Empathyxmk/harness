using Xunit;
using Ch02Core.Lifecycle;

namespace OriginalTests.Lifecycle
{
    public class SUTTest : System.IDisposable
    {
        private static ResourceForAllTests? _resourceForAllTests;
        private SUT _systemUnderTest;

        static SUTTest()
        {
            _resourceForAllTests = new ResourceForAllTests("Our resource for all tests");
        }

        public SUTTest()
        {
            _systemUnderTest = new SUT("Our system under test");
        }

        public void Dispose()
        {
            _systemUnderTest?.Close();
        }

        [Fact]
        public void TestRegularWork()
        {
            bool canReceiveRegularWork = _systemUnderTest.CanReceiveRegularWork();
            Assert.True(canReceiveRegularWork);
        }

        [Fact]
        public void TestAdditionalWork()
        {
            bool canReceiveAdditionalWork = _systemUnderTest.CanReceiveAdditionalWork();
            Assert.False(canReceiveAdditionalWork);
        }
    }
}