using Xunit;
using aegis1980_WifiHotSpot;

namespace aegis1980_WifiHotSpot.Tests
{
    public class HotSpotManagerTests
    {
        [Fact]
        public void DummyTest_HotSpotManager_Exists()
        {
            var manager = new HotSpotManager();
            Assert.NotNull(manager);
        }
    }
}