using Xunit;
using Aegis1980.Hotspot;

namespace Aegis1980.Hotspot.PublicTests
{
    public class PublicHotSpotManagerTests
    {
        [Fact]
        public void TestInitialStatePublic()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.IsEnabled());
            Assert.Equal("defaultSSID", manager.GetSsid());
            Assert.Equal("password", manager.GetPassword());
        }

        [Fact]
        public void TestEnableHotspotValidPublic()
        {
            var manager = new HotSpotManager();
            bool result = manager.EnableHotspot("PublicSSID", "Another123");
            Assert.True(result);
            Assert.True(manager.IsEnabled());
            Assert.Equal("PublicSSID", manager.GetSsid());
            Assert.Equal("Another123", manager.GetPassword());
        }

        [Fact]
        public void TestEnableHotspotInvalidSsidPublic()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot(null, "publicpass"));
            Assert.False(manager.EnableHotspot("", "publicpass"));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotInvalidPasswordPublic()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot("MyNetwork", null));
            Assert.False(manager.EnableHotspot("MyNetwork", "short1"));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestDisableHotspotPublic()
        {
            var manager = new HotSpotManager();
            manager.EnableHotspot("Network42", "SuperPass9");
            Assert.True(manager.IsEnabled());
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotPasswordExactly8Public()
        {
            var manager = new HotSpotManager();
            string password8 = "abcdefgh";
            bool result = manager.EnableHotspot("SSID_Public", password8);
            Assert.True(result);
            Assert.True(manager.IsEnabled());
            Assert.Equal("SSID_Public", manager.GetSsid());
            Assert.Equal(password8, manager.GetPassword());
        }

        [Fact]
        public void TestDisablingTwicePublic()
        {
            var manager = new HotSpotManager();
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
            manager.EnableHotspot("PublicSSID2", "ExtraPass2");
            Assert.True(manager.IsEnabled());
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
            manager.DisableHotspot();
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotPasswordWith8ButNullSSIDPublic()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot(null, "abcdefgh"));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotNullPasswordPublic()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot("AnotherNet", null));
            Assert.False(manager.IsEnabled());
        }

        [Fact]
        public void TestMultipleEnablesPublic()
        {
            var manager = new HotSpotManager();
            Assert.True(manager.EnableHotspot("FirstSSID", "initPass99"));
            Assert.Equal("FirstSSID", manager.GetSsid());
            Assert.Equal("initPass99", manager.GetPassword());
            Assert.True(manager.IsEnabled());

            Assert.True(manager.EnableHotspot("SecondSSID", "reNewPass0"));
            Assert.Equal("SecondSSID", manager.GetSsid());
            Assert.Equal("reNewPass0", manager.GetPassword());
            Assert.True(manager.IsEnabled());
        }

        [Fact]
        public void TestEnableHotspotEmptyPasswordPublic()
        {
            var manager = new HotSpotManager();
            Assert.False(manager.EnableHotspot("MyNet", ""));
            Assert.False(manager.IsEnabled());
        }
    }
}