using Xunit;
using Aegis1980.Hotspot;

namespace Aegis1980.Hotspot.Tests.Original
{
    public class HotSpotManagerTests
    {
        [Fact]
        public void TestInitialState()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.IsEnabled());
            Assert.Equal("defaultSSID", manager.GetSsid());
            Assert.Equal("password", manager.GetPassword());
        }

        [Fact]
        public void TestEnableHotspotValid()
        {
            var manager = new HotSpotManager();
            bool result = manager.EnableHotspot("MySSID", "MyPass123");
            Assert.True(result);
            Assert.True(manager.IsEnabled());
            Assert.Equal("MySSID", manager.GetSsid());
            Assert.Equal("MyPass123", manager.GetPassword());
        }

        [Fact]
        public void TestEnableHotspotInvalidSsid()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot(null, "password123"));
            Assert.False(manager.EnableHotspot("", "password123"));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotInvalidPassword()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot("SSID", null));
            Assert.False(manager.EnableHotspot("SSID", "short"));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestDisableHotspot()
        {
            var manager = new HotSpotManager();
            manager.EnableHotspot("SSID", "password123");
            Assert.True(manager.IsEnabled());
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
        }

        // NEW TESTS FOR FULL BRANCH COVERAGE

        [Fact]
        public void TestEnableHotspotPasswordExactly8()
        {
            var manager = new HotSpotManager();
            string password8 = "12345678";
            bool result = manager.EnableHotspot("SSID2", password8);
            Assert.True(result);
            Assert.True(manager.IsEnabled());
            Assert.Equal("SSID2", manager.GetSsid());
            Assert.Equal(password8, manager.GetPassword());
        }

        [Fact]
        public void TestDisablingTwice()
        {
            var manager = new HotSpotManager();
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
            manager.EnableHotspot("SSID", "password123");
            Assert.True(manager.IsEnabled());
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotPasswordWith8ButNullSSID()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot(null, "12345678"));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotNullPassword()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot("SSID", null));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestMultipleEnables()
        {
            var manager = new HotSpotManager();
            Assert.True(manager.EnableHotspot("SSID", "password123"));
            Assert.Equal("SSID", manager.GetSsid());
            Assert.Equal("password123", manager.GetPassword());
            Assert.True(manager.IsEnabled());

            Assert.True(manager.EnableHotspot("SSID2", "password456"));
            Assert.Equal("SSID2", manager.GetSsid());
            Assert.Equal("password456", manager.GetPassword());
            Assert.True(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotEmptyPassword()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot("SSID", ""));
            Assert.False(manager.IsEnabled());
        }
    }
}